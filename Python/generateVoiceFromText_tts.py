'''
OPÇÕES DE TEXT TO SPEECH (TTS):

1. Google Text to Speech (gtts)
2. pyttsx3
3. FakeYou (https://fakeyou.com)
'''

# Openai
from connect_openai import call_gpt

# TTS
from gtts import gTTS
import pyttsx3
import fakeyou

# Download speech
import requests

# Get Enviroment Variables
from dotenv import load_dotenv
import os

# Serial + playAudio
from serial import Serial
# from play_audio import playAudio
from sendViaSerial_andPlayAudio import mainPlayAudio

# Global variables
load_dotenv()
username = os.getenv("USER_FAKEYOU")
password = os.getenv("PASSWORD_FAKEYOU")

fy = fakeyou.FakeYou(verbose=True)
fy.login(username, password)

# Functions
# 1. gtts
def getVoice_gtts(responseChatGPT):
    tts = gTTS(text=responseChatGPT, lang='pt')
    tts.save("voiceFiles/answers/answer.mp3")
    return

# 2. pyttsx3
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
    engine.save_to_file(responseChatGPT, 'voiceFiles/answers/answer.mp3')

    ## DO NOT DELETE
    engine.runAndWait()
    return

# 3. Fakeyou
def get_tts_token(model_name):
    voices = fy.list_voices()

    json_data = []

    for json_archive in zip(voices.json):
        json_data.append(json_archive[0])

    for i in range(len(json_data)):
        data = json_data[i]
        if (data['ietf_primary_language_subtag'] == 'pt'):
            if (model_name.lower() == data['title'].lower() or model_name.lower() == data['maybe_suggested_unique_bot_command']):
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


def getFilePathFakeyou():
    # current path
    current_path = (os.getcwd()).replace('\\', '/')

    # base path
    complement = '/voiceFiles/answers/'

    # filePath
    return current_path + complement

def downloadVoiceFromFakeyou(responseChatGPT, tts_model_token):
    try:
        # get required data
        inference_job_token = fy.make_tts_job(responseChatGPT, tts_model_token)
        url_wav_data = "https://api.fakeyou.com/tts/job/" + inference_job_token

        # request data from url
        request_wav_data = requests.get(url_wav_data)

        # generate a json file
        json_file = request_wav_data.json()

        while (json_file['state']['status'] != 'complete_success'):
            request_wav_data = requests.get(url_wav_data)
            json_file = request_wav_data.json()

        # get url to download file
        wav_url_base = 'https://storage.googleapis.com/vocodes-public'
        maybe_public_bucket_wav_audio_path = json_file['state']['maybe_public_bucket_wav_audio_path']

        wav_url = wav_url_base + maybe_public_bucket_wav_audio_path

        try:
            # get filename
            # filename = format_model_name(tts_model_token)

            # download wav file
            wav_file = requests.get(wav_url)
            print(wav_file)
            path = getFilePathFakeyou() + 'answer.wav'
            with open(path, 'wb') as f:
                f.write(wav_file.content)

            print("Voz salva\n")

        except Exception as e:
            print(e)
    except Exception as e1:
        print(e1)
    return

def getVoice_fakeyou(responseChatGPT, tts_model_token):
    try:
        fy.say(text=responseChatGPT,ttsModelToken=tts_model_token)
        downloadVoiceFromFakeyou(responseChatGPT, tts_model_token)
    except fakeyou.exception.TooManyRequests:
        print("Cool down")
    return

# Conversion according to the question/prompt and chosen character
def text2voice(responseChatGPT, character):

    # Serial variable
    mySerial = Serial("COM5", baudrate=9600, timeout=0.1)
    # mySerial = None

    # convert text to voice
    if (character == 'Robo'):
        getVoice_gtts(responseChatGPT)
        audio_path = 'voiceFiles/answers/answer.mp3'
        mainPlayAudio(mySerial, audio_path)
    elif (character == 'Mulher 1'):
        getVoice_pyttsx3(responseChatGPT)
        audio_path = 'voiceFiles/answers/answer.mp3'
        mainPlayAudio(mySerial, audio_path)
    else:
        # get tts_model_token
        tts_model_token = get_tts_token(character)

        # compare to empty string
        if (tts_model_token != ''):
            getVoice_fakeyou(responseChatGPT, tts_model_token)
            audio_path = 'voiceFiles/answers/answer.wav'
            mainPlayAudio(mySerial, audio_path)
        else:
            print("Modelo de voz não encontrado")
    return

# Get response to show in tkinter
def getResponseChatGPT(prompt):
    responseChatGPT = call_gpt(prompt)
    return responseChatGPT
