# Instalaciones previas
# sudo apt install lame portaudio19-dev gcc python-pip ffmpeg libavcodec-extra libav-tools
# pip install PyAudio pydub
# python -m pip install --upgrade pip
# https://gist.github.com/mabdrabo/8678538
# https://github.com/jiaaro/pydub
# https://github.com/vprusso/youtube_tutorials/blob/master/utility_scripts/wav_to_mp3/wav_to_mp3.py

import pyaudio
import pydub
import wave
import os
import commands
import glob
from datetime import datetime

primera = False

while True:
    if primera:
        try:
            sound = pydub.AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
            sound.export(mp3file, format="mp3", bitrate="128k")
        except IOError:
            print 'cannot open'
        else:
            os.remove(WAVE_OUTPUT_FILENAME)
            print("* MP3 Listo")
    primera = True

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 22000
    RECORD_SECONDS = 300

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    fecha = str(datetime.now())[:19]
    WAVE_OUTPUT_FILENAME = fecha+".wav"
    mp3file = fecha+".mp3"

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    """ try:
        sound = pydub.AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
        sound.export(mp3file, format="mp3", bitrate="128k")
    except IOError:
        print 'cannot open'
    else:
        os.remove(WAVE_OUTPUT_FILENAME)
        print("* MP3 Listo")
    """
    # commands.getoutput('lame -V0 -h -b 128 --vbr-new WAVE_OUTPUT_FILENAME mp3file')