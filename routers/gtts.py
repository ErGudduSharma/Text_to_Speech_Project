from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS
import os
import uuid
import io
from utils import log_input

# Initialize router for gTTS
router = APIRouter(prefix="/gtts", tags=["Google TTS"])

# Output directory for usage
BASE_OUTPUT_DIR = "output"
GTTS_OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, "gtts")
os.makedirs(GTTS_OUTPUT_DIR, exist_ok=True)

# Request model for gTTS API
class GTTSRequest(BaseModel):
    text: str
    lang: str = "en"
    slow: bool = False

@router.post("/generate", summary="Generate MP3 from text using Google TTS")
async def generate_gtts_audio(request: GTTSRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Log input
        log_input(request.text, "gtts", request.lang)

        # Generate unique filename
        random_filename = f"gtts_{uuid.uuid4()}.mp3"
        file_path = os.path.join(GTTS_OUTPUT_DIR, random_filename)
        
        # Initialize gTTS
        tts = gTTS(text=request.text, lang=request.lang, slow=request.slow)
        
        # Save the audio file
        tts.save(file_path)
        
        return {
            "status": "success",
            "message": "gTTS audio generated successfully",
            "file_name": random_filename,
            "file_path": f"/output/gtts/{random_filename}",
            "engine": "gTTS"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream", summary="Stream audio and save to disk")
async def stream_gtts_audio(
    text: str,
    lang: str = "en"
):
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Log input
        log_input(text, "gtts", lang)

        # Generate unique filename
        file_id = str(uuid.uuid4())[:8]
        filename = f"live_gtts_{file_id}.mp3"
        file_path = os.path.join(GTTS_OUTPUT_DIR, filename)

        # Initialize gTTS
        tts = gTTS(text=text, lang=lang)
        
        # Save to file
        tts.save(file_path)

        def generate():
            with open(file_path, "rb") as f:
                yield f.read()

        return StreamingResponse(
            generate(), 
            media_type="audio/mpeg",
            headers={"X-Audio-Path": f"/output/gtts/{filename}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

