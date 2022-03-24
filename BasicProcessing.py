# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 09:00:20 2022

@author: thierry.schwaller
"""

from scipy.io import wavfile
import numpy as np
import pyaudio
import wave  

def modified_amplitude_modulation(data,m,order_of_expansion):
    channel_1 = (m * data + 1)
    channel_2 = (np.sqrt(1 + m*data + 1/8*m**4*data**4))
    return np.column_stack((channel_1,channel_2))

def print_avaiable_channels(p):
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print((i,dev['name'],dev['maxInputChannels'],dev['maxOutputChannels']))    


chunk = 1024

samplerate, data = wavfile.read('africa-toto.wav')
data = data[samplerate*33:samplerate*35]
# data = data[0:samplerate*5]
normalized_data = data/32767
modified_data = modified_amplitude_modulation(normalized_data, 1, 0)
modified_scaled_data = modified_data * 32767



p = pyaudio.PyAudio()
print_avaiable_channels(p)

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=samplerate,
                output=True)

stream.write(data)  


stream.stop_stream()
stream.close()

p.terminate()