from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import edge_tts
import os
import uuid
import asyncio

router = APIRouter(prefix="/edge-tts", tags=["Microsoft Edge TTS"])

# Output directory for usage
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class EdgeTTSRequest(BaseModel):
    text: str
    voice: str = "en-US-AriaNeural"
    rate: str = "+0%"
    volume: str = "+0%"
    pitch: str = "+0Hz"

@router.post("/generate", summary="Generate MP3 from text using Microsoft Edge TTS")
async def generate_edge_audio(request: EdgeTTSRequest):
    """
    Convert text to speech using Microsoft Edge TTS and save as an MP3 file.
    
    - **text**: The text to convert.
    - **voice**: Voice model (default: 'en-US-AriaNeural'). Examples: 'en-US-GuyNeural', 'hi-IN-SwaraNeural'.
    - **rate**: Speech rate adjustment (default: '+0%').
    - **volume**: Volume adjustment (default: '+0%').
    - **pitch**: Pitch adjustment (default: '+0Hz').
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Generate unique filename
        random_filename = f"edge_{uuid.uuid4()}.mp3"
        file_path = os.path.join(OUTPUT_DIR, random_filename)

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
            "file_path": file_path,
            "engine": "Edge TTS"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list-voices", summary="List available Edge TTS voices")
async def list_edge_voices():
    """
    List all available voices for Edge TTS.
    """
    try:
        voices = await edge_tts.list_voices()
        # Filter details to keep response manageable
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
