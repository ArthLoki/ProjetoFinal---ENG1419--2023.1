from tkinter import *
from tkinter import scrolledtext
from subprocess import Popen, PIPE, run
import os
from threading import Thread
from generateVoiceFromText_tts import text2voice, getResponseChatGPT
import whisper
from os import system
#from DeteccaoDeRostos import streaming, deteccao
import cv2
import math

# Serial
from serial import Serial

global aplicativo
aplicativo = None

janela = Tk()
janela.title("Ice Cream IV")

canvas = Canvas(janela, width=450, height=520)
canvas.pack()

global botau1,textobotao1,texto1, tipo, dictTipos, texto_final, respostaChatGPT
botau1 = False
tipo = ''
respostaChatGPT = ''

dictTipos = {"Robo": {'nome': 'Robo', 'idioma': 'portugues br', 'especificacao': '', 'personalidade': 'triste'},
             "Mulher 1": {'nome': 'Mulher 1', 'idioma': 'portugues br', 'especificacao': '','personalidade': 'normal'},
             "Mario Bros": {'nome': 'mario', 'idioma': 'ingles', 'especificacao': 'do jogo Super Mario','personalidade': 'feliz'},
             "Darth Vader": {'nome': 'Darth Vader (New, Version 2.0)', 'idioma': 'ingles', 'especificacao': 'dos filmes de Star Wars','personalidade': 'zangado'},
             "Feiticeira Escarlate": {'nome': 'Elizabeth Olsen', 'idioma': 'ingles', 'especificacao': 'da marvel nao explique o contexto', 'personalidade': 'triste'},
             "Donald Trump": {'nome': 'angrydonaldtrump', 'idioma': 'ingles', 'especificacao': 'utilizando o mesmo tipo de discurso que ele utiliza nos discursos', 'personalidade': 'zangado'},
             "Gato de Botas": {'nome': 'elgatoconbotas', 'idioma': 'espanhol', 'especificacao': '', 'personalidade': 'feliz'}}


global dic
dic = {}
dic['x'] = 0
dic['y'] = 0
dic['w'] = 0
dic['h'] = 0

global iteracoes
iteracoes = 0

global imagem
imagem = 0
global faces
faces = []

# Serial variable
global mySerial
mySerial = Serial("COM12", baudrate=115200, timeout=0.1)
# mySerial = None

def atualiza_valores(x,y,w,h):
    global x_novo, y_novo, w_novo, h_novo       
    x_novo = x
    y_novo = y
    w_novo = w
    h_novo = h
    
