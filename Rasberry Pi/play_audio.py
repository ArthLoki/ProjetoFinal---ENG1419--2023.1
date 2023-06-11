# from pygame import mixer
from serial import Serial
from pygame import time as pytime, mixer as mx
from time import sleep
import librosa
# import os

global mySerial, audio_duration

mySerial = Serial("COM9", baudrate=9600, timeout=0.1)
# mySerial = None

audio_duration = 0

# def observeFolderChanges():
#     return

# def getNewerVoiceFile():
#     return

def getAudioDuration(audio_path):
    return librosa.get_duration(path=audio_path)

def incCounter(audioPlayed):
    global mySerial, audio_duration
    sleep(audio_duration)
    audioPlayed = True
    if (audioPlayed == True):
        text2sendViaSerial = "fim\n"
        print(text2sendViaSerial)
        mySerial.write(text2sendViaSerial.encode("UTF-8"))
        mx.music.pause()
        mx.music.stop()
        mx.quit()

def playAudio(audio_path):
    global mySerial, audio_duration

    try:
        mx.init()
        audioPlayed = False

        mixer = mx.get_init()
        print("music started playing....")
        while (mixer != None):
            mx.music.load(audio_path)
            mx.music.set_volume(0.2)

            if (audioPlayed == False):
                text2sendViaSerial = "falando\n"
                print(text2sendViaSerial)
                mySerial.write(text2sendViaSerial.encode("UTF-8"))

                audio_duration = getAudioDuration(audio_path)
                mx.music.play()
                incCounter(audioPlayed)
            else:
                break
            mixer = mx.get_init()
    except Exception as e:
        print(e)


    # deletes the audio file
    # os.remove(audio_path)
    return

# playAudio('voiceFiles/answers/answer.mp3')
