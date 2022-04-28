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

from scipy.signal import butter, windows, kaiserord, lfilter, firwin, freqz, firwin2, convolve
import pyaudio
import time
import numpy as np
import matplotlib.pyplot as plt

class AudioProcessing():
    def __init__(self ,
                 channel_count,
                 input_device,
                 output_device,
                 fir_window_size = 251,
                 chunk_size = 4096,
                 sampling_rate = 44100,
                 byte_width = 4):
        
        self.byte_width = byte_width
        self.channel_count = channel_count
        self.sampling_rate = sampling_rate
        self.chunk_size = chunk_size
        self.window_size = fir_window_size
        self.input_device = input_device
        self.output_device = output_device
        self.previousWindow = np.zeros(self.window_size,dtype=np.float32)
        self.bandpass = self.kaiserBandpass(self.window_size)
        self.equalizer_filter = self.equalizer({(0,200): 0,
                                                (200,1000): 0,
                                                (1000,2000):1,
                                                (2000,4000):1,
                                                (4000,8000):1,
                                                (8000,16000):0,
                                                (16000,20000):0}
                                               , "hamming")
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
        
    def print_avaiable_channels(self):
        for i in range(self.pyaudio.get_device_count()):
            dev = self.pyaudio.get_device_info_by_index(i)
            print((i,dev['name'],
                   dev['maxInputChannels'],
                   dev['maxOutputChannels'],
                   dev["defaultSampleRate"]))  
                
    def equalizer(self,
                  gain_dict,
                  filter_type,
                  **kwargs):
        taps = np.zeros(self.window_size,dtype=np.float32)
        for freq in gain_dict:
            if freq[0] == 0:
                taps += firwin(self.window_size,
                               freq[1]/22100,
                               window=filter_type)
            else:
                taps += firwin(self.window_size,
                               [v/22100 for v in freq],
                               window=filter_type,
                               pass_zero=False) * gain_dict[freq]
        fig, ax = plt.subplots()
        ax.stem(taps)
        
        w,h = freqz(taps)
        fig, ax =plt.subplots()
        ax.plot(w / np.pi * 22100,20*np.log10(np.abs(h)))
        return taps
            
    def kaiserBandpass(self, 
                       window_size,
                       f_c_hp = 200, # 200 Hz
                       f_c_lp = 15000,
                       beta_lp = 3):
        
        lowpass = firwin(window_size //2 ,
                          cutoff = f_c_lp/self.sampling_rate*2,
                          window=("kaiser",beta_lp),
                          pass_zero=True)
        highpass = firwin(window_size //2,
                         cutoff = f_c_hp/self.sampling_rate*2,
                         window="blackman",
                         pass_zero=False)
        
        bandpass = np.convolve(lowpass, highpass)
        # fig, ax = plt.subplots()
        # ax.stem(lowpass)
        
        # fig, ax = plt.subplots()
        # w,h = freqz(lowpass)
        # ax.plot(w/np.pi*self.sampling_rate/2,20*np.log10(np.abs(h)))
        
        # fig, ax = plt.subplots()
        # ax.stem(highpass)
        
        # fig, ax = plt.subplots()
        # w,h = freqz(highpass)
        # ax.plot(w/np.pi*self.sampling_rate/2,20*np.log10(np.abs(h)))
        
        # bandpass = np.convolve(lowpass, highpass)
        # fig, ax = plt.subplots()
        # ax.stem(bandpass)
        
        # fig, ax = plt.subplots()
        # w, h = freqz(bandpass)
        # ax.plot(w/np.pi*self.sampling_rate/2,20*np.log10(np.abs(h)))
        
        return bandpass
    
    def callback(self, 
                 in_data,
                 frame_count,
                 time_info, status):
        if status:
            print("Playback Error: %i" % status)
        callback_output = np.frombuffer(in_data, dtype=np.float32)
        # Only process left channel and then duplicate at the end
        left_channel = callback_output[::2]
        # Overlap
        left_channel_long = np.hstack((self.previousWindow,
                                        left_channel))
        output = np.convolve(left_channel_long,self.equalizer_filter,"valid")
        output = np.float32(output)
        full_callback_lp = np.repeat(output, 2)
        self.previousWindow = left_channel[-self.window_size:]
        return (full_callback_lp, pyaudio.paContinue)


audioPro = AudioProcessing(2,input_device=1,output_device=5)
try:
    while audioPro.stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt: 
    audioPro.endStream()
    

