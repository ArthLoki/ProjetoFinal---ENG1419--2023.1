# from openai.connect_openai import call_gpt
from gtts import gTTS
import pyttsx3
import fakeyou
from dotenv import load_dotenv
import os
import requests, json

load_dotenv()

username = os.getenv("USER_FAKEYOU")
password = os.getenv("PASSWORD_FAKEYOU")

'''
OPÇÕES DE TEXT TO SPEECH (TTS):

1. Google Text to Speech (gtts)
2. pyttsx3
3. CoquiTTS
4. FakeYou (https://fakeyou.com)
'''

def getAudioFromFakeyou(requests):
    response = requests.get('https://fakeyou.com/profile/' + username, auth=('username', 'password'))
    return

def getVoice_fakeyou(responseChatGPT):
    fy=fakeyou.FakeYou(verbose=False)
    fy.login(username,password)

    # voices=fy.list_voices(size=100)

    # for title,creator in zip(voices.title,voices.creatorUsername):
    #     # if ("Brazilian Portuguese" in title):
    #     print(title,creator)


    # categories=fy.list_voice_categories()

    # for name,token in zip(categories.name,categories.categoryToken):
    #     print(name,token)

    try:
        # fy.say(text=responseChatGPT,ttsModelToken="TM:7wbtjphx8h8v")
        fy.say(text="It's a me, Mario!",ttsModelToken="TM:7wbtjphx8h8v")
    except fakeyou.exception.TooManyRequests:
        print("Cool down")
    return

def getVoice_pyttsx3(responseChatGPT):
    engine = pyttsx3.init()

    """RATE"""
    engine.setProperty('rate', 200)

    """VOLUME"""
    engine.setProperty('volume', 1.0)

    """VOICE"""
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    ## Save into a file
    engine.save_to_file(responseChatGPT, 'voiceFiles/person/person.mp3')

    ## DO NOT DELETE
    engine.runAndWait()

    return

def getVoice_gtts(responseChatGPT):
    tts = gTTS(text=responseChatGPT, lang='en')
    tts.save("voiceFiles/robot/robot.mp3")
    return


def text2voice(prompt):

    # get text answer from chatGPT
    # respostaChatGPT = call_gpt(prompt)

    responseChatGPT = "Hello World"

    # convert text to voice
    getVoice_fakeyou(responseChatGPT)

    getVoice_pyttsx3(responseChatGPT)

    getVoice_gtts(responseChatGPT)


    return

def testeText2VoiceSemPrompt():
    text2voice('')
    return


testeText2VoiceSemPrompt()