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
#import matplotlib.pyplot as plt

class AudioProcessing():
    def __init__(self ,
                 channel_count,
                 input_device,
                 output_device,
                 fir_window_size = 100,
                 chunk_size = 4096,
                 sampling_rate = 44100,
                 byte_width = 4):
        
        self.byte_width = byte_width
        self.channel_count = 1
        self.sampling_rate = sampling_rate
        self.chunk_size = chunk_size
        self.window_size = fir_window_size
        self.input_device = input_device
        self.output_device = output_device
        self.previousWindow = np.zeros(self.window_size)
        self.low_pass, self.high_pass = self.kaiserBandpass(self.window_size)
        self.startStream()
        
    def startStream(self):
        self.pyaudio = pyaudio.PyAudio()
        self.print_avaiable_channels()
        self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.byte_width),
                                        channels=self.channel_count,
                                        rate=self.sampling_rate, 
                                        frames_per_buffer=self.chunk_size,
                                        input_device_index=self.input_device,
                                        output_device_index=self.output_device,
                                        input=True,
                                        output=True,
                                        stream_callback=self.callback)
        self.stream.start_stream()
        
    def endStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()
        
    def setupStream(self):
        stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.byte_width),
                                   channels=self.channel_count,
                                   rate=self.sampling_rate, 
                                   frames_per_buffer=self.chunk_size,
                                   input_device_index=self.input_device,
                                   output_device_index=self.output_device,
                                   input=True,
                                   output=True,
                                   stream_callback=self.callback)
        return stream
                
        
    def print_avaiable_channels(self):
        for i in range(self.pyaudio.get_device_count()):
            dev = self.pyaudio.get_device_info_by_index(i)
            print((i,dev['name'],dev['maxInputChannels'],dev['maxOutputChannels']))  
                
        
    def kaiserBandpass(self, 
                       window_size,
                       w_c_l = 0.0904977375565611 * np.pi, # 200 Hz
                       w_c_h = 0.6787330316742082 * np.pi,
                       beta_l = 5,
                       beta_h = 5):
        k = np.linspace(-window_size//2, window_size//2,window_size)
        kaiser_window_l = np.kaiser(window_size,beta_l)
        kaiser_window_h = np.kaiser(window_size,beta_h)
        sinc_fun_l = np.sin(w_c_l*k)/(np.pi*k) * kaiser_window_l
        sinc_fun_h = np.sin(w_c_h*k)/(np.pi*k) * kaiser_window_h
            
        dirac = np.zeros(window_size)
        dirac[window_size//2] = 1
            
        highpass = dirac - sinc_fun_l
        lowpass = sinc_fun_h
            
        # print(np.sum(lowpass))
        # print(np.sum(highpass))
        
        # fig, ax = plt.subplots()
        # ax.plot(highpass)
        
        # fig, ax = plt.subplots()
        # ax.plot(lowpass)
        
        # fig, ax = plt.subplots()
        # ax.plot(np.abs(np.fft.rfft(lowpass)))
        
        # fig, ax = plt.subplots()
        # ax.plot(np.abs(np.fft.rfft(highpass)))
        
        return lowpass, highpass
    
    def callback(self, 
                 in_data,
                 frame_count,
                 time_info, status):
        if status:
            print("Playback Error: %i" % status)
        callback_output = np.frombuffer(in_data, dtype=np.int32)
        full_callback = np.hstack((self.previousWindow,callback_output))
        full_callback_lp = np.convolve(full_callback,self.low_pass,"valid")
        self.previousWindow = callback_output[-self.window_size:]
        return (full_callback_lp, pyaudio.paContinue)


audioPro = AudioProcessing(1,input_device=4,output_device=1)
try:
    while audioPro.stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt:
    audioPro.endStream()
audioPro.endStream()
