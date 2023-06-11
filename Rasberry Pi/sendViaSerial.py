from serial import Serial
from threading import Thread
from time import sleep


global mySerial, dictCharacterServoInfo, energyList

mySerial = Serial("COM9", baudrate=9600, timeout=0.1)
# mySerial = None

print("[INFO] Serial: OK")

dictCharacterServoInfo = {'Xuxa': {'boca': 100}, 'Robo': {'boca': 20}, "Mulher 1": {'boca': 50}, "William Bonner": {'boca': 80}}

def sendCommandViaSerial(character):
    global mySerial, dictCharacterServoInfo

    if (mySerial != None):
        commandCharacter = "personalidade " + character
        mySerial.write(commandCharacter.encode("UTF-8"))

        commandMouthValue = dictCharacterServoInfo[character]['boca']
        if (commandMouthValue < 10):
            commandMouth = "boca 00" + commandMouthValue
        elif (commandMouthValue < 100):
            commandMouth = "boca 0" + commandMouthValue
        mySerial.write(commandMouth.encode("UTF-8"))
    return

def mainSerial(character):
    thread = Thread(target = sendCommandViaSerial, args = [character])
    thread.daemon = True
    thread.start()
    return
