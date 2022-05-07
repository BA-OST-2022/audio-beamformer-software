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
from scipy.interpolate import interp1d
from scipy.signal import butter, windows, kaiserord, lfilter, firwin, freqz, firwin2, convolve
# Audio In / Output Handling
import sounddevice as sd
# Other
import sys
import numpy as np
import ast

class AudioProcessing:
    def __init__(self,
                input_device_index = 1,
                output_device_index = 3,
                samplerate=44100,
                chunk_size=4096,
                equalizer_window_size=123):
        self.__equalier_dict_path = "Modules/Files/equalizer_dict.txt"
        self.__equalizer_profile_list = {}
        with open(self.__equalier_dict_path) as f:
            for line in f.readlines():
                line_tupel = ast.literal_eval(line)
                self.__equalizer_profile_list[line_tupel[0]] = line_tupel[1]
        self._chunk_size = chunk_size
        self._samplerate = samplerate
        self._tot_gain = 1
        self._equalizer_enable = False
        self._modulation_index = 0
        self._mam_gain = 1
        self._enable_interpolation = False
        self._interpolation_factor = 0
        if(sys.platform == 'linux'):
            channels = getChannels
            self._output_device = [i[1] for i in channels].index('snd_rpi_hifiberry_dac: HifiBerry DAC HiFi pcm5102a-hifi-0 (hw:0,0)')
            inputDeviceName = [s for s in [i[1] for i in channels] if s.startswith('Loopback') and s.endswith(',1)')][0]
            self._input_device = [i[1] for i in channels].index(inputDeviceName)
        else:
            self._input_device = input_device_index
            self._output_device = output_device_index
        self._channel_count_input = 1 # Get channel count
        self._channel_count_output = 2

        # Window size can not be even
        if not (equalizer_window_size % 2):
            print(f"FIR window size was made uneven. Length: {equalizer_window_size-1}")
            self.equ_window_size = equalizer_window_size - 1
        else:
             self.equ_window_size = equalizer_window_size
        # If system is linux then the loopback and the audio beamformer 
        # are the initial input/output devices
        self.__previousWindow = np.zeros(self.equ_window_size - 1,dtype=np.float32)
        self.__modulation_dict = {0: self.AMModulation, 1: self.MAMModulation}
        self.__current_source_level = 0
        self.__source_dict = {}
        self.__stream_running = False

    def begin(self):
            self.getChannels()
            self.setupStream()
            self._stream.start()

    def end(self):
        self._stream.close()

    def setupStream(self):
        self._stream = sd.Stream(samplerate=self._samplerate,
                                blocksize=self._chunk_size,
                                device=(self._input_device, self._output_device), 
                                channels=(self._channel_count_input, self._channel_count_output),
                                dtype=np.int32,
                                callback=self.callback)

    def startStream(self):
        self._stream.start()
        self.__stream_running = True

    def endStream(self):
        self._stream.close()
        self.__stream_running = False

    def getChannels(self):
        channelInfo = []
        for p,i in enumerate(sd.query_devices()):
            print(f"{p} Name: {i['name']},API: {i['hostapi']} ,In {i['max_input_channels']}, Out {i['max_output_channels']}") 
            channelInfo.append((p,
                                i['name'],
                                i['max_input_channels'],
                                i['hostapi'],
                                i['max_output_channels']))
        return channelInfo

    def getSourceList(self):
        sourceDict = {}
        sourceList = []
        counter = 0
        for i,device in enumerate(sd.query_devices()):
            if device['max_input_channels'] > 0 and device['hostapi'] == 0:
                sourceList.append(device["name"])
                sourceDict[counter] = i
                counter += 1
        self.__source_dict = sourceDict
        # Filter source list
        return sourceList

    def setSource(self, source_index):
        if self.__stream_running:
            # Stream terminate
            self.endStream()
        # Stream setup
        self._input_device = self.__source_dict[source_index]
        # Stream start
        self.setupStream()
        self.startStream()

    def setSourceLevel(self, indata):
        indata = indata /2147483648
        self.__current_source_level = np.sqrt(np.mean(indata**2))

    def getSourceLevel(self):
        return self.__current_source_level

    def setGain(self,gain):
        self._tot_gain = gain
    
    def enableEqualizer(self,enable):
        self._equalizer_enable = enable

    def getEqualizerProfileList(self):
        return list(self.__equalizer_profile_list.keys())

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
        self._modulation_index = type
    
    def setMAMMix(self,gain):
        self._mam_gain = gain

    def AMModulation(self,data):
        # Implement logic
        return data

    def MAMModulation(self,data):
        # Implement logic
        return data * self._mam_gain

    def callback(self, indata, outdata, frames, time, status):
        indata_oneCh = indata[:,0] * self._tot_gain
        self.setSourceLevel(indata_oneCh)
        if self._equalizer_enable:
            indata_oneCh = np.hstack((self.previousWindow,
                                    indata_oneCh))
            
            outdata_oneCh = np.convolve(indata_oneCh,
                                        self.equalizer_filter,
                                        "valid")
            outdata_oneCh = np.float32(outdata_oneCh)
        else:
            outdata_oneCh = indata[:,0]
        # Modulation
        second_channel_data = self.__modulation_dict[self._modulation_index](outdata_oneCh)
        # Stich output together
        outdata[:] = np.column_stack((outdata_oneCh, second_channel_data))
        self.previousWindow = indata_oneCh[-self.equ_window_size+1:]

    def createEqualizerPlots(self):
        path = "../GUI/qml/images"
