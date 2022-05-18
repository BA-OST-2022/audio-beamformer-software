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
from pathlib import Path

DEBUG = False

class Beamsteering():
    def __init__(self,
                 sensors = None,
                 facetracking = None,
                 fpgaControl = None,
                 leds=None):
        # Module init
        self._fpga_controller = fpgaControl
        self._sensors = sensors
        self._facetracking = facetracking
        self._leds = leds
        # Constants
        self.__distance = 0.01475
        self.__row_count = 19
        #   Camera angle in degree
        self.__max_angle_camera = 40
        # Var init
        self._initialized = False
        self._runThread = False
        self._updateRate = 2
        self._ledsUpdateRate = 20
        self._timeTemp = 0
        # Beamsteering 
        self._beamsteeringEnable = True
        self._beamsteeringSources = {0: "Camera", 1: "Manual", 2: "Pattern"}
        self._currSteerSource = 0
        self._angleToSteer = 0
        self._angleToSteer_faceTracking = 0
        self._angleToSteer_manual = 0
        #   Pattern
        self._beamsteeringPattern = {"Pattern 1": (-45,45,10,1)}
        self._activePattern = np.linspace(-45,45,10)
        self._currentPattern = 0
        self._PatternHoldTime = 1
        # Window
        self.__window_types = {"Rectangle": self.rectWindow(),
                             "Cosine": self.cosineWindow(),
                             "Hann": self.hannWindow(),
                             "Hamming": self.hammingWindow(),
                             "Blackman": self.blackmanWindow(),
                             "Dolph-Chebyshev": self.chebyWindow()}
        self._activeWindow = "Rectangle"
        # LED 
        self._start_color = np.array([1,0.4,0])
        self._end_color = np.array([0.05,0.2,0.95])
        #self._start_color = np.array([1,0.3,0])
        #self._end_color = np.array([0.5,0.87,0.92])
        # Mute channel
        self._enableChannel = np.ones(self.__row_count)


    def begin(self):
         if not self._initialized:
            self._initialized = True
            self._runThread = True
            self.update()

    def end(self):
        self._runThread = False

    def update(self):
        if(self._initialized):
            if(self._runThread):
                # Update rate for the LEDS
                threading.Timer(1.0 / self._ledsUpdateRate, self.update).start()
                self.setLEDS()
                # Update rate for the angle
                if(time.time() - self._timeTemp > 1 / self._updateRate):
                    self._timeTemp = time.time()
                    if(self._beamsteeringEnable):
                        self.setAngle()
                        self.calculateDelay()

    def enableBeamsteering(self,value):
        self._beamsteeringEnable = value
        # If beamsteering is being turne of set angle to zero and calculate delay
        if value==0:
            self._angleToSteer = 0
            self.calculateDelay()

    def setBeamsteeringSource(self, source):
        self._currSteerSource = source

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
        # TODO Measure camera angle
        max_image_size_x = 680
        
        angle = 0
        # If facetracking found
        if self._facetracking:
            # Get position from facetracking
            position = self._facetracking.getFocusLocation()
            # If position avaiable
            if len(position) > 1:
                # Zero at center
                x_pos = max_image_size_x/2-position[0]
                # Calculate angle
                distance = max_image_size_x / (2*np.tan(self.__max_angle_camera/ 180 * np.pi))
                angle = np.arctan(x_pos / distance)* 180 / np.pi
        return angle

    def setLEDS(self):
        #TODO Check if works with self.__max_angle_camera
        min_angle = -45
        max_angle = 45
        # Where should the peak be
        peak = self._angleToSteer / (max_angle - min_angle) * self.__row_count  + self.__row_count // 2
        # Calc difference vector and scale
        color_gradient = (self._end_color - self._start_color)/ (np.ceil(np.abs(peak - self.__row_count // 2)) + self.__row_count // 2)
        leds_display = np.ones((self.__row_count,3))
        for i,elem in enumerate(leds_display):
            distance = np.abs(i - peak)
            leds_display[i,:] = self._start_color + distance * color_gradient
        self._leds.setChannelColors(np.abs(leds_display))
        
        if self._currSteerSource != 0:  #Turn off LEDs if not in camera mode
            self._leds.setCameraAnimation(self._leds.OFF)
        else:
            if self._facetracking.getDetectionCount() == 0:
                self._leds.setCameraAnimation(self._leds.SEARCHING)
            else:
                self._leds.setCameraAnimation(self._leds.TRACKING)
    

    def setAngle(self):
        # Face Tracking
        if (self._currSteerSource == 0):
            self._angleToSteer = self._calc_angle_face() 
        # Manual
        elif (self._currSteerSource == 1):
            self._angleToSteer = self._angleToSteer_manual
        # Pattern
        else:
            self._angleToSteer = self._activePattern[int(time.time()/self._PatternHoldTime % len(self._activePattern))]
    
    def calculateDelay(self):
        # If angle below 1 degree set delay to zero
        if abs(self._angleToSteer) >= 1:
            delay = np.arange(self.__row_count) * (self.__distance / self.getSpeedOfSound()) * np.sin(self._angleToSteer/180*np.pi)
            # Make all delays positive
            if (np.sin(self._angleToSteer/180*np.pi) < 0):
                delay = delay[::-1] * -1
        else:
            delay = np.zeros(self.__row_count)
        
        # Check if delay allowed
        maxDelay = self._fpga_controller.getMaxChannelDelay()
        if np.any(delay >= maxDelay):
            print(f"Wrong angle: {delay}")
        
        delay = np.clip(delay, 0, maxDelay)
        self._fpga_controller.setChannelDelay(delay)
        self._fpga_controller.update()
    
    def calculateGains(self):
        gains = self.__window_types[self._activeWindow]
        if not DEBUG:
            self._fpga_controller.setChannelGain(np.array(gains))
            self._fpga_controller.update()
        else:
            print(f"Gains: {np.array(gains)}")

    def getSpeedOfSound(self):
        if self._sensors:
            temp = self._sensors.getTemperature(self._sensors.SRC_AMBIENT)
            if not np.isnan(temp):
                return 331.5 + 0.607 * temp
            return 343.3

    def setWindowProfile(self, profile):
        self._activeWindow = self.__window_list[profile]
        self.calculateGains()

    def getWindowProfileList(self):
        self.__window_list = list(self.__window_types.keys())
        return list(self.__window_types.keys())

    # Window types

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
        