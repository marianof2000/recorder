# Instalaciones previas
# sudo apt install lame portaudio19-dev gcc python-pip ffmpeg libavcodec-extra libav-tools
# pip install PyAudio pydub command // instalarlos también como root
# python -m pip install --upgrade pip
# https://gist.github.com/mabdrabo/8678538
# https://github.com/jiaaro/pydub
# https://github.com/vprusso/youtube_tutorials/blob/master/utility_scripts/wav_to_mp3/wav_to_mp3.py
# https://thispointer.com/how-to-create-a-directory-in-python/

import pyaudio
import pydub
import wave
import os
from datetime import datetime
from time import sleep

rutabase = 'record/'
#rutabase = '/home/privado/recorder/record/'
hora = 700 # permite entrar al ciclo while

try:
    # Crea directorio de base 'record' en caso de no existir
    os.mkdir(rutabase)
    #print("Directory " , rutabase ,  " Created ") 
except FileExistsError:
    print("* Directory " , rutabase ,  " already exists")
    pass

# hace el ciclo hasta las 19 horas
while hora<=1900:
    fecha = str(datetime.now())[:19]
    hora = int(fecha[11:13]+fecha[14:16])
    ruta = rutabase+fecha[:10]+'/'
    try:
        # Crea directorio diario con formato fecha
        os.mkdir(ruta)
        # print("Directory " , ruta ,  " Created ") 
    except FileExistsError:
        print("* Directory " , ruta ,  " already exists")
        pass

    # graba en los horarios de entrada y de salida de maniana y tarde
    if (hora>=800 and hora<=1200) or (hora>=1330 and hora<=1630):
        # nombres de los archivos a generar
        WAVE_OUTPUT_FILENAME = ruta+fecha+".wav"
        mp3file = ruta+fecha.replace(" ", "_")+".mp3"

        #objeto de grabacion 
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 22000
        RECORD_SECONDS = 600 #archivos de 10 minutos (600 segundos)
        p = pyaudio.PyAudio() 
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
        print("* recording")
        # genera el stream de grabacion
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()

        # genera el archivo WAV con todo lo capturado
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        try:
            # convierte el archivo WAV a MP3
            sound = pydub.AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
            sound.export(mp3file, format="mp3", bitrate="128k")
        except IOError:
            print('cannot open')
        else:
            # remueve el archivo WAV, deja solo el MP3
            os.remove(WAVE_OUTPUT_FILENAME)
            # agrega al archivo de log
            log = open(rutabase+"logs.txt","a+")
            log.write(fecha+" "+mp3file+"\n")
            log.close() 
            print("* MP3 Listo")

    else:
        # espera que sean los horarios de trabajo, no captura
        print("* Esperando: "+str(hora))
        sleep(60)
