'''
OPÇÕES DE TEXT TO SPEECH (TTS):

1. Google Text to Speech (gtts)
2. pyttsx3
3. FakeYou (https://fakeyou.com)
'''

# from connect_openai import call_gpt
from gtts import gTTS
import pyttsx3
import fakeyou.objects as objects
import fakeyou
from dotenv import load_dotenv
import os
import requests, json
from pyhelpers.ops import is_downloadable

load_dotenv()

username = os.getenv("USER_FAKEYOU")
password = os.getenv("PASSWORD_FAKEYOU")

fy = fakeyou.FakeYou(verbose=True)
fy.login(username, password)


# 1. gtts (OK)
def getVoice_gtts(responseChatGPT):
    tts = gTTS(text=responseChatGPT, lang='pt')
    tts.save("voiceFiles/robot/robot.mp3")
    return

# 2. pyttsx3 (OK)
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

# 3. Fakeyou (NOT OK)
def get_tts_token(model_name):  # OK!
    voices = fy.list_voices()

    json_data = []

    for json_archive in zip(voices.json):
        json_data.append(json_archive[0])

    for i in range(len(json_data)):
        data = json_data[i]
        # if (data['ietf_primary_language_subtag'] == 'pt'):
        if (model_name.lower() == data['title'] or model_name.lower() == data['maybe_suggested_unique_bot_command']):
            return data['model_token']
    return ''


def get_model_name(tts_model_token):
    voices = fy.list_voices()

    json_data = []

    for json_archive in zip(voices.json):
        json_data.append(json_archive[0])

    for i in range(len(json_data)):
        data = json_data[i]
        if (tts_model_token == data['model_token']):
            return data['title']
    return ''


def format_model_name(tts_model_token):
    model_name = get_model_name(tts_model_token)
    if "(" in model_name and ")" in model_name:
        model_name.replace("(", ' ')
        model_name.replace(")", ' ')

    if ' ' in model_name:
        lComp = model_name.split(' ')

    new_model_name = 'fakeyou_'
    for i in range(len(lComp)):
        if (i < len(lComp) - 1):
            new_model_name += (lComp[i] + '_')
        else:
            new_model_name += lComp[i]

    return new_model_name


def getFilePathFakeyou():  # OK!
    # current path
    current_path = (os.getcwd()).replace('\\', '/')

    # base path
    complement = 'voiceFiles/fakeyou/'

    # filePath
    return current_path + '/' + complement


def getVoice_fakeyou(responseChatGPT, tts_model_token):  # It doesn't work
    try:
        fy.say(text="It's a me, Mario!", ttsModelToken=tts_model_token)
        # fy.say(text=responseChatGPT,ttsModelToken=tts_model_token)

        # get required data
        inference_job_token = fy.make_tts_job(responseChatGPT, tts_model_token)
        url_wav_data = "https://api.fakeyou.com/tts/job/" + inference_job_token

        # request data from url
        request_wav_data = requests.get(url_wav_data)

        # generate a json file
        json_file = request_wav_data.json()
        print(json_file)

        while (json_file['state']['status'] != 'complete_success'):
            print(json_file['state']['status'])
            if (json_file['state']['status'] == 'complete_success'):
                # tentativa 1
                print(json_file['state']['status'])
                objects.wav(json_file)

                # path = getFilePathFakeyou()
                objects.wav.save(os.getcwd())  # problem
            else:
                request_wav_data = requests.get(url_wav_data)
                json_file = request_wav_data.json()
    except fakeyou.exception.TooManyRequests:
        print("Cool down")
    return

# Conversion according to the question and chosen character
def text2voice(prompt, character):

    # get text response from chatGPT
    # responseChatGPT = call_gpt(prompt)
    responseChatGPT = "Olá mundo"

    # convert text to voice
    if (character == 'robo'):
        getVoice_gtts(responseChatGPT)
    elif (character == 'pessoa'):
        getVoice_pyttsx3(responseChatGPT)
    else:
        # get tts_model_token
        tts_model_token = get_tts_token(character)

        # compare to empty string
        if (tts_model_token != ''):
            getVoice_fakeyou(responseChatGPT, tts_model_token)
        else:
            print("Modelo de voz não encontrado")
    return

# Testing
text2voice('','mario')