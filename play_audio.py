# from pygame import mixer
import pygame
import os

def observeFolderChanges():
    return

def getNewerVoiceFile():
    return

def playAudio(audio_path):
    # # init mixer
    # mixer.init()

    # # load audio
    # mixer.music.load(audio_path)

    # # set volume
    # mixer.music.set_volume(0.7)

    # # play audio
    # mixer.music.play()

    pygame.init()
    sound = pygame.mixer.Sound("desert_rustle.wav")
    pygame.mixer.Sound.play(sound)

    # deletes the audio file after it's played
    # os.remove(audio_path)
    return
