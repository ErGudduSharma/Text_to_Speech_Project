from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from gtts import gTTS
import os
import uuid


# Initialize router for gTTS
router = APIRouter(prefix="/gtts", tags=["Google TTS"])

# Output directory for usage
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Request model for gTTS API
class GTTSRequest(BaseModel):
    text: str
    lang: str = "en"
    slow: bool = False

@router.post("/generate", summary="Generate MP3 from text using Google TTS")
async def generate_gtts_audio(request: GTTSRequest):
    """
    Convert text to speech using Google TTS (gTTS) and save as an MP3 file.
    
    - **text**: The text to convert.
    - **lang**: Language code (default: 'en').
    - **slow**: Whether to speak slowly (default: False).
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Generate unique filename
        random_filename = f"gtts_{uuid.uuid4()}.mp3"
        file_path = os.path.join(OUTPUT_DIR, random_filename)
        
        # Initialize gTTS
        tts = gTTS(text=request.text, lang=request.lang, slow=request.slow)
        
        # Save the audio file
        tts.save(file_path)
        
        return {
            "status": "success",
            "message": "gTTS audio generated successfully",
            "file_name": random_filename,
            "file_path": file_path,
            "engine": "gTTS"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