def streaming():
    
    global x_novo, y_novo, w_novo, h_novo
    global imagem, faces, dic, iteracoes
    global mySerial
    
    stream = cv2.VideoCapture(0)
    
    while True:
        
        _, imagem = stream.read()

        # Carregar o classificador Haar Cascade pré-treinado para detecção de faces
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Carregar a imagem em escala de cinza
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        # Realizar a detecção de faces na imagem
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        dist = 1000
        x_novo = dic['x']
        y_novo = dic['y']
        w_novo = dic['w']
        h_novo = dic['h']
        
        # Iterar sobre as faces detectadas
        for (x, y, w, h) in faces:
            
            #calculando o centro da face da ultima posicao
            centro_x1 = dic['x'] + (dic['w'] // 2)
            centro_y1 = dic['y'] + (dic['h'] // 2)
            #calculando o centro da face da posicao atual
            centro_x2 = x + (w // 2)
            centro_y2 = y + (h // 2)
            #comparando a distancia entre os centros para ver se esta perto
            distancia = math.sqrt((centro_x2 - centro_x1)**2 + (centro_y2 - centro_y1)**2)

            #guardando a menor distancia e os valores associados a ela
            if distancia < dist:
                #controlando possiveis "piscadas"
                if distancia>100:
                    iteracoes = iteracoes + 1
                    if iteracoes>20:
                        dist = distancia
                        atualiza_valores(x,y,w,h)
                        iteracoes = 0
                else:
                    dist = distancia
                    atualiza_valores(x,y,w,h)

        if (cv2.waitkey(1) & 0xFF == ord("q")):
            break

        #guardando no dicionario
        dic['x'] = x_novo
        dic['y'] = y_novo
        dic['w'] = w_novo
        dic['h'] = h_novo
        
        #calculando o angulo
        centro_x = dic['x'] + (dic['w'] / 2)
        largura_tela = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        centro_da_tela = largura_tela//2
        angulo = (90*centro_x)/centro_da_tela
        angulo_str = str(int(180 - angulo))
        diff = 3 - len(angulo_str)
        textSerialAngulo = "olho " + (diff * "0") + angulo_str + "\n"
        mySerial.write(textSerialAngulo.encode("UTF-8"))

def deteccao():
    global imagem, faces

    copia = imagem    
    
    for (x, y, w, h) in faces:
        if (x,y,w,h):
            cv2.rectangle(copia, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow("Minha Janela", copia)

    # if (waitkey(1) & 0xFF == ord("q")):
    #     break
    #cv2.waitKey(1)
    #cv2.destroyAllWindows()


def chamando_streaming():
    deteccao()
    janela.after(50, chamando_streaming)
    
def tudo_func():
    global aplicativo, botau1,textobotao1,texto1, tipo
    global mySerial

    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
        
        print("\n\n Parando gravação de áudio...\n\n")
        
        system("ffmpeg -y -i voiceFiles/questions/question.wav -acodec libopus voiceFiles/questions/question.ogg")

        print("\n\n Convertendo o audio em texto: \n\n")
        
        botau1 = False
        textobotao1.destroy()
        
        textobotao1 = Label(janela, text="Processando ...", font=("Arial", 16))
        textobotao1.pack()
        textobotao1.place(x=40, y=70)

        model = whisper.load_model('base')
        # audio_file = 'voiceFiles/questions/question.ogg'
        audio_file = 'audio.wav'

        # Iniciar a transcrição do áudio
        transcribe = model.transcribe(audio_file, fp16=False)

        print("\n Resultado: \n")
        # Imprimir a transcrição final completa
        texto_final = transcribe['text']
        print(texto_final, "\n")

    textobotao1.destroy()
    texto1.insert(END, texto_final)
    if tipo.get() != "Robo":
        texto_final = "Responda a mensagem a seguir fingindo ser {} falando no idioma {}. Lembrando não sai do seu papel de interpretar {}.".format(tipo.get(),dictTipos[tipo.get()]['especificacao'],dictTipos[tipo.get()]['idioma'],tipo.get()) + texto_final
    respostaChatGPT = getResponseChatGPT(texto_final)
    texto2.config(state='normal')    
    texto2.insert(END, respostaChatGPT)
    texto2.config(state='disable')
    openai_thread = Thread(target = text2voice, args = [mySerial, respostaChatGPT, dictTipos[tipo.get()]['nome']])
    openai_thread.start()

def whisper_func():
    global aplicativo, botau1,textobotao1,texto1, tipo

    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
        
        print("\n\n Parando gravação de áudio...\n\n")
        
        system("ffmpeg -y -i voiceFiles/questions/question.wav -acodec libopus voiceFiles/questions/question.ogg")

        print("\n\n Convertendo o audio em texto: \n\n")
        
        botau1 = False
        textobotao1.destroy()
        
        textobotao1 = Label(janela, text="Processando ...", font=("Arial", 16))
        textobotao1.pack()
        textobotao1.place(x=40, y=70)

        model = whisper.load_model('base')
        # audio_file = 'voiceFiles/questions/question.ogg'
        audio_file = 'audio.wav'

        # Iniciar a transcrição do áudio
        transcribe = model.transcribe(audio_file, fp16=False)

        print("\n Resultado: \n")
        # Imprimir a transcrição final completa
        texto_final = transcribe['text']
        print(texto_final, "\n")

    textobotao1.destroy()    
    texto1.insert(END, texto_final)
    

def resposta():
    global mySerial

    texto_final = texto1.get("1.0", END)
    print(texto_final)
    if tipo.get() != "Robo":
        texto_final = "Responda a mensagem a seguir fingindo ser {} falando no idioma {}. Lembrando não sai do seu papel de interpretar {}.".format(tipo.get(),dictTipos[tipo.get()]['especificacao'],dictTipos[tipo.get()]['idioma'],tipo.get()) + texto_final
    respostaChatGPT = getResponseChatGPT(texto_final)
    texto2.config(state='normal')
    texto2.delete("1.0", END)
    texto2.config(state='disable')
    texto2.config(state='normal')    
    texto2.insert(END, respostaChatGPT)
    texto2.config(state='disable')
    
def voz_resposta():
    respostaChatGPT = texto2.get("1.0", END)
    openai_thread = Thread(target = text2voice, args = [mySerial, respostaChatGPT, dictTipos[tipo.get()]['nome']])
    openai_thread.start()
    
    
def imprimir_mensagem1():
    global botau1,textobotao1,texto1
    if botau1 == False:
        botau1 = True
        textobotao1 = Label(janela, text="Gravando ...", font=("Arial", 16))
        textobotao1.pack()
        textobotao1.place(x=40, y=70)
        texto1.delete("1.0", END)
        global aplicativo
        comando = ["ffmpeg", "-y", "-f", "dshow", "-i", "audio=Microphone (Synaptics SmartAudio HD)", "-t", "00:30", "voiceFiles/questions/question.wav"]  # Microfone Luiza: Microfone (Synaptics SmartAudio HD)
        aplicativo = Popen(comando)
        print("Iniciando gravação de áudio...\n\n")
    else:
        texto_thread = Thread(target = whisper_func)
        texto_thread.start()
        
def imprimir_tudo1():
    global botau1,textobotao1,texto1
    if botau1 == False:
        botau1 = True
        textobotao1 = Label(janela, text="Gravando ...", font=("Arial", 16))
        textobotao1.pack()
        textobotao1.place(x=40, y=70)
        texto1.delete("1.0", END)
        global aplicativo
        comando = ["ffmpeg", "-y", "-f", "dshow", "-i", "audio=Microphone (Synaptics SmartAudio HD)", "-t", "00:30", "audio.wav"]  # Microfone Luiza: Microfone (Synaptics SmartAudio HD)
        aplicativo = Popen(comando)
        print("Iniciando gravação de áudio...\n\n")
    else:
        texto_thread = Thread(target = tudo_func)
        texto_thread.start()

botao0 = Button(janela, text="Tudo", command=imprimir_tudo1)
botao0.place(x=335, y=22)

botao1 = Button(janela, text="Gravar", command=imprimir_mensagem1)
botao1.place(x=280, y=52)

botao2 = Button(janela, text="ChatGPT", command=resposta)
botao2.place(x=380, y=52)

botao3 = Button(janela, text="Voz", command=voz_resposta)
botao3.place(x=340, y=52)

personagem = Label(janela, text="Personagem")
personagem.place(x=20, y=20)

tipo = StringVar(value="Robo")  # essa variável vai guardar a opção escolhida pelo usuário
campo_personagem = OptionMenu(janela, tipo, "Robo","Mulher 1", "Mario Bros", "Darth Vader","Feiticeira Escarlate","Donald Trump","Gato de Botas")
campo_personagem.config(width=40)
campo_personagem.place(x=20, y=20)

quadro1 = Frame(janela, width=440, height=180)
quadro1.place(x=20, y=120)

quadro2 = Frame(janela, width=440, height=180)
quadro2.place(x=20, y=320)

texto1 = scrolledtext.ScrolledText(quadro1, wrap=WORD, state='normal')
texto1.place(x=0, y=0, width=420, height=180)

texto2 = scrolledtext.ScrolledText(quadro2, wrap=WORD, state='disabled')
texto2.place(x=0, y=0, width=420, height=180)

deteccao_thread = Thread(target = streaming)
#deteccao_thread.daemon = True
deteccao_thread.start() 

chamando_streaming()

janela.mainloop()
