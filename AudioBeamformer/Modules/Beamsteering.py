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
import time

DEBUG = False

class Beamsteering():
    def __init__(self,
                 sensors = None,
                 facetracking = None,
                 fpgaControl = None):
        self._beamsteeringEnable = False
        self._beamsteeringSources = {0: "Camera", 1: "Manual", 2: "Pattern"}
        self._activeSource = 0
        self._beamsteeringPattern = {"Pattern 1": (-45,45,10,1)}
        self._activePattern = np.linspace(-45,45,10)
        self._activeWindow = "rect"
        self._fpga_controller = fpgaControl
        self._sensors = sensors
        self._facetracking = facetracking
        self._angleToSteer = 0
        self._angleToSteer_faceTracking = 0
        self._angleToSteer_manual = 0
        self._currentPattern = 0
        self._PatternHoldTime = 1
        self._enableChannel = np.ones(19)
        self.__window_types = {"rect": self.rectWindow,
                             "cosine": self.cosineWindow,
                             "hann": self.hannWindow,
                             "hamming": self.hammingWindow,
                             "blackman": self.blackmanWindow,
                             "cheby": self.chebyWindow}
        self._initialized = False
        self.__distance = 0.01475
        self.__speed_of_sound = 343.2
        self.__row_count = 19

    def begin(self):
         if not self._initialized:
            self._initialized = True
            self._updateRate = 2
            self._runThread = True
            self.update()

    def end(self):
        self._runThread = False

    def update(self):
        if(self._initialized):
            if(self._runThread):
                threading.Timer(1.0 / self._updateRate, self.update).start()
                if(self._beamsteeringEnable):
                    self.setAngle()
                    self.calculateSpeedOfSound()
                    self.calculateDelay()

    def enableBeamsteering(self,value):
        self._beamsteeringEnable = value
        if value==0:
            self._angleToSteer = 0
            self.calculateDelay()

    def setBeamsteeringSource(self, source):
        self._activeSource = source

    def setBeamsteeringAngle(self, angle):
        self._angleToSteer_manual = angle

    def setBeamsteeringPattern(self, pattern):  
        min_angle, max_angle, steps, time = self._beamsteeringPattern[self._beamsteeringPattern_list[pattern]]
        self._activePattern = np.linspace(min_angle,max_angle, steps)
        self._PatternHoldTime = time

    def getBeamsteeringPattern(self):
        self._beamsteeringPattern_list = list(self._beamsteeringPattern.keys())
        return list(self._beamsteeringPattern.keys())

    def setChannelEnable(self,list):
        self._enableChannel = np.array(list)
        self._fpga_controller.enableChannels(list)
        self._fpga_controller.update()
    
    def _calc_angle_face(self):
        return 0

    def setAngle(self):
        # Face Tracking
        if (self._activeSource == 0):
            self._angleToSteer = self._calc_angle_face() # Needs to be adjusted
        # Manual
        elif (self._activeSource == 1):
            self._angleToSteer = self._angleToSteer_manual
        else:
            self._angleToSteer = self._activePattern[int(time.time()/self._PatternHoldTime % len(self._activePattern))]

    def calculateDelay(self):
        delay = np.arange(self.__row_count) * self.__distance / self.__speed_of_sound * np.sin(self._angleToSteer/180*np.pi)
        print(delay)
        if (np.sin(self._angleToSteer/180*np.pi) < 0):
            delay = delay[::-1] * -1
        if not DEBUG:
            self._fpga_controller.setChannelDelay(delay)
            self._fpga_controller.update()
        else:
            print(delay[0])
            print(f"Delay: {delay}")
    
    def calculateGains(self):
        gains = self.__window_types[self._activeWindow]()
        if not DEBUG:
            self._fpga_controller.setChannelGain(np.array(gains))
            self._fpga_controller.update()
        else:
            print(f"Gains: {np.array(gains)}")

    def calculateSpeedOfSound(self):
        if not self._sensors == None:
            self.__speed_of_sound = 331.5 + 0.607*self._sensors.getTemperature("Ambient")
            return self.__speed_of_sound
        else:
            return 343.3
    
    def getWindowProfileList(self):
        self.__window_list = list(self.__window_types.keys())
        return list(self.__window_types.keys())

    def setWindowProfile(self, profile):
        self._activeWindow = self.__window_list[profile]
        self.calculateGains()

    def rectWindow(self):
        gains = [1] * self.__row_count
        return gains

    def cosineWindow(self):
        gains = np.sin(np.arange(self.__row_count)*np.pi/(self.__row_count-1))
        gains /= max(gains)
        return gains

    def hannWindow(self):
        gains = np.sin(np.arange(self.__row_count)*np.pi/(self.__row_count-1))**2
        gains /= max(gains)
        return gains

    def hammingWindow(self):
        gains = 0.54 - 0.46 * np.cos(2*np.arange(self.__row_count)*np.pi/(self.__row_count-1))
        gains /= max(gains)
        return gains

    def blackmanWindow(self):
        gains = 0.42 - 0.5 * np.cos(2*np.arange(self.__row_count)*np.pi/(self.__row_count-1)) + 0.08 * np.cos(4*np.arange(self.__row_count)*np.pi/(self.__row_count-1))
        gains /= max(gains)
        return gains

    def chebyWindow(self):
        alpha = 5
        beta = np.cosh(1/self.__row_count*np.arccosh(10**alpha))
        freq_dom = np.array([self.chebyPol(beta*np.cos(np.pi * val /(self.__row_count+1)))/self.chebyPol(beta) for val in np.arange(self.__row_count)])
        gains = np.real(np.fft.fftshift(np.fft.ifft(freq_dom)))
        gains /= max(gains)
        return gains

    def chebyPol(self, val):
        N = self.__row_count
        if val <= -1:
            return (-1)**N*np.cosh(N*np.arccosh(-val))
        elif val >= 1:
            return np.cosh(N*np.arccosh(val))
        else:
            return np.cos(N*np.arccos(val))
        