import pyttsx3
import os
import sys

def main() -> None:
    try:
        # create output directory if not exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok = True)

        # initialize tts engine
        engine = pyttsx3.init()

        # get available voices
        voices = engine.getProperty("voices")

        # select voice (0 = Hazel UK, 1 = Zira US)
        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)
        else:
            engine.setProperty("voices", voices[0].id)

        # set speech rate (default ~ 200)
        engine.setProperty("rate", 170)

        # set volume (0.0 to 1.0)
        engine.setProperty("volume", 1.0)

        # text to speech convert
        text = "Hello Guddu, this is high quality neural text to speech conversion running with GPU"
       
        # output file path
        output_path = os.path.join(output_dir, "pyttsx3_output.mp3")

        # execute speech engine
        engine.runAndWait()

        print(f"file saved successfully at: {output_path}")

    except Exception as e:
        print("error occurred:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()