#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 22:32:19 2022

@author: root
"""

"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).
This is the callback (non-blocking) version.
"""


# https://www.tutonaut.de/raspberry-pi-als-bluetooth-airplay-empfaenger-kombi/

# Test Thierry


import pyaudio
import time
import numpy as np
# import matplotlib.pyplot as plt


def modified_amplitude_modulation(data,m):
    channel_1 = 1/2*(m * data + 1)
    channel_2 = np.zeros(data)      #1/2*(1 - 1/2*m**4*data**2 - 1/8*m**4*data**4)
    return np.column_stack((channel_1,channel_2))

def print_avaiable_channels(p):
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print((i,dev['name'],dev['maxInputChannels'],dev['maxOutputChannels']))  
        

WIDTH = 4
CHANNELS = 1
RATE = 44100
CHUNK = 4096
p = pyaudio.PyAudio()

# fig, ax = plt.subplots()
# xdata, ydata = [], []
# ln, = ax.plot([], [], 'ro-')

def callback(in_data, frame_count, time_info, status):
    if status:
        print("Playback Error: %i" % status)
    callback_output = np.fromstring(in_data, dtype=np.int32)
    #print(len(callback_output))
    #fft = np.fft.rfft(callback_output)
    #print(len(fft))
    #Limiter
    #Equalizer
    #Bandpass
    # Kaiser Window
    
    return (in_data, pyaudio.paContinue)



print_avaiable_channels(p)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE, 
                frames_per_buffer=CHUNK,
                input_device_index=4,
                output_device_index=1,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()
try:
    while stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt:
    stream.stop_stream()  
    stream.close()
    
    p.terminate()