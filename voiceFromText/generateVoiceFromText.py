# from openai.connect_openai import call_gpt
from gtts import gTTS
import pyttsx3
import fakeyou
import tempfile
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("USER_FAKEYOU")
password = os.getenv("PASSWORD_FAKEYOU")

fy = fakeyou.FakeYou()
fy.login(username,password)

'''
OPÇÕES DE TEXT TO SPEECH (TTS):

1. Google Text to Speech (gtts)
2. pyttsx3
3. CoquiTTS
4. FakeYou (https://fakeyou.com)
'''

def get_tts_token(model_name):
    voices = fy.list_voices()

    json_data = []

    for json_archive in zip(voices.json):
        json_data.append(json_archive[0])

    for i in range(len(json_data)):
        data = json_data[i]
        if (data['ietf_primary_language_subtag'] == 'pt'):
            if (model_name.lower() == data['title'] or model_name.lower() == data['maybe_suggested_unique_bot_command']):
                return data['model_token']
    return ''

def getFilePathFakeyou(model_name):
    # base path
    base = 'voiceFiles/fakeyou/'

    # filename
    lNames = model_name.split(' ')
    filename = ''
    for i in range(len(lNames)):
        if i < len(lNames) - 1:
            filename += (lNames[i].lower() + '_')
        else:
            filename += (lNames[i].lower() + '.wav')

    filePath = base + filename
    return filePath

def getVoice_fakeyou(responseChatGPT, model_name):
    try:
        temp_file = tempfile.mkdtemp()
        filename = os.path.join(temp_file, model_name.lower() + '.wav')
        tts_model_token = get_tts_token(model_name)
        # print(tts_model_token)
        if tts_model_token != '':
            fy.say(text="It's a me, Mario!", ttsModelToken=tts_model_token)
            # fy.say(text=responseChatGPT,ttsModelToken=tts_model_token, filename=filename)
            print("Voz salva\n")
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
    engine.setProperty('voice', voices[2].id)

    ## Save into a file
    engine.save_to_file(responseChatGPT, 'voiceFiles/person/person.mp3')

    ## DO NOT DELETE
    engine.runAndWait()

    return

def getVoice_gtts(responseChatGPT):
    tts = gTTS(text=responseChatGPT, lang='pt')
    tts.save("voiceFiles/robot/robot.mp3")
    return

def text2voice(prompt):

    # get text answer from chatGPT
    # respostaChatGPT = call_gpt(prompt)

    responseChatGPT = "Olá mundo"

    # convert text to voice
    getVoice_fakeyou(responseChatGPT, 'xuxa')

    # getVoiceTextToSpeech(responseChatGPT)

    # getVoice_pyttsx3(responseChatGPT)

    # getVoice_gtts(responseChatGPT)


    return

def testeText2VoiceSemPrompt():
    text2voice('')
    return

testeText2VoiceSemPrompt()
