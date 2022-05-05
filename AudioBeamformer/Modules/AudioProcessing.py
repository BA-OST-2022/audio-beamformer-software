###############################################################################
# file    AudioProcessing.py
###############################################################################
# brief   This module handels the audio processing for the audio-beamformer
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-05-04
###############################################################################
# MIT License
#
# Copyright (c) 2021 Institute for Networked Solutions OST
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################
# For Equalizer and Filter
from scipy.interpolate import interp1d
from scipy.signal import butter, windows, kaiserord, lfilter, firwin, freqz, firwin2, convolve
# Audio In / Output Handling
import sounddevice as sd
# Other
import sys
import numpy as np
import matplotlib.pyplot as plt

def AudioProcessing():
    def __init__(self,
                input_device_index = 0,
                output_device_index = 0,
                samplerate=44100,
                chunk_size=1024,
                equalizer_window_size=123):

        self.chunk_size = chunk_size
        self.samplerate = samplerate
        self.equalizer_profiles = {"First equalizer": {}}
        # Window size can not be even
        if (equalizer_window_size % 2):
            print(f"FIR window size was made uneven. Length: {equalizer_window_size-1}")
            self.equ_window_size = equalizer_window_size - 1
        else:
             self.equ_window_size = equalizer_window_size
        # If system is linux then the loopback and the audio beamformer 
        # are the initial input/output devices
        if(sys.platform == 'linux'):
            channels = getChannels
            self.output_device = [i[1] for i in channels].index('snd_rpi_hifiberry_dac: HifiBerry DAC HiFi pcm5102a-hifi-0 (hw:0,0)')
            inputDeviceName = [s for s in [i[1] for i in channels] if s.startswith('Loopback') and s.endswith(',1)')][0]
            self.input_device = [i[1] for i in channels].index(inputDeviceName)
        else:
            self.input_device_index = input_device_index
            self.output_device_index = output_device_index

        self.__previousWindow = np.zeros(self.window_size - 1,dtype=np.float32)
        

    def getChannels(self):
        channelInfo = []
        for p,i in enumerate(sd.query_devices()):
            print(f"{p} Name: {i['name']}, In {i['max_input_channels']}, Out {i['max_output_channels']}") 
            channelInfo.append((p,
                                i['name'],
                                i['max_input_channels'],
                                i['max_output_channels']))
        return channelInfo