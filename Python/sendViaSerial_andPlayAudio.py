from serial import Serial
from pygame import mixer as mx
from time import sleep
from threading import Thread
from calcula_energia_audio import createEnergyList

global audioPlaying
audioPlaying = False

global dictTipos

dictTipos = {'Xuxa': {'nome': 'xuxa', 'idioma': 'portugues br', 'personalidade': 'feliz'}, 
            'Robo': {'nome': 'Robo', 'idioma': 'portugues br', 'personalidade': 'triste'}, 
            "Mulher 1": {'nome': 'Mulher 1', 'idioma': 'portugues br', 'personalidade': 'normal'},
            "William Bonner": {'nome': 'William Bonner', 'idioma': 'portugues br', 'personalidade': 'cansado'},
            "Mario Bros": {'nome': 'mario', 'idioma': 'ingles', 'personalidade': 'feliz'},
            "Darth Vader": {'nome': 'Darth Vader (New, Version 2.0)', 'idioma': 'ingles', 'personalidade': 'zangado'}, 
            "Elizabeth Olsen": {'nome': 'Elizabeth Olsen', 'idioma': 'ingles', 'personalidade': 'triste'},
            "Gato de Botas": {'nome': 'elgatoconbotas', 'idioma': 'espanhol', 'personalidade': 'feliz'}}

def playAudio(mySerial, mx, audio_path, character):
    global audioPlaying, dictTipos

    audio_pos = 0

    energyList = createEnergyList(audio_path)

    audioPlaying = mx.music.get_busy()
    mixer = mx.get_init()

    # Character 
    sendCommandViaSerial(mySerial, dictTipos[character]['personalidade'])

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
                    energy_str = str(int(energy))
                    len_energy_str = len(energy_str)
                    diff = 3 - len_energy_str

                    # Audio
                    text2sendViaSerial = "falando " + (diff * "0") + energy_str + "\n"
                    mySerial.write(text2sendViaSerial.encode("UTF-8"))

                    # serial_thread = Thread(target=getFromSerial, args = [mySerial])
                    # serial_thread.daemon = True
                    # serial_thread.start()

                    if (i >= len(energyList)):
                        endAudio(mySerial, mx)
                        break

                i += 1
        # else:
        #     endAudio(mySerial, mx)
        #     # text2sendViaSerial = "fim\n"
        #     # mySerial.write(text2sendViaSerial.encode("UTF-8"))
        #     # mx.music.stop()
        #     # mx.quit()
        #     break

        mixer = mx.get_init()
    return

def endAudio(mySerial, mx):
    text2sendViaSerial = "fim\n"
    mySerial.write(text2sendViaSerial.encode("UTF-8"))
    mx.music.stop()
    mx.quit()
    return

def sendCommandViaSerial(mySerial, characterPersonality):
    commandCharacter = "personalidade " + characterPersonality + "\n"
    mySerial.write(commandCharacter.encode("UTF-8"))
    return


def getFromSerial(mySerial):
    # while True:
    if mySerial != None:
        textReceived = mySerial.readline().decode().strip()
        print("Texto recebido pela Serial: ", textReceived)
    sleep(0.1)

def mainPlayAudio(mySerial, audio_path, character):
    if (mySerial != None):
        mx.init()
        audio_thread = Thread(target = playAudio, args = [mySerial, mx, audio_path, character])
        audio_thread.start()
        audio_thread.join()

    return

# def testing():
#     mySerial = Serial("COM12", baudrate=9600, timeout=0.1)
#     audio_path = "voiceFiles/answers/answer.mp3"
#     mainPlayAudio(mySerial, audio_path, 'Robo')
#     return

# testing()
