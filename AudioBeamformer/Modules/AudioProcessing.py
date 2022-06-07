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
import matplotlib.pyplot as plt
from pathlib import Path
import shutil
import filecmp

DEBUG = False
LINUX = (sys.platform == 'linux')
sys.path.insert(0, os.path.dirname(__file__)) 
sys.path.insert(0, os.path.dirname(__file__) + "/Modules")

from AudioPlayer import AudioPlayer
from Plotter import EqualizerPlotter




class AudioProcessing:
    def __init__(self, fpgaControl = None):
        # Adjustable values
        self._chunk_size = 8192
        self._samplerate = 44100
        self.equ_window_size = 123
        self.__black_list_input_device = ["pulse","loopin","default"]
        self.__modulation_dict = {0: self.AMModulation, 1: self.MAMModulation}
        self._fpga_controller = fpgaControl
        # Device index
        channels = self.getChannels()
        if LINUX:  
            # If system is linux then the loopback and the audio beamformer 
            # are the initial input/output devices
            self._output_device = [i[1] for i in channels].index('snd_rpi_hifiberry_dac: HifiBerry DAC HiFi pcm5102a-hifi-0 (hw:0,0)')
            inputDeviceName = [s for s in [i[1] for i in channels] if s.startswith('Loopback') and s.endswith(',1)')][0]
            self._input_device = [i[1] for i in channels].index(inputDeviceName)
        else:
            try:
                self._output_device = [i[1] for i in channels].index('Microsoft Sound Mapper - Output')
                self._input_device = [i[1] for i in channels].index('Microsoft Sound Mapper - Input')
            except Exception:
                self._output_device = None
                self._input_device = None
                print("No Input or Output Device detected\n")
                
        # Start values
        self._tot_gain = 1.0
        self._equalizer_enable = True
        self._modulation_index = 1
        self._mam_gain = 0.2
        self._enable_interpolation = True
        self._interpolation_factor = 64
        self._stream = None
        self.__previousWindow = np.zeros(self.equ_window_size - 1,dtype=np.float32)
        self.__current_source_level = 0
        self.__source_dict = {}
        self.__equalizer_profile_list = {}
        self.__equalizerList = []
        self.__equalizer_tabs = []
        self.__stream_running = False
        self._enableMagic = False
        self._enableMute = True
        self._outputGain = 0.0
        self._player = None
        self._plotter = EqualizerPlotter(285, int(285 * 0.517), self._samplerate)
        
        # Equalizer initialization
        createPlots = False
        self.__equalier_dict_path = os.path.dirname(os.path.realpath(__file__)) + "/Files/equalizer_dict.txt"
        tempPath = self.__equalier_dict_path.rsplit('.', 1)[0] + ".tmp"
        if not Path(tempPath).is_file():  # Create initial backup file
            createPlots = True
            shutil.copyfile(self.__equalier_dict_path, tempPath)
        if not filecmp.cmp(self.__equalier_dict_path, tempPath): # Check if temp file is diffrent to actual file
            createPlots = True
            shutil.copyfile(self.__equalier_dict_path, tempPath)
       
        with open(self.__equalier_dict_path) as f:
            for i,line in enumerate(f.readlines()):
                line_tupel = ast.literal_eval(line)
                self.__equalizerList.append(line_tupel[0])
                self.__equalizer_profile_list[line_tupel[0]] = line_tupel[1]
                taps = self.equalizer(line_tupel[1])
                if createPlots:
                    self.createEqualizerPlot(i, taps)
                self.__equalizer_tabs.append(taps)
                
        self._equalizer_filter = np.ones(self.equ_window_size)

    def begin(self):
            self.getChannels()
            self.setupStream()
            self.startStream()

    def end(self):
        self.endStream()

    def setupStream(self):
        try:
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
        except Exception:
            self._stream = None



    def startStream(self):
        if self._stream:
            self._stream.start()
            self.__stream_running = True

    def endStream(self):
        if self._stream:
            self._stream.close()
            self.__stream_running = False

    def getEqualizerList(self):
        equalizer_list = []
        for key in self.__equalizer_profile_list.keys():
            y_val = []
            x_val = []
            for freq_band in self.__equalizer_profile_list[key].keys():
                x_val.append(freq_band[0])
                x_val.append(freq_band[1])
                y_val.append(self.__equalizer_profile_list[key][freq_band]["band_gain"])
                y_val.append(self.__equalizer_profile_list[key][freq_band]["band_gain"])
            equalizer_list.append([x_val,y_val])
        return equalizer_list


    def getChannels(self):
        channelInfo = []
        sd._terminate()
        sd._initialize()
        for p,i in enumerate(sd.query_devices()):
            channelInfo.append((p,
                                i['name'],
                                i['max_input_channels'],
                                i['hostapi'],
                                i['max_output_channels']))
        return channelInfo
    
    def printChannels(self):
        for i, p in enumerate(self.getChannels()):
            name = p[1].replace("\r\n", "")
            print(f"{i:2} - API: {p[3]}, In: {p[2]}, Out: {p[4]}, Name: {name}")
        print()

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
                        if ((device["name"].startswith('Loopback') and device["name"].endswith(',1)'))
                            or (device["name"] == "Microsoft Sound Mapper - Input")):
                            sourceList.append(default_val)
                        else:
                            sourceList.append(device["name"])
        if sourceList:
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
        try:
            if source_index < len(self.__sourceIndexList):
                self._input_device = self.__sourceIndexList[source_index]
            else:
                self._input_device = self.__sourceIndexList[0]
        except IndexError:
            print("Source is no more available")
       
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
        return taps

    def createEqualizerPlot(self, profile, taps):
        w,h = freqz(taps, worN=10000)
        path = Path(os.path.dirname(__file__)).parents[0] / f"GUI/qml/images/eq_{profile}.svg"
        self._plotter.generatePlot(w, np.abs(h), path)

    def setEqualizerProfile(self, profile):
        self._equalizer_filter = self.__equalizer_tabs[profile]
        #self.createEqualizerPlot(profile, self._equalizer_filter)

    def enableInterpolation(self,enable):
        if self._fpga_controller:
            if enable:
                self._fpga_controller.setInterpolation(self._interpolation_factor)
            else:
                self._fpga_controller.setInterpolation(1)
            self._fpga_controller.update()

    def setInterpolationFactor(self,factor):
        self._interpolation_factor = factor

    def setModulationType(self, modType):
        self._modulation_index = modType
        if self._fpga_controller:
            if self._modulation_index == 0:     # AM
                self._fpga_controller.setModulationType(self._fpga_controller.DSB)
            elif self._modulation_index == 1:   # MAM
                self._fpga_controller.setModulationType(self._fpga_controller.MAM)
            self._fpga_controller.update()

    
    def setMAMMix(self,gain):
        self._mam_gain = gain

    def AMModulation(self,data):
        return data

    def MAMModulation(self,data):
        data = data / np.iinfo(np.int32).max
        data_out = 1 - 1/2*data**2 - 1/8*data**4
        return data_out * np.iinfo(np.int32).max  * self._mam_gain
    
    def enableMagic(self, state):
        self._enableMagic = state
        if(state):
            path = os.path.join(os.path.dirname(__file__), "Files/magic.wav")
            self._player = AudioPlayer(sampleRate=self._samplerate,
                                       blockSize=self._chunk_size)
            self._player.begin(path)
        else:
            if self._player:
                self._player.end()
                self._player = None
                
    def enableMute(self, state):
        self._enableMute = state
        
    def setOutputGain(self, gain):
        self._outputGain = gain
        

    def callback(self, indata, outdata, frames, time, status):
        if status:
            print(status)
            
        print(np.type(indata), indata)
        indata_oneCh = np.float32(indata[:,0]) * self._tot_gain 
        self.setSourceLevel(indata_oneCh)
        print(np.type(indata_oneCh), indata_oneCh)
        
        outdata_oneCh = indata_oneCh
        if self._equalizer_enable:
            indata_oneCh = np.hstack((self.__previousWindow,
                                    indata_oneCh))  # This is longer than indata[:,0]
            
            outdata_oneCh = np.convolve(indata_oneCh,
                                        self._equalizer_filter,
                                        "valid")
            outdata_oneCh = np.float32(outdata_oneCh)

        if self._enableMagic:
            data = self._player.getData()[:,0]
            if np.shape(data) == np.shape(outdata_oneCh):
                outdata_oneCh = data
            else:
                outdata_oneCh = np.zeros_like(indata[:,0])
                print("No data yet to play")
                
        
        outdata_oneCh *= self._outputGain
        if self._enableMute:
            outdata_oneCh = np.zeros_like(indata[:,0])
        print(outdata_oneCh)
            
        # Modulation
        second_channel_data = self.__modulation_dict[self._modulation_index](outdata_oneCh)
        # Stich output together
        outdata[:] = np.int32(np.column_stack((outdata_oneCh, second_channel_data)))
        self.__previousWindow = indata_oneCh[-self.equ_window_size+1:]


if __name__ == '__main__':
    import time
    audio_processing = AudioProcessing()
    audio_processing.printChannels()
    print(audio_processing.getSourceList())
    # audio_processing.enableMagic(True)
    audio_processing.begin()
    audio_processing.enableMute(False)
    audio_processing.setEqualizerProfile(1)
    time.sleep(10)
    audio_processing.end()
    

