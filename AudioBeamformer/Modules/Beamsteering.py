###############################################################################
# file    AudioProcessing.py
###############################################################################
# brief   This module handels the beamsteering for the audio-beamformer
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
import threading
import numpy 
class Beamsteering():
    def __init__(self,
                 spi_interface,
                 temperature=22,
                 row_count=6,
                 distance=14.75e-3):
        self._beamsteeringEnable = False
        self._beamsteeringSources = {0: "Face", 1: "Manual", 2: "Pattern"}
        self._activeSource = 0
        self._beamsteeringPattern = {0: (-45,45,10,1)}
        self._activePattern = 0 
        self._activeWindow = "rect"
        self._fpga_control = 
        self.spi_interface = spi_interface
        self.temperature = temperature
        self.speed_of_sound = 331.5 + 0.607*temperature
        self.row_count = row_count
        self.distance = distance
        self.window_types = {"rect": self.rectWindow(),
                             "cosine": self.cosineWindow(),
                             "hann": self.hannWindow(),
                             "hamming": self.hammingWindow(),
                             "blackman": self.blackmanWindow(),
                             "cheby": self.chebyWindow()}
        self._updateRate = 30
        self._initialized = False

    def begin(self):
         if not self._initialized:
            self._initialized = True
            self._updateRate = framerate
            self._runThread = True
            self.update()

    def end(self):
        self._runThread = False

    def update(self):
        if(self._initialized):
            if(self._runThread):
                threading.Timer(1.0 / self._updateRate, self.update).start()
    
    def rectWindow(self):
        gains = [1] * self.row_count
        return gains

    def cosineWindow(self):
        gains = np.sin(np.arange(self.row_count)*np.pi/(self.row_count-1))
        gains /= max(gains)
        return gains

    def hannWindow(self):
        gains = np.sin(np.arange(self.row_count)*np.pi/(self.row_count-1))**2
        gains /= max(gains)
        return gains

    def hammingWindow(self):
        gains = 0.54 - 0.46 * np.cos(2*np.arange(self.row_count)*np.pi/(self.row_count-1))
        gains /= max(gains)
        return gains

    def blackmanWindow(self):
        gains = 0.42 - 0.5 * np.cos(2*np.arange(self.row_count)*np.pi/(self.row_count-1)) + 0.08 * np.cos(4*np.arange(self.row_count)*np.pi/(self.row_count-1))
        gains /= max(gains)
        return gains

    def chebyWindow(self):
        alpha = 5
        beta = np.cosh(1/self.row_count*np.arccosh(10**alpha))
        freq_dom = np.array([self.chebyPol(beta*np.cos(np.pi * val /(self.row_count+1)))/self.chebyPol(beta) for val in np.arange(self.row_count)])
        gains = np.real(np.fft.fftshift(np.fft.ifft(freq_dom)))
        gains /= max(gains)
        return gains

    def chebyPol(self, val):
        N = self.row_count
        if val <= -1:
            return (-1)**N*np.cosh(N*np.arccosh(-val))
        elif val >= 1:
            return np.cosh(N*np.arccosh(val))
        else:
            return np.cos(N*np.arccos(val))

    def steerAngle(self, angle):
        delay = np.arange(self.row_count) * self.distance / self.speed_of_sound * np.sin(angle/180*np.pi)
        if (np.sin(angle/180*np.pi) < 0):
            delay = delay[::-1] * -1
        self.spi_interface.delay = delay
        self.spi_interface.updateSPI()
        