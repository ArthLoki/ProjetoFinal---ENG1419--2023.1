from pygame import mixer

def observeFolderChanges():
    return

def getNewerVoiceFile():
    return

def playAudio(audio):
    mixer.init()
    mixer.music.load("voiceFiles/" + audio)
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return