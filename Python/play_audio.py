# from pygame import mixer
# from serial import Serial
from pygame import mixer as mx
from time import sleep
import librosa
# import os

global audio_duration

audio_duration = 0

def getAudioDuration(audio_path):
    return librosa.get_duration(path=audio_path)

def incCounter(mySerial, audioPlayed):
    global audio_duration
    sleep(audio_duration)
    audioPlayed = True
    if (audioPlayed == True):
        text2sendViaSerial = "fim\n"
        print("[INFO] Serial: fim")
        mySerial.write(text2sendViaSerial.encode("UTF-8"))
        mx.music.pause()
        mx.music.stop()
        mx.quit()

def playAudio(mySerial, audio_path):
    global audio_duration

    if (mySerial != None):
        # print("[INFO] Serial: OK")

        try:
            mx.init()
            mixer = mx.get_init()

            audioPlayed = False

            while (mixer != None):
                mx.music.load(audio_path)
                mx.music.set_volume(0.2)

                if (audioPlayed == False):
                    text2sendViaSerial = "falando\n"
                    print("[INFO] Serial: falando")
                    mySerial.write(text2sendViaSerial.encode("UTF-8"))

                    audio_duration = getAudioDuration(audio_path)
                    mx.music.play()
                    incCounter(mySerial, audioPlayed)
                else:
                    break

                mixer = mx.get_init()
        except Exception as e:
            print(e)
    return
