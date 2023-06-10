from tkinter import *
from subprocess import Popen, PIPE, run
import os

global aplicativo
aplicativo = None

root = Tk()               
root.geometry('200x200')

def iniciar_gravacao():
    global aplicativo

    comando = ["ffmpeg", "-y", "-f", "dshow", "-i", "audio=@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{E583998B-419A-4CE4-896B-85202F906BD0}", "-t", "00:30", "audio.wav"]
    aplicativo = Popen(comando)
    print("Iniciando gravação de áudio...\n\n")
    
def parar_gravacao():
    global aplicativo

    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
        
        print("\n\n Parando gravação de áudio...\n\n")
        
        root.destroy()
        
        print("\n\n Convertendo o audio em texto: \n\n")

        os.system("pip install -U openai-whisper")
        os.system("start ffmpeg.exe")
        def out(command):
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            return result.stdout

        texto = out("whisper audio.wav --model medium")
        num_timeStamps = texto.count(']')
        texto_final = ""
        for i in range(num_timeStamps):
            indice_inicial = texto.find(']')
            indice_final = texto[indice_inicial:].find('\n')
            texto_final += texto[indice_inicial+1:indice_final+indice_inicial]
            texto = texto[indice_final+indice_inicial+1:]

        print("\n Resultado: \n")
        print(texto_final)

btn = Button(root, text = 'Clique para gravar', bg = 'red', command = iniciar_gravacao)  
btn.place(x=50, y=50)
btn2 = Button(root, text = 'Clique para parar', bg = 'black', fg = 'white', command = parar_gravacao)  
btn2.place(x=50, y=90)

    
root.mainloop()




