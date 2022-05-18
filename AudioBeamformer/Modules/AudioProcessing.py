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
from importlib.abc import SourceLoader
from tkinter.messagebox import NO
from scipy.interpolate import interp1d
from scipy.signal import butter, windows, kaiserord, lfilter, firwin, freqz, firwin2, convolve
# Audio In / Output Handling
import sounddevice as sd
# Other
import os
import sys
import numpy as np
import ast

DEBUG = True
LINUX = (sys.platform == 'linux')
sys.path.insert(0, os.path.dirname(__file__)) 
sys.path.insert(0, os.path.dirname(__file__) + "/Modules")

from AudioPlayer import AudioPlayer


class AudioProcessing:
    def __init__(self):
        # Adjustable values
        self._chunk_size = 4096
        self._samplerate = 44100
        self.equ_window_size = 123
        self.__black_list_input_device = ["pulse","loopin","default"]
        self.__modulation_dict = {0: self.AMModulation, 1: self.MAMModulation}
        # Device index
        if LINUX:  
            # If system is linux then the loopback and the audio beamformer 
            # are the initial input/output devices
            channels = self.getChannels()
            self._output_device = [i[1] for i in channels].index('snd_rpi_hifiberry_dac: HifiBerry DAC HiFi pcm5102a-hifi-0 (hw:0,0)')
            inputDeviceName = [s for s in [i[1] for i in channels] if s.startswith('Loopback') and s.endswith(',1)')][0]
            self._input_device = [i[1] for i in channels].index(inputDeviceName)
        else:
            self._input_device = 0
            self._output_device = 2
        # Start values
        self._tot_gain = 1
        self._output_enable = 1
        self._equalizer_enable = False
        self._modulation_index = 0
        self._mam_gain = 1
        self._enable_interpolation = False
        self._interpolation_factor = 0
        self._stream = None
        self.__previousWindow = np.zeros(self.equ_window_size - 1,dtype=np.float32)
        self.__current_source_level = 0
        self.__source_dict = {}
        self.__equalizer_profile_list = {}
        self.__equalizerList = []
        self.__stream_running = False
        self._enableMagic = False
        self._player = AudioPlayer(sampleRate=self._samplerate, blockSize=self._chunk_size)
        
        # Equalizer initialization
        self.__equalier_dict_path = os.path.dirname(os.path.realpath(__file__)) + "/Files/equalizer_dict.txt"
        with open(self.__equalier_dict_path) as f:
            for line in f.readlines():
                line_tupel = ast.literal_eval(line)
                self.__equalizerList.append(line_tupel[0])
                self.__equalizer_profile_list[line_tupel[0]] = line_tupel[1]
        self._equalizer_filter = np.ones(self.equ_window_size)
        self.generatePlots()

    def begin(self):
            self.getChannels()
            self.setupStream()
            self.startStream()

    def end(self):
        self._stream.close()

    def setupStream(self): 
        if LINUX or DEBUG:
            if sd.query_devices(self._input_device)['max_input_channels'] >= 1:
                channel_input = 1 if sd.query_devices(self._input_device)['max_input_channels'] == 1 else 2
            else:
                channel_input = 2
                self._input_device = self.__sourceIndexList[0]
            self._stream = sd.Stream(samplerate=self._samplerate,
                                    blocksize=self._chunk_size,
                                    device=(self._input_device , self._output_device), 
                                    channels=(channel_input, 2),
                                    dtype=np.int32,
                                    callback=self.callback)



    def startStream(self):
        if self._stream:
            self._stream.start()
            self.__stream_running = True

    def endStream(self):
        if self._stream:
            self._stream.close()
            self.__stream_running = False

    def generatePlots(self):
        for key in self.__equalizer_profile_list.keys():
            y_val = []
            x_val = []
            for freq_band in self.__equalizer_profile_list[key].keys():
                x_val.append(freq_band[0])
                x_val.append(freq_band[1])
                y_val.append(self.__equalizer_profile_list[key][freq_band]["band_gain"])
                y_val.append(self.__equalizer_profile_list[key][freq_band]["band_gain"])

    def getChannels(self):
        channelInfo = []
        sd._terminate()
        sd._initialize()
        for p,i in enumerate(sd.query_devices()):
            print(f"{p} Name: {i['name']},API: {i['hostapi']} ,In {i['max_input_channels']}, Out {i['max_output_channels']}") 
            channelInfo.append((p,
                                i['name'],
                                i['max_input_channels'],
                                i['hostapi'],
                                i['max_output_channels']))
        return channelInfo

    def getSourceList(self): 
        if self.__stream_running:
            sd._terminate()
            sd._initialize()     
        default_val = "System"
        sourceIndexList = []
        sourceList = []
        for i,device in enumerate(sd.query_devices()):
            if device["hostapi"] == 0 and device['max_input_channels'] > 0:
                if not any(bl == device["name"] for bl in self.__black_list_input_device):
                    if not (device["name"].startswith('Loopback') and device["name"].endswith(',0)')):
                        sourceIndexList.append(i)
                        if (device["name"].startswith('Loopback') and device["name"].endswith(',1)')):
                            sourceList.append(default_val)
                        else:
                            sourceList.append(device["name"])
        if LINUX:
            ind = sourceList.index(default_val)
            sourceList.insert(0,sourceList.pop(ind))
            sourceIndexList.insert(0,sourceIndexList.pop(ind))
        self.__sourceIndexList = sourceIndexList
        # Filter source list
        return sourceList

    def setSource(self, source_index):
        if self.__stream_running:
            # Stream terminate
            self.endStream()
        # Stream setup
        if source_index < len(self.__sourceIndexList):
            self._input_device = self.__sourceIndexList[source_index]
        else:
            self._input_device = self.__sourceIndexList[0]
        # Stream start
        self.setupStream()
        self.startStream()

    def setSourceLevel(self, indata):
        indata = indata /2147483648
        rms = np.sqrt(np.mean(indata**2))
        if not rms < 0.00001:
            level = 10*np.log10(np.sqrt(np.mean(indata**2)))
        else:
            level = -50
        if level:
            self.__current_source_level = level
        else:
            self.__current_source_level = -50

    def setOutputEnable(self,enable):
        self._output_enable = enable

    def getSourceLevel(self):
        return self.__current_source_level

    def setGain(self,gain):
        self._tot_gain = gain
        print(self._tot_gain)
    
    def enableEqualizer(self,enable):
        self._equalizer_enable = enable

    def getEqualizerProfileList(self):
        return list(self.__equalizer_profile_list.keys())

    def equalizer(self, gain_dict):
        taps = np.zeros(self.equ_window_size,dtype=np.float32)
        for freq in gain_dict:
            if freq[0] == 0:
                taps += firwin(self.equ_window_size,
                               freq[1]/self._samplerate*2,
                               window=gain_dict[freq]["f_type"],
                               pass_zero=True) * gain_dict[freq]["band_gain"]
            else:
                taps += firwin(self.equ_window_size,
                               [v/self._samplerate*2 for v in freq],
                               window=gain_dict[freq]["f_type"],
                               pass_zero=False) * gain_dict[freq]["band_gain"]
        #fig, ax = plt.subplots()
        #ax.stem(taps)
        
        #w,h = freqz(taps)
        #fig, ax =plt.subplots()
        #ax.plot(w / np.pi * self.sampling_rate / 2,20*np.log10(np.abs(h)))
        return taps

    def equalizerPlot(self):
        pass

    def setEqualizerProfile(self,profile):
        taps = self.equalizer(self.__equalizer_profile_list[self.__equalizerList[profile]])
        self._equalizer_filter = taps

    def enableInterpolation(self,enable):
        # Call function from FPGA and enable interpolation
        # FPGA.Interpolation(self._interpolation_factor)
        self._enable_interpolation = enable
        if enable:
            #FPGA.enableInterpolation()
            #FPGA.interpolationFactor(self._interpolation_factor)
            pass
        else:
            #FPGA.disableInterpolation()
            pass
        pass

    def setInterpolationFactor(self,factor):
        self._interpolation_factor = factor

    def setModulationType(self, type):
        print(type)
        self._modulation_index = type
    
    def setMAMMix(self,gain):
        self._mam_gain = gain

    def AMModulation(self,data):
        return data

    def MAMModulation(self,data):
        data = data / 2147483648
        data_out = 1 - 1/2*data**2 - 1/8**data**4
        return data_out * 2147483648  * self._mam_gain
    
    def enableMagic(self, state):
        self._enableMagic = state
        if(state):
            self._player.begin("files/magic.wav")
        else:
            self._player.end()

    def callback(self, indata, outdata, frames, time, status):
        indata_oneCh = indata[:,0] * self._tot_gain 
        self.setSourceLevel(indata_oneCh)
        indata_oneCh *= self._output_enable
        if self._equalizer_enable:
            indata_oneCh = np.hstack((self.__previousWindow,
                                    indata_oneCh))
            
            outdata_oneCh = np.convolve(indata_oneCh,
                                        self._equalizer_filter,
                                        "valid")
            outdata_oneCh = np.float32(outdata_oneCh)
        else:
            outdata_oneCh = indata[:,0]
            
        # if self._enableMagic:
        #     outdata_oneCh = self._player.getData()[:,0]
            
        # Modulation
        second_channel_data = self.__modulation_dict[self._modulation_index](outdata_oneCh)
        # Stich output together
        outdata[:] = np.column_stack((outdata_oneCh, second_channel_data))
        self.__previousWindow = indata_oneCh[-self.equ_window_size+1:]

    def createEqualizerPlots(self):
        path = "../GUI/qml/images"


if __name__ == '__main__':
    import time
    audio_processing = AudioProcessing()
    print(audio_processing.getSourceList())
    audio_processing.enableMagic(True)
    
    audio_processing.begin()
    time.sleep(10)
    audio_processing.end()
    

