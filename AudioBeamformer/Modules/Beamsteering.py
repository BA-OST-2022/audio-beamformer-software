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

import os
import ast
import threading
import numpy as np
import time
from pathlib import Path
from Plotter import WindowPlotter
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
        
        #   LED 
        self._COLOR_GRAD_PEAK = np.array([1.00, 0.40, 0.00])
        self._COLOR_GRAD_LOW  = np.array([0.05, 0.20, 0.95])
        self._COLOR_DEAFULT   = np.array([0.50, 0.87, 0.92])
        
        #   Camera angle in degree
        self.__max_angle_camera = 40
        
        # Var init
        self._initialized = False
        self._runThread = False
        self._updateRate = 2
        self._ledsUpdateRate = 12
        self._timeTemp = 0
        
        # Beamsteering 
        self._beamsteeringEnable = False
        self._beamsteeringSources = {0: "Camera", 1: "Manual", 2: "Pattern"}
        self._currSteerSource = 0
        self._angleToSteer = 0
        self._angleToSteer_faceTracking = 0
        self._angleToSteer_manual = 0
        self._beamfocusing_enable = False
        self.__beamfocusing_radius = 3 # Beamfocusing radius is set to three 
        #   Pattern
        self._beamsteeringPattern = {}
        self.__pattern_dict_path = os.path.dirname(os.path.realpath(__file__)) + "/Files/beamsteering_pattern.txt"
        with open(self.__pattern_dict_path, encoding="utf-8") as f:
            for line in f.readlines():
                line_tupel = ast.literal_eval(line)
                self._beamsteeringPattern[line_tupel[0]] = line_tupel[1:]
        self.setBeamsteeringPattern(0)
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
        self._enableChannel = np.ones(self.__row_count)
        self._gains = np.ones(self.__row_count)
        self._plotter = WindowPlotter(250, int(250 * 0.517))
        self.generatePlot()

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
            else:
                return
            
            self.setAngle()
            self.setLEDS()
            # Update rate for the angle
            if(time.time() - self._timeTemp > 1 / self._updateRate):
                self._timeTemp = time.time()
                if(self._beamsteeringEnable or self._beamfocusing_enable):
                    
                    self.calculateDelay()

    def generatePlot(self):
        for i,elem in enumerate(self.__window_types.keys()):
            path = Path(os.path.dirname(__file__)).parents[0] / f"GUI/qml/images/window_{i}.svg"
            taps = self.__window_types[elem]
            self._plotter.generatePlot(taps,path)

    def enableBeamsteering(self,value):
        self._beamsteeringEnable = value
        # If beamsteering is being turne of set angle to zero and calculate delay
        if value==0:
            self._angleToSteer = 0
            self.calculateDelay()

    def setBeamsteeringSource(self, source):
        self._currSteerSource = source

    def enableBeamfocusing(self,enable):
        self._beamfocusing_enable = enable

    def setBeamfocusingRadius(self,radius):
        self.__beamfocusing_radius = radius

    def setBeamsteeringAngle(self, angle):
        self._angleToSteer_manual = angle

    def setBeamsteeringPattern(self, pattern):
        name = list(self._beamsteeringPattern.keys())[pattern]
        min_angle, max_angle, steps, time = self._beamsteeringPattern[name]
        self._activePattern = np.linspace(min_angle,max_angle, steps)
        self._PatternHoldTime = time

    def getBeamsteeringPattern(self):
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
        color_gradient = (self._COLOR_GRAD_LOW - self._COLOR_GRAD_PEAK)/ (np.ceil(np.abs(peak - self.__row_count // 2)) + self.__row_count // 2)
        leds_display = np.ones((self.__row_count,3))
        if self._beamsteeringEnable:
            for i,elem in enumerate(leds_display):
                distance = np.abs(i - peak)
                leds_display[i,:] = self._COLOR_GRAD_PEAK + distance * color_gradient
            leds_display = np.abs(leds_display)
        else:
            leds_display *= self._COLOR_DEAFULT
        
        # Window Brightness Overlay
        leds_display *= np.abs(np.column_stack((self._gains,self._gains, self._gains)))
        # Channel Enable Overlay
        leds_display *= np.column_stack((self._enableChannel,self._enableChannel, self._enableChannel))

        self._leds.setChannelColors(leds_display)            
        
        if self._currSteerSource != 0:  # Turn off LEDs if not in camera mode
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
        # Check if delay allowed
        maxDelay = self._fpga_controller.getMaxChannelDelay()
        # If angle below 1 degree set delay to zero
        if abs(self._angleToSteer) >= 1 and self._beamsteeringEnable:
            delay = np.arange(self.__row_count) * (self.__distance / self.getSpeedOfSound()) * np.sin(self._angleToSteer/180*np.pi)
            # Make all delays positive
            if (np.sin(self._angleToSteer/180*np.pi) < 0):
                delay = delay[::-1] * -1
        else:
            delay = np.zeros(self.__row_count)
            
        if self._beamfocusing_enable:
            focus_delay = self.__distance**2/(2*self.__beamfocusing_radius*self.getSpeedOfSound()) * np.arange(self.__row_count) * (self.__row_count - np.arange(self.__row_count) - 1)
            tot_delay = delay + focus_delay
            tot_delay -= min(tot_delay)
            if not np.any(np.max(tot_delay) >= maxDelay):
                delay = tot_delay
            else:
                print(f"Beamfocusing was not applied")
        print(delay)
        if np.any(delay >= maxDelay):
            print(f"Wrong angle: {delay}")
        delay = np.clip(delay, 0, maxDelay)
        self._fpga_controller.setChannelDelay(delay)
        self._fpga_controller.update()
    
    def calculateGains(self):
        self._gains = np.array(self.__window_types[self._activeWindow])
        if not DEBUG:
            self._fpga_controller.setChannelGain(self._gains)
            self._fpga_controller.update()
        else:
            print(f"Gains: {np.array(self._gains)}")

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
        
        
if __name__ == '__main__':
    beamsteering = Beamsteering()
    