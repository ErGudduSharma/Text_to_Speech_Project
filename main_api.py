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

from fastapi.staticfiles import StaticFiles

# Include Routers
app.include_router(gtts_router.router) # Include gtts router to app
app.include_router(edge_tts_router.router) # Include edge tts router to app

# Mount output folder for static access
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/library", tags=["Library"])
async def get_library():
    """
    List all generated audio files stored in the output directory and subdirectories.
    """
    try:
        files = []
        for root, dirs, filenames in os.walk(OUTPUT_DIR):
            for filename in filenames:
                if filename.endswith(".mp3"):
                    # Get relative path for URL
                    rel_dir = os.path.relpath(root, OUTPUT_DIR)
                    if rel_dir == ".":
                        file_url = f"/output/{filename}"
                    else:
                        file_url = f"/output/{rel_dir.replace(os.sep, '/')}/{filename}"
                        
                    stats = os.stat(os.path.join(root, filename))
                    files.append({
                        "name": filename,
                        "url": file_url,
                        "date": stats.st_mtime,
                        "size": stats.st_size,
                        "engine": rel_dir if rel_dir != "." else "general"
                    })
        # Sort by newest first
        files.sort(key=lambda x: x["date"], reverse=True)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}


from fastapi.responses import HTMLResponse

@app.get("/", tags=["UI"])
async def root():
    """
    Serve the frontend UI for live streaming TTS.
    """
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return {"message": "Welcome to the Dual Text-to-Speech API. Visit /docs for Swagger UI. (Frontend index.html not found)"}
