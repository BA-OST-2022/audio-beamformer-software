###############################################################################
# file    FPGAControl.py
###############################################################################
# brief   This module controls the physical connection with the FPGAs
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-05-08
###############################################################################
# MIT License
#
# Copyright (c) 2022 ICAI Interdisciplinary Center for Artificial Intelligence
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

import sys
import time
import numpy as np

DEBUG = False
LINUX = (sys.platform == 'linux')

if LINUX:
    import spidev
    import RPi.GPIO as GPIO 


class FPGAControl():
    def __init__(self, channel_count, channel_per_fpga):
        self.MAM = 0
        self.DSB = 1
        
        self._spiBus = 0                      # Physical SPI-Bus Interface
        self._spiFreq = 1000000               # Interface Frequency in Hz
        self._spiCs = 0                       # SPI-Device Chip-Select
        self._syncPin = 17                    # Raspberry Pi GPIO Number
        
        self._initialized = False
        self._channel_per_fpga = channel_per_fpga
        self._channel_count = channel_count
        self._fpga_count = int(np.ceil(channel_count / channel_per_fpga))
        self._gain = np.ones(self._channel_count)
        self._delay = np.ones(self._channel_count) * 0
        self._enable_channel = [False] * self._channel_count
        self._interpolation = 64              # Interpolation: 1, 2, 4, ..., 64
        self._modulation_type = self.DSB      # Modulation type: DSB, MAM
        self._sigma_delta_coeff = 2**13       # coeff value: 2^0 ... 2^15
        self._sigma_delta_freq = 6.25E6       # Frequency in Hz
        self._tick_length = 2 / self._sigma_delta_freq
        self._spi = None
    
    
    def __del__ (self):
        self.end()
       
        
    def begin(self):
        if not self._initialized:
            self._initialized = True
            if LINUX:
                self._spi = spidev.SpiDev()
                self._spi.open(bus=self._spiBus, device=self._spiCs)
                self._spi.max_speed_hz = self._spiFreq
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)        # Use RaspberryPi GPIO Numbers
                GPIO.setup(self._syncPin, GPIO.OUT, initial=GPIO.LOW)
                time.sleep(0.01)              # 10ms Sync-Pulse
                GPIO.output(self._syncPin, GPIO.HIGH)
            self.update()
    
    
    def end(self):
        if(self._initialized):
            self._enable_channel = [False] * self._channel_count
            self.update()
            self._initialized = False
            if LINUX:
                self._spi.close()
    
    
    def enableChannels(self, channels):
        if(len(channels) != self._channel_count):
            raise ValueError("Channel count does not match")
        self._enable_channel = channels
    
    
    def setChannelGain(self, gain):
        if(len(gain) != self._channel_count):
            raise ValueError("Channel count does not match")
        if not any([-1 <= g <= 1 for g in gain]):
            raise ValueError("Gain between -1 and 1")
        self._gain = gain
    
    
    def setChannelDelay(self, delay):
        if(len(delay) != self._channel_count):
            raise ValueError("Channel count does not match")
        if not any([0 <= d <= self._tick_length * 2046 for d in delay]):
            raise ValueError(f"Delay between 0 and {self._tick_length*2046} s")
        self._delay = delay
        
    
    def getMaxChannelDelay(self):
        return self._tick_length * 2046
    
    
    def setInterpolation(self, interpolation):
        if not interpolation in [1, 2, 4, 8, 16, 32, 64]:
            raise ValueError("Interpolation out of bound")
        self._interpolation = interpolation
    
    
    def setModulationType(self, modType):
        if not modType in [self.MAM, self.DSB]:
            raise ValueError("Modulation type not avaiable")
        self._modulation_type = modType
        
        
    def setSigmaDeltaCoeff(self, coeff):
        if not (1 <= coeff <= 32767):
            raise ValueError("Sigma delta coeff must be between 1 and 32767")
        self._sigma_delta_coeff = coeff
    
        
    def update(self):
        if self._initialized:
            settings = 0x00                       # Bit [7:4] free 
            settings |= (int(7 - np.log2(self._interpolation)) & 0x03)
            settings |= (int(self._modulation_type) & 0x01) << 3
            
            sigma_delta = np.array([i for i in (self._sigma_delta_coeff).
                                    to_bytes(2, "big")])
            
            gain_int = (self._gain * 32767).astype(int)
            gains = np.array([i for gain in gain_int for i in int(gain).
                              to_bytes(2, "big", signed=True)])
            delay_count = (self._delay / self._tick_length).astype(int)
            delay_count = np.array([i for d in delay_count for i in int(d).
                                    to_bytes(2, "big", signed=True)])
            
            spi_data = []
            for fpga in range(self._fpga_count):
                spi_data.append(settings)
                spi_data.append(int(sigma_delta[0]))
                spi_data.append(int(sigma_delta[1]))
                enable_list = self._enable_channel[fpga * self._channel_per_fpga:(fpga+1) * self._channel_per_fpga]
                enable = sum([2**i*int(value) for i,value in
                            enumerate(enable_list)]).to_bytes(2, "big")
                spi_data.append(int(enable[0]))
                spi_data.append(int(enable[1]))
                for channel in range(self._channel_per_fpga):
                    if((channel + 1) * (fpga + 1) > self._channel_count):
                        break
                    spi_data.append(int(delay_count[channel * 2]))
                    spi_data.append(int(delay_count[channel * 2 + 1]))
                    spi_data.append(int(gains[channel * 2 + 0]))
                    spi_data.append(int(gains[channel * 2 + 1]))
    
            if LINUX:
                self._spi.writebytes(spi_data[::-1])
            if DEBUG:
                print(spi_data)
        
 
fpgaControl = FPGAControl(channel_count=19, channel_per_fpga=10)       
 
if __name__ == '__main__':
    enable = [False] * 19
    enable[0] = True
    fpgaControl.enableChannels(enable)
    fpgaControl.begin()
    
    time.sleep(3)
    fpgaControl.end()
    