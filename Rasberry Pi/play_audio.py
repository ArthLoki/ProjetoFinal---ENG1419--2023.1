# from pygame import mixer
from serial import Serial
import pygame
import os

global mySerial, audioPlaying

mySerial = Serial("COM9", baudrate=9600, timeout=0.1)
# mySerial = None

audioPlaying = 0  # 0 para False e 1 para True

def observeFolderChanges():
    return

def getNewerVoiceFile():
    return

def playAudio(audio_path):
    global mySerial, audioPlaying

    # # init mixer
    # mixer.init()

    # # load audio
    # mixer.music.load(audio_path)

    # # set volume
    # mixer.music.set_volume(0.7)

    # # play audio
    # mixer.music.play()

    try:
        pygame.init()
        sound = pygame.mixer.Sound("desert_rustle.wav")
        pygame.mixer.Sound.play(sound)

        audioPlaying = 1
        text2sendViaSerial = "falando"
    except Exception as e:
        audioPlaying = 0
        text2sendViaSerial = "silencio"
        print(e)

    mySerial.write(text2sendViaSerial.encode("UTF-8"))


    # deletes the audio file
    # os.remove(audio_path)
    return
