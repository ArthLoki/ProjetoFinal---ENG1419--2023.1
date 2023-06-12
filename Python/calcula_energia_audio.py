import sounddevice as sd
import numpy as np
import librosa
import time

# Função para calcular a energia do áudio
def calculate_audio_energy(audio_data):
    energy = np.sum((np.abs(audio_data)*100) ** 2) / len(audio_data)
    return energy

# Função de callback para processar o áudio em tempo real
def audio_callback(indata, frames, tempo, status):
    global start_time,data,sample_rate,last_time

    current_time = time.time() - start_time

    if current_time > last_time + 0.1 and len(data) >= int((current_time + 0.05) * sample_rate):
        print("Tempo decorrido:", current_time)
        starter_time = current_time - 0.05  # Tempo de início em segundos
        end_time = current_time + 0.05  # Tempo de fim em segundos

        # Converte o intervalo de tempo para amostras
        start_sample = int(starter_time * sample_rate)
        end_sample = int(end_time * sample_rate)
        
        print("{}".format(calculate_audio_energy(data[start_sample:end_sample])))
        last_time = current_time
    #energy = calculate_audio_energy(data[start_time:end_time])
    #print("Energia do áudio:", energy)

# Carrega o arquivo de áudio
data, sample_rate = librosa.load(r"C:\Users\micro1\Downloads\audio.wav")


#print(data[start_sample:end_sample])
# Inicia a reprodução do áudio
last_time = 0
start_time = time.time()
with sd.OutputStream(callback=audio_callback, samplerate=sample_rate):
    sd.play(data, sample_rate)
    sd.wait()
