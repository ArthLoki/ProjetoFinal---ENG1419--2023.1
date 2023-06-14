from serial import Serial
from pygame import mixer as mx
from time import sleep
import librosa
from threading import Thread
from calcula_energia_audio import createEnergyList

global audio_duration, audioPlaying

audio_duration = 0
audioPlaying = False

def getAudioDuration(audio_path):
    global audio_duration
    audio_duration = librosa.get_duration(path=audio_path)
    return

def playAudio(mySerial, mx, audio_path):
    global audioPlaying

    audio_pos = 0

    energyList = createEnergyList(audio_path)

    audioPlaying = mx.music.get_busy()
    mixer = mx.get_init()

    mx.music.load(audio_path)
    mx.music.set_volume(0.2)
    mx.music.play()

    i = 0
    while (mixer != None):
        audioPlaying = mx.music.get_busy()
        if (audioPlaying == True): 
            if (mx.music.get_pos() > audio_pos + 50):
                audio_pos = mx.music.get_pos()
                if (i < len(energyList)):
                    energy = energyList[i]
                    
                    # Character 
                    sendCommandViaSerial(mySerial, energy)

                    # Audio
                    text2sendViaSerial = "falando " + str(energyList[i]) + "\n"
                    print("[INFO] Serial: falando " + str(energyList[i]))
                    mySerial.write(text2sendViaSerial.encode("UTF-8"))
                i += 1
        else:
            endAudio(mySerial, mx)
        mixer = mx.get_init()
    return

def endAudio(mySerial, mx):
    text2sendViaSerial = "fim\n"
    print("[INFO] Serial: fim")
    mySerial.write(text2sendViaSerial.encode("UTF-8"))
    # mx.music.pause()
    mx.music.stop()
    mx.quit()
    return

def sendCommandViaSerial(mySerial, energy):
    commandCharacter = "personalidade " + str(energy) + "\n"
    print("[INFO] Serial: personalidade " + str(energy))
    mySerial.write(commandCharacter.encode("UTF-8"))
    return

def mainPlayAudio(mySerial, audio_path):
    # global audio_duration

    # getAudioDuration(audio_path)

    if (mySerial != None):
        mx.init()
        # playAudio(mySerial, mx, audio_path)
        audio_thread = Thread(target = playAudio, args = [mySerial, mx, audio_path])
        audio_thread.start()
        audio_thread.join()
    return

def testing():
    mySerial = Serial("COM8", baudrate=9600, timeout=0.1)
    mainPlayAudio(mySerial, "voiceFiles/answers/answer.mp3")
    return

testing()
