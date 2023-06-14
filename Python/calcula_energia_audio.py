# import sounddevice as sd
import numpy as np
import librosa
import time

# Função para calcular a energia do áudio
def calculate_audio_energy(audio_data):
    energy = np.sum((np.abs(audio_data)*100)**2) / len(audio_data)
    return energy

# Função de callback para processar o áudio em tempo real
def audio_callback(data,sample_rate,lista):
    tempo = 0.025
    tempo_max = librosa.get_duration(y=data, sr=sample_rate)
    while(tempo < tempo_max):
        starter_time = tempo - 0.025  # Tempo de início em segundos
        end_time = tempo + 0.025  # Tempo de fim em segundos
        # Converte o intervalo de tempo para amostras
        start_sample = int(starter_time * sample_rate)
        end_sample = int(end_time * sample_rate)
        lista.append(calculate_audio_energy(data[start_sample:end_sample]))
        tempo += 0.05

# Carrega o arquivo de áudio
def createEnergyList(nome_audio):
    energiListy = []
    data, sample_rate = librosa.load(nome_audio)
    #r"C:\Users\micro1\Downloads\audio.wav"
    audio_callback(data,sample_rate,energiListy)
    maior = max(energiListy)
    for i in range(len(energiListy)):
        energiListy[i] = energiListy[i]/maior * 100
    return energiListy

#print(data[start_sample:end_sample])
# Inicia a reprodução do áudio
# last_time = 0
# start_time = time.time()
# with sd.OutputStream(callback=audio_callback, samplerate=sample_rate):
#     sd.play(data, sample_rate)
#     sd.wait()

