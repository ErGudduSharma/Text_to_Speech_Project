# Dual Text-to-Speech API Project

This project provides a robust REST API to convert text into speech using two powerful engines:
1.  **Google Text-to-Speech (gTTS)**: Simple, online, multi-language support.
2.  **Microsoft Edge TTS**: High-quality, neural voices, online, free.

The API is built with **FastAPI** and uses **Swagger UI** for interactive documentation and testing.

## Features
- **Modular Design**: Separate routers for gTTS and Edge TTS logic to ensure clean code and no overlap.
- **Google TTS Support**:
    -   Language selection (`lang`).
    -   Slow speech option (`slow`).
- **Edge TTS Support**:
    -   Neural voices (e.g., `en-US-AriaNeural`, `hi-IN-SwaraNeural`).
    -   Adjustable Rate, Volume, and Pitch.
    -   Voice listing endpoint.
- **Random Output Filenames**: Generates unique filenames (UUID) to prevent overwrites, stored in `output/` folder.

## Prerequisites
- Python 3.7+
- pip

## Installation

1.  **Clone/Open the project directory:**
    ```bash
    cd "d:\Users\guddu\Complete_DataScience\Generative_AI\Text_to_Speech"
    ```

2.  **Install Dependencies:**
    ```bash
    pip install fastapi uvicorn gtts edge-tts
    ```

## Usage

1.  **Run the Server:**
    ```bash
    uvicorn main_api:app --reload
    ```
    Server runs at `http://127.0.0.1:8000`.

2.  **Access Documentation:**
    -   **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    -   **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

3.  **API Endpoints:**

    ### Google TTS
    -   `POST /gtts/generate`: Generate speech using Google TTS.
        -   Body: `{"text": "...", "lang": "en", "slow": false}`

    ### Microsoft Edge TTS
    -   `POST /edge-tts/generate`: Generate speech using Edge TTS.
        -   Body: `{"text": "...", "voice": "en-US-AriaNeural", "rate": "+0%", "volume": "+0%", "pitch": "+0Hz"}`
    -   `GET /edge-tts/list-voices`: List all available voices and their details.

## Project Structure
-   `main_api.py`: Main application entry point.
-   `routers/`: Directory containing separate logic for each TTS engine.
    -   `gtts.py`: Logic and endpoints for Google TTS.
    -   `edge.py`: Logic and endpoints for Edge TTS.
-   `output/`: Stores generated audio files.
-   `step.txt`: Linear guide to running the project.
