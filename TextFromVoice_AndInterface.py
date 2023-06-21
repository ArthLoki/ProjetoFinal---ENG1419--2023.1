from tkinter import *
from tkinter import scrolledtext
import os
from threading import Thread
from generateVoiceFromText_tts import text2voice
import openai
from subprocess import Popen
import whisper
from os import system

global aplicativo
aplicativo = None

janela = Tk()
janela.title("Ice Cream V")

canvas = Canvas(janela, width=450, height=520)
canvas.pack()

global botau1,textobotao1,texto1, tipo, dictTipos, texto_final
botau1 = False
tipo = ''

dictTipos = {'Xuxa': 'xuxa', 'Robo': 'Robo', "Mulher 1": "Mulher 1", "William Bonner": "William Bonner"}

def whisper_func():
    global aplicativo, botau1,textobotao1,texto1, tipo

    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
        
        print("\n\n Parando gravação de áudio...\n\n")
        
        system("ffmpeg -y -i audio.wav -acodec libopus audio.ogg")

        print("\n\n Convertendo o audio em texto: \n\n")
        
        botau1 = False
        textobotao1.destroy()
        
        textobotao1 = Label(janela, text="Processando ...", font=("Arial", 16))
        textobotao1.pack()
        textobotao1.place(x=40, y=70)

        model = whisper.load_model('base')
        audio_file = 'audio.ogg'

        # Iniciar a transcrição do áudio
        transcribe = model.transcribe(audio_file, fp16=False)

        print("\n Resultado: \n")
        # Imprimir a transcrição final completa
        texto_final = transcribe['text']
        print(texto_final, "\n")

    textobotao1.destroy()
    texto1.config(state='normal')    
    texto1.insert(END, texto_final)
    texto1.config(state='disable')
    # openai_thread = Thread(target = text2voice, args = [texto_final, dictTipos[tipo.get()]])
    # openai_thread.start()



def imprimir_mensagem1():
    global botau1,textobotao1,texto1
    if botau1 == False:
        botau1 = True
        textobotao1 = Label(janela, text="Gravando ...", font=("Arial", 16))
        textobotao1.pack()
        textobotao1.place(x=40, y=70)
        texto1.config(state='normal')
        texto1.delete("1.0", END)
        texto1.config(state='disable')
        global aplicativo
        comando = ["ffmpeg", "-y", "-f", "dshow", "-i", "audio=@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{E583998B-419A-4CE4-896B-85202F906BD0}", "-t", "00:30", "audio.wav"]
        aplicativo = Popen(comando)
        print("Iniciando gravação de áudio...\n\n")
    else:
        texto_thread = Thread(target = whisper_func)

        texto_thread.start()


botao1 = Button(janela, text="Gravar", command=imprimir_mensagem1)
botao1.place(x=380, y=22)

personagem = Label(janela, text="Personagem")
personagem.place(x=20, y=20)

tipo = StringVar(value="Robo")  # essa variável vai guardar a opção escolhida pelo usuário
campo_personagem = OptionMenu(janela, tipo, "Xuxa", "Robo","William Bonner","Mulher 1")
campo_personagem.config(width=40)
campo_personagem.place(x=20, y=20)

quadro1 = Frame(janela, width=440, height=180)
quadro1.place(x=20, y=120)

quadro2 = Frame(janela, width=440, height=180)
quadro2.place(x=20, y=320)

texto1 = scrolledtext.ScrolledText(quadro1, wrap=WORD, state='disabled')
texto1.place(x=0, y=0, width=420, height=180)

texto2 = scrolledtext.ScrolledText(quadro2, wrap=WORD, state='disabled')
texto2.place(x=0, y=0, width=420, height=180)

janela.mainloop()