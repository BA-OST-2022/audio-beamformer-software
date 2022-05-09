s# -*- coding: utf-8 -*-
"""
Created on Tue May  3 13:51:20 2022

@author: thierry.schwaller
"""

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

from scipy.interpolate import interp1d
from scipy.signal import butter, windows, kaiserord, lfilter, firwin, freqz, firwin2, convolve
import sounddevice as sd
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

class AudioProcessing():
    def __init__(self ,
                 channel_count_input = 1,   # Default Stereo
                 channel_count_output = 2,  # Default Stereo
                 input_device = 9,      # Dummy Input
                 output_device = 11,     # Dummy Output
                 fir_window_size = 555,
                 chunk_size = 1024,
                 sampling_rate = 44100,
                 byte_width = 4):
        
        self.byte_width = byte_width
        self.channel_count_input = channel_count_input
        self.channel_count_output = channel_count_output
        self.sampling_rate = sampling_rate
        self.chunk_size = chunk_size
        self.window_size = fir_window_size
        self.input_device = input_device
        self.output_device = output_device
        
        self.previousWindow = np.zeros(self.window_size - 1,dtype=np.float32)
        frq = np.linspace(200,20000)
        model_transducer = np.column_stack((frq.T,200**(2/3)/(frq.T)**(2/3)))
        self.gain_dict = self.equalizeModell(model_transducer,
                                             "1/w^2",
                                             20,
                                             spacing="lin")
        # self.equalizer_filter = self.equalizer({(0,200): {"band_gain": 0,
        #                                                   "f_type":("kaiser",8.6)},
        #                                         (200,2000): {"band_gain": 1,
        #                                                      "f_type": ("kaiser",5)},
        #                                         (2000,4000): {"band_gain": 0,
        #                                                       "f_type":("kaiser",5)},
        #                                         (4000,8000): {"band_gain": 1,
        #                                                       "f_type":("kaiser",5)},
        #                                         (8000,16000): {"band_gain": 1,
        #                                                        "f_type":("kaiser",5)},
        #                                         (16000,20000): {"band_gain": 0,
        #                                                         "f_type":("kaiser",5)}})
        self.equalizer_filter = self.equalizer(self.gain_dict)
        
    def setupStream(self):
        self.stream = sd.Stream(samplerate=self.sampling_rate,
                                blocksize=self.chunk_size,
                                device=(self.input_device, self.output_device), 
                                channels=(self.channel_count_input,
                                          self.channel_count_output),
                                dtype=np.int32,
                                callback=self.callback)
                                
    def getChannels(self):
        channelInfo = []
        for p,i in enumerate(sd.query_devices()):
            print(f"{p} Name: {i['name']}, In {i['max_input_channels']}, Out {i['max_output_channels']}") 
            channelInfo.append((p,
                                i['name'],
                                i['max_input_channels'],
                                i['max_output_channels']))
        return channelInfo

         
    def equalizer(self, gain_dict):
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
    
    def equalizeModell(self, 
                       model_is,
                       model_should,
                       nr_of_tabs,
                       spacing="lin",
                       start_frq=200,
                       stop_frq=20000):
        if spacing=="log":
            taps_pos = np.geomspace(start_frq, stop_frq, num=nr_of_tabs)
        elif spacing=="lin":
            taps_pos = np.linspace(start_frq, stop_frq, nr_of_tabs)
        else:
            raise Exception(f"Spacing has to be 'log' or 'lin' and not {spacing}")
            
        func_model_is = interp1d(model_is[:,0],model_is[:,1])
        
        if model_should == "equal":
            func_model_should = interp1d([start_frq,stop_frq],[1,1])
        elif model_should == "1/w":
            func_model_should = interp1d(taps_pos, start_frq/taps_pos)
        elif model_should == "1/w^2":
            func_model_should = interp1d(taps_pos, start_frq**2/taps_pos**2)
        else:
            raise Exception(f"model_should has to be 'equal','1/w' or '1/w^2' and not {model_should}")
            
        taps_pos_between = np.convolve(taps_pos,[0.5,0.5],"valid")
        val_is = func_model_is(taps_pos_between)
        val_should = func_model_should(taps_pos_between) 
        gain = val_should/val_is
        gain_norm = gain / max(gain)
        
        gain_dict = {(taps_pos[i], taps_pos[i+1]): {"band_gain": g
                                                    , "f_type":("kaiser",5)} for i,g in enumerate(gain_norm)}
        fig, ax = plt.subplots()
        ax.plot(model_is[:,0],model_is[:,1])
        ax.vlines(taps_pos,0,1,colors="red",linestyles="dashed")
        
        fig, ax = plt.subplots()
        ax.plot(taps_pos, func_model_should(taps_pos)) 
        
        return gain_dict
    
    def MAMPreprocessing(self):
        pass
    
    def callback(self, indata, outdata, frames, time, status):
        if status:
            print(status)

        indata_oneCh = indata[:,0]
        indata_oneCh = np.hstack((self.previousWindow,
                                  indata_oneCh))
        
        outdata_oneCh = np.convolve(indata_oneCh,
                                    self.equalizer_filter,
                                    "valid")
        outdata_oneCh = np.float32(outdata_oneCh)
        outdata_oneCh = indata[:,0]
        self.previousWindow = indata_oneCh[-self.window_size+1:]
        # print(indata_oneCh)
        outdata[:] = np.column_stack((outdata_oneCh, outdata_oneCh))



if __name__ == "__main__":
    audioPro = AudioProcessing()
    channels = audioPro.getChannels()
    
    if(sys.platform == 'linux'):
        audioPro.output_device = [i[1] for i in channels].index('snd_rpi_hifiberry_dac: HifiBerry DAC HiFi pcm5102a-hifi-0 (hw:0,0)')
        # audioPro.output_device = [i[1] for i in channels].index('USB Audio Device: - (hw:1,0)')
        inputDeviceName = [s for s in [i[1] for i in channels] if s.startswith('Loopback') and s.endswith(',1)')][0]
        audioPro.input_device = [i[1] for i in channels].index(inputDeviceName)
        # audioPro.input_device = [i[1] for i in channels].index('Samson RXD wireless receiver: USB Audio (hw:5,0)')
    print(f"Output Index: {audioPro.output_device}, Input Index: {audioPro.input_device}")
    
    audioPro.setupStream()
    try:
        with audioPro.stream:
            print('#' * 80)
            print('press Return to quit')
            print('#' * 80)
            input()
    except KeyboardInterrupt: 
        print("Stream terminated")
    

