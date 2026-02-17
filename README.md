# VoiceSense Pro - AI Streaming TTS 🚀

VoiceSense Pro is a premium, ultra-fast Text-to-Speech platform featuring real-time streaming and a stunning, high-performance web interface. It combines Microsoft Edge's high-quality neural voices with Google TTS flexibility, optimized for gapless narration.

## 🌟 Key Features
- **Stunning UI/UX**: Premium "Glassmorphism" dashboard with smooth animations and responsive design.
- **Real-Time Streaming**: Audio begins narrating while you type, with ultra-fast WebSocket delivery.
- **Gapless Playback**: Professional Web Audio API scheduler for smooth, continuous speech without stuttering.
- **Delta Narration**: Intelligent tracking that only narrates new text, preventing repetition of previously spoken words.
- **Smart Chunking**: Prioritizes punctuated sentences for perfect intonation while maintaining high-speed live feedback.
- **Organized Storage**: 
    - `output/edge/` & `output/gtts/`: Organized model-specific directories.
    - `output/temp/`: Managed intermediate sentence fragments.
    - Final merged MP3 generation for complete requests.
- **Activity Logging**: Every user input is captured in `logs/inputs.json` for analytics and search.
- **Live Visualizer**: Interactive animated waves that react to the voice stream.

## 🛠️ Technology Stack
- **Backend**: FastAPI (Python)
- **Engines**: Microsoft Edge TTS, Google Translate TTS (gTTS)
- **Frontend**: HTML5, Vanilla CSS3, Web Audio API (JavaScript)
- **Communication**: WebSockets (WS) for binary audio streaming.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- Activated virtual environment (recommended)

### 2. Install Dependencies
```bash
pip install fastapi uvicorn gtts edge-tts websockets
```

### 3. Run the Application
```bash
uvicorn main_api:app --reload
```
Open your browser at: `http://127.0.0.1:8000`

## 📂 Project Structure
- `main_api.py`: Core FastAPI server and static file hosting.
- `index.html`: Premium frontend application logic and Web Audio engine.
- `routers/`:
    - `edge.py`: WebSocket server for real-time Edge/gTTS streaming.
    - `gtts.py`: Standard gTTS generation endpoints.
- `utils.py`: Utility functions for input logging.
- `output/`: Folder for archived and final recordings.
- `logs/`: Application usage history.

## 🎯 Usage Tips
- **Click to Unlock**: Browsers block automatic audio. Click anywhere on the dashboard once to enable the sound engine.
- **Engine Toggling**: Switch between Microsoft and Google engines in the top-right settings.
- **Fast Mode**: Typing a period (`.`) or pause for >300ms triggers instant narration.

---
*Created with ❤️ for high-performance AI narration.*
