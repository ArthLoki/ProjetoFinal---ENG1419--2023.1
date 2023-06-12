# from serial import Serial
from time import sleep


global energyList, dictCharacterServoInfo

dictCharacterServoInfo = {'Xuxa': {'boca': 100, "sobrancelha": 60}, 
                        'Robo': {'boca': 20, "sobrancelha": 5}, 
                        "Mulher 1": {'boca': 50, "sobrancelha": 20}, 
                        "William Bonner": {'boca': 80, "sobrancelha": 30}}

def sendCommandViaSerial(mySerial, character):
    global dictCharacterServoInfo

    if (mySerial != None):
        print("[INFO] Serial: OK")

        # Character
        commandEyebrowValue = dictCharacterServoInfo[character]['sobrancelha']
        commandEyebrowValueLenDiff = 3 - len(str(commandEyebrowValue))
        commandCharacter = "personalidade " + (commandEyebrowValueLenDiff * "0") + str(commandEyebrowValue) + "\n"
        print("[INFO] Serial: personalidade " + (commandEyebrowValueLenDiff * "0") + str(commandEyebrowValue))

        # Mouth
        commandMouthValue = dictCharacterServoInfo[character]['boca']
        commandMouthValueLenDiff = 3 - len(str(commandMouthValue))
        commandMouth = "boca " + (commandMouthValueLenDiff * "0") + str(commandMouthValue) + "\n"
        print("[INFO] Serial: boca " + (commandMouthValueLenDiff * "0") + str(commandMouthValue))

        try:
            mySerial.write(commandCharacter.encode("UTF-8"))
            mySerial.write(commandMouth.encode("UTF-8"))
        except Exception as e:
            print(e)
    return
