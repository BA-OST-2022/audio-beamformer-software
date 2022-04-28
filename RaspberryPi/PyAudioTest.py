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
import sys

class AudioProcessing():
    def __init__(self ,
                 channel_count = 2,     # Default Stereo
                 input_device = 3,      # Dummy Input
                 output_device = 0,     # Dummy Output
                 fir_window_size = 255,
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
        
        #self.bandpass = self.kaiserBandpass(self.window_size)
        self.equalizer_filter = self.equalizer({(0,200): {"band_gain": 0,
                                                          "f_type":("blackman")},
                                                (200,2000): {"band_gain": 1,
                                                             "f_type": ("kaiser",5)},
                                                (2000,4000): {"band_gain": 0,
                                                              "f_type":("hamming")},
                                                (4000,8000): {"band_gain": 1,
                                                              "f_type":("hamming")},
                                                (8000,16000): {"band_gain": 1,
                                                               "f_type":("hamming")},
                                                (16000,20000): {"band_gain": 0,
                                                                "f_type":("hamming")}})
        self.pyaudio = pyaudio.PyAudio()
        # print(self.getChannels())
        
        
    def startStream(self):
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
        
    def getChannels(self):
        channelInfo = []
        for i in range(self.pyaudio.get_device_count()):
            dev = self.pyaudio.get_device_info_by_index(i)
            channelInfo.append((i,dev['name'],
                   dev['maxInputChannels'],
                   dev['maxOutputChannels'],
                   dev["defaultSampleRate"]))
        return channelInfo

         
    def equalizer(self, gain_dict, **kwargs):
        taps = np.zeros(self.window_size,dtype=np.float32)
        for freq in gain_dict:
            if freq[0] == 0:
                taps += firwin(self.window_size,
                               freq[1]/self.sampling_rate*2,
                               window=gain_dict[freq]["f_type"],
                               pass_zero=True) * gain_dict[freq]["band_gain"]
            else:
                taps += firwin(self.window_size,
                               [v/self.sampling_rate*2 for v in freq],
                               window=gain_dict[freq]["f_type"],
                               pass_zero=False) * gain_dict[freq]["band_gain"]
        fig, ax = plt.subplots()
        ax.stem(taps)
        
        w,h = freqz(taps)
        fig, ax =plt.subplots()
        ax.plot(w / np.pi * self.sampling_rate / 2,20*np.log10(np.abs(h)))
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



if __name__ == "__main__":
    audioPro = AudioProcessing()
    channels = audioPro.getChannels()
    
    if(sys.platform == 'linux'):
        audioPro.output_device = [i[1] for i in channels].index('snd_rpi_hifiberry_dac: HifiBerry DAC HiFi pcm5102a-hifi-0 (hw:0,0)')
        audioPro.input_device = [i[1] for i in channels].index('Loopback: PCM (hw:1,1)')
    
    print(f"Output Index: {audioPro.output_device}, Input Index: {audioPro.input_device}")
    audioPro.startStream()
    
    try:
        while audioPro.stream.is_active():
            time.sleep(0.1)
    except KeyboardInterrupt: 
        audioPro.endStream()
    

