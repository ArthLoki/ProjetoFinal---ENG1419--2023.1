from openai.connect_openai import call_gpt
from gtts import gTTS

def text2voice(prompt):
    respostaChatGPT = call_gpt(prompt)
    tts = gTTS(text=respostaChatGPT, lang='pt')
    tts.save("voices/respostaChatGPT.mp3")
    return