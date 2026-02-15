import asyncio
import edge_tts
import os

async def generate_audio() -> None:
    os.makedirs("output", exist_ok = True)

    text = "Hello Guddu, this is high quality neural text to speech conversion running with GPU"

    
    # communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    communicate = edge_tts.Communicate(text, "hi-in-NeelamNeural")
    await communicate.save("output/edge_hello_hin.mp3")

    print("Audio generate successfully!")

asyncio.run(generate_audio())