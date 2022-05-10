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
import numpy as np

class Beamsteering():
    def __init__(self,
                 fpga_controll,
                 sensors,
                 facetracking):
        self._beamsteeringEnable = False
        self._beamsteeringSources = {0: "Camera", 1: "Manual", 2: "Pattern"}
        self._activeSource = 0
        self._beamsteeringPattern = {0: (-45,45,10,1)}
        self._activePattern = np.linspace(-45,45,10)
        self._activeWindow = "rect"
        self._fpga_controlller = fpga_controll
        self._sensors = sensors
        self._facetracking = facetracking
        self._angleToSteer = 0
        self._angleToSteer_faceTracking = 0
        self._angleToSteer_manual = 0
        self._currentPattern = 0
        self._PatternHoldTime = 1
        self.window_types = {"rect": self.rectWindow(),
                             "cosine": self.cosineWindow(),
                             "hann": self.hannWindow(),
                             "hamming": self.hammingWindow(),
                             "blackman": self.blackmanWindow(),
                             "cheby": self.chebyWindow()}
        self._initialized = False

    def begin(self):
         if not self._initialized:
            self._initialized = True
            self._updateRate = 30
            self._runThread = True
            self.update()

    def end(self):
        self._runThread = False

    def update(self):
        if(self._initialized):
            if(self._runThread):
                threading.Timer(1.0 / self._updateRate, self.update).start()
                self.setAngle()

    def setBeamsteeringSource(self, source):
        self._activeSource = source

    def setBeamsteeringAngle(self, angle):
        self._angleToSteer_manual = angle

    def setBeamsteeringPattern(self, pattern):  
        min_angle, max_angle, steps, time = self._beamsteeringPattern[pattern]
        self._activePattern = np.linspace(min_angle,max_angle, steps)
        self._PatternHoldTime = time

    def setAngle(self):
        # Face Tracking
        if (self._activeSource == 0):
            self._angleToSteer = self._facetracking.angle() # Needs to be adjusted
        # Manual
        elif (self._activeSource == 1):
            self._angleToSteer = self._angleToSteer_manual
        #else:
        #    self._angleToSteer = 

    
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
        