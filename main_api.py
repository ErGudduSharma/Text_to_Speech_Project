from fastapi import FastAPI
from routers import gtts as gtts_router
from routers import edge as edge_tts_router
import os

# Initialize FastAPI app (web server)
app = FastAPI(
    title="Dual Text-to-Speech API",
    description="API to convert text to speech using Google TTS (gTTS) and Microsoft Edge TTS.",
    version="2.0.0"
)

# Output directory ensure it exists
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok = True)

# Include Routers
app.include_router(gtts_router.router) # Include gtts router to app
app.include_router(edge_tts_router.router) # Include edge tts router to app

@app.get("/", tags = ["Health"])
async def root(): # Root endpoint for health check
    return {"message": "Welcome to the Dual Text-to-Speech API. Visit /docs for Swagger UI."}
