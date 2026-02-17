from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import time
import re
from pydantic import BaseModel
import edge_tts
import os
import uuid
import asyncio
from utils import log_input

router = APIRouter(prefix="/edge-tts", tags=["Microsoft Edge TTS"])

# Output directory for usage
BASE_OUTPUT_DIR = "output"
EDGE_OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, "edge")
os.makedirs(EDGE_OUTPUT_DIR, exist_ok=True)

class EdgeTTSRequest(BaseModel):
    text: str
    voice: str = "en-US-AriaNeural"
    rate: str = "+0%"
    volume: str = "+0%"
    pitch: str = "+0Hz"

@router.post("/generate", summary="Generate MP3 from text using Microsoft Edge TTS")
async def generate_edge_audio(request: EdgeTTSRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Log input
        log_input(request.text, "edge", request.voice)

        # Generate unique filename
        random_filename = f"edge_{uuid.uuid4()}.mp3"
        file_path = os.path.join(EDGE_OUTPUT_DIR, random_filename)

        # Communicate with Edge TTS
        communicate = edge_tts.Communicate(
            text=request.text,
            voice=request.voice,
            rate=request.rate,
            volume=request.volume,
            pitch=request.pitch
        )
        
        await communicate.save(file_path)

        return {
            "status": "success",
            "message": "Edge TTS audio generated successfully",
            "file_name": random_filename,
            "file_path": f"/output/edge/{random_filename}",
            "engine": "Edge TTS"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list-voices", summary="List available Edge TTS voices")
async def list_edge_voices():
    try:
        voices = await edge_tts.list_voices()
        simple_voices = [
            {
                "Name": v["Name"],
                "ShortName": v["ShortName"],
                "Gender": v["Gender"],
                "Locale": v["Locale"]
            }
            for v in voices
        ]
        return {"voices": simple_voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream", summary="Stream audio and save to disk")
async def stream_edge_audio(
    text: str = Query(..., description="The text to convert to speech"),
    voice: str = Query("hi-IN-SwaraNeural", description="Voice model"),
    rate: str = Query("+0%", description="Speech rate adjustment"),
    volume: str = Query("+0%", description="Volume adjustment"),
    pitch: str = Query("+0Hz", description="Pitch adjustment")
):
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Log input
        log_input(text, "edge", voice)

        # Generate unique filename for storage
        file_id = str(uuid.uuid4())[:8]
        filename = f"live_edge_{file_id}.mp3"
        file_path = os.path.join(EDGE_OUTPUT_DIR, filename)

        async def audio_generator():
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=rate,
                volume=volume,
                pitch=pitch
            )
            
            with open(file_path, "wb") as f:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                        yield chunk["data"]

        return StreamingResponse(
            audio_generator(), 
            media_type="audio/mpeg",
            headers={"X-Audio-Path": f"/output/edge/{filename}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            text = data.get("text", "")
            engine = data.get("engine", "edge")
            voice = data.get("voice", "hi-IN-SwaraNeural")
            
            if not text.strip():
                continue

            # Log input
            log_input(text, engine, voice)

            # Use appropriate output directory
            current_out_dir = os.path.join(BASE_OUTPUT_DIR, engine)
            os.makedirs(current_out_dir, exist_ok=True)

            # Optimized chunking strategy
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
            
            # Temporary storage for merging or final saving
            temp_dir = os.path.join(BASE_OUTPUT_DIR, "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            merged_audio = b""
            last_final_path = ""

            for sentence in sentences:
                try:
                    start_time = time.time()
                    file_id = str(uuid.uuid4())[:8]
                    # Intermediate files go to temp
                    filename = f"part_{engine}_{file_id}.mp3"
                    file_path = os.path.join(temp_dir, filename)

                    sentence_audio = b""
                    if engine == "edge":
                        communicate = edge_tts.Communicate(
                            text=sentence, voice=voice, rate="+0%", volume="+0%"
                        )
                        async for chunk in communicate.stream():
                            if chunk["type"] == "audio":
                                sentence_audio += chunk["data"]
                        
                        # Send full sentence audio for clean decoding
                        if sentence_audio:
                            await websocket.send_bytes(sentence_audio)
                    else:
                        from gtts import gTTS
                        import io
                        tts = gTTS(text=sentence, lang=voice)
                        mp3_fp = io.BytesIO()
                        tts.write_to_fp(mp3_fp)
                        sentence_audio = mp3_fp.getvalue()
                        if sentence_audio:
                            await websocket.send_bytes(sentence_audio)

                    
                    merged_audio += sentence_audio
                    
                    # Save intermediate only if needed, but we save the full one at the end
                    with open(file_path, "wb") as f:
                        f.write(sentence_audio)

                    end_time = time.time()
                    latency = round((end_time - start_time) * 1000, 2)
                    
                    await websocket.send_json({
                        "type": "report",
                        "sentence": sentence,
                        "latency_ms": latency,
                        "engine": engine,
                        "file_path": f"/output/temp/{filename}",
                        "status": "streaming"
                    })
                except Exception as inner_e:
                    print(f"Inner WS error: {inner_e}")

            # SAVE FINAL AUDIO (The complete text)
            if merged_audio:
                final_id = str(uuid.uuid4())[:10]
                final_filename = f"final_{engine}_{final_id}.mp3"
                final_path = os.path.join(current_out_dir, final_filename)
                with open(final_path, "wb") as f:
                    f.write(merged_audio)
                
                # Send a final report with the permanent link
                await websocket.send_json({
                    "type": "final",
                    "file_path": f"/output/{engine}/{final_filename}",
                    "message": "Full audio saved successfully"
                })

    except WebSocketDisconnect:
        print("WebSocket client disconnected normally.")
    except Exception as e:
        print(f"Fatal WebSocket error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except:
            pass




