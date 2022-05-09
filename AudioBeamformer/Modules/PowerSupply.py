###############################################################################
# file    PowerSupply.py
###############################################################################
# brief   This module controls the physical volume and power supply 
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-05-04
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

DEBUG = False
LINUX = (sys.platform == 'linux')

if LINUX:
    import spidev
    import RPi.GPIO as GPIO


class PowerSupply():
    def __init__(self):
        self._spiBus = 4                      # Physical SPI-Bus Interface
        self._spiFreq = 8000000               # Interface Frequency in Hz
        self._spiCs = 1                       # SPI-Device Chip-Select
        self._hvEnPin = 27                    # Raspberry Pi GPIO Number
        
        vRef = 1.23                           # Reference Voltage in V
        rTop = 100E3                          # Top Resistor in Ohm
        rBot = 3.01E3                         # Bottom Resistor in Ohm
        rPot = 10E3                           # Dig. Pot. Resistance in Ohm
        
        self._initialized = False
        self._maxVolume = 1.0                 # Default is max volume
        self._vMax = (vRef / rBot) * (rBot + rTop)
        self._vMin = (vRef / (rBot + rPot)) * (rBot + rPot + rTop)
        
    
    def __del__(self):
        self.end()
    
    
    def begin(self):
        if not self._initialized:
            self._initialized = True
            if LINUX:
                self._spi = spidev.SpiDev()
                self._spi.open(bus=self._spiBus, device=self._spiCs)
                self._spi.max_speed_hz = self._spiFreq
                GPIO.setmode(GPIO.BCM)        # Use RaspberryPi GPIO Numbers
                GPIO.setup(self._hvEnPin, GPIO.OUT, initial=GPIO.HIGH)
                self.enableOutput(False)
                self.setVolume(0.0)
                
    
    def end(self):
        self.enableOutput(False)
        if(self._initialized):
            self._initialized = False
            if LINUX:
                self._spi.close()
    
    
    def enableOutput(self, state):
        if LINUX:
            if(state):
                GPIO.output(self._syncPin, GPIO.LOW)
            else:
                GPIO.output(self._syncPin, GPIO.HIGH)
    
    
    def setVolume(self, volume):
        if not (0 <= volume <= 1.0):
            raise ValueError("Volume out of bound: 0.0 ... 1.0")

        volume = min(volume, self._maxVolume)
        vTarget = self._vMin + (self._vMax - self._vMin) * volume
        if DEBUG:
            print(f"Output Voltage: {vTarget:.01f} V")
        if LINUX:
            self._spi.writebytes([0x11, int(volume * 255)]) # TODO: check if potentiometer polarity is correct 

    
    def setMaxVolume(self, maxVolume):
        if not (0 <= maxVolume <= 1.0):
            raise ValueError("Max Volume out of bound: 0.0 ... 1.0")
        self._maxVolume = maxVolume
        


powerSupply = PowerSupply()

if __name__ == '__main__':
    powerSupply.begin()
    powerSupply.setVolume(0.5)
    powerSupply.enableOutput(True)
    
    import time
    time.sleep(3)
    powerSupply.enableOutput(False)
    powerSupply.end()
    
    