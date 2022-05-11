# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 08:06:56 2022

@author: thierry.schwaller
"""
import pyaudio 
import sounddevice as sd

BUFFER_SIZE = 4096
DURATION = 5
SAMPLE_RATE = 44100


p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i,dev['name'],dev['maxInputChannels'],dev['maxOutputChannels']))    
    
input_stream = p.open(
    format=pyaudio.paInt16,
    channels=2,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=BUFFER_SIZE,
    input_device_index=10
    )

output_stream = p.open(
    format=pyaudio.paInt16,
    channels=2,
    rate=SAMPLE_RATE,
    output=True
    )

for i in range(int(SAMPLE_RATE / BUFFER_SIZE * DURATION)):
    data = input_stream.read(BUFFER_SIZE)
    output_stream.write(data)

input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()