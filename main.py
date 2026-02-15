from gtts import gTTS
import os

# create folder for store voice

os.makedirs("output", exist_ok = True)

# text = "Hello, how are you?"

text = "जीवाणु एक एककोशिकीय जीव है। इसका आकार कुछ मिलिमीटर तक ही होता है। इनकी आकृति गोल या मुक्त-चक्राकार से लेकर छङा, आदि आकार की हो सकती है।"

# convert text to speech
gtts = gTTS(text = text, lang = "hi")

file_path = "output/hello_hin.mp3"
gtts.save(file_path)

print(f"Voice saved to {file_path}")