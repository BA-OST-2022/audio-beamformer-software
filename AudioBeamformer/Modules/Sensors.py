###############################################################################
# file    Sensors.py
###############################################################################
# brief   This module handles all low-level components and sensors
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-05-11
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
import sys
import time
import threading
import re, subprocess
import numpy as np
import psutil

DEBUG = False
LINUX = (sys.platform == 'linux')
sys.path.insert(0, os.path.dirname(__file__)) 
sys.path.insert(0, os.path.dirname(__file__) + "/Modules")

from TempSensor import TempSensor
from ToFSensor import ToFSensor
from HMI import HMI
from RotaryEncoder import RotaryEncoder
from scipy.signal import convolve2d
from colorsys import hsv_to_rgb


class Sensors():
    def __init__(self, powerSupply=None, audioProcessing=None, leds=None):  
        self.SRC_AMBIENT = 0
        self.SRC_SYSTEM = 1
        self.SRC_CPU = 2
        self.EVENT_ALERT = 0
        self.EVENT_FREE = 1
        
        self.COLOR_BOOT = np.array([1.0, 1.0, 0.0])        # White
        self.COLOR_RUN = np.array([0.0, 1.0, 1.0])         # Cyan
        self.COLOR_MUTE = np.array([1.0, 0.0, 0.0])        # Red
        self.COLOR_STANDBY = np.array([0.62, 0.62, 0.0])   # Yellow (dark)
        
        self._updateRateTemp = 2                           # Update rate in Hz
        self._updateRateLed = 10                           # Update rate in Hz
        self._updateRateToF = 3                            # Update rate in Hz                
        
        self._tempSensorAmbient = TempSensor(0x48)
        self._tempSensorSystem = TempSensor(0x49)
        self._hmi = HMI(0x62)
        self._tofSensor = ToFSensor(self._updateRateToF)
        self._rotaryEncoder = RotaryEncoder(pinA=16, pinB=12, pinS=20)
        self._powerSupply = powerSupply
        self._audioProcessing = audioProcessing
        self._leds = leds
        
        self._initialized = False
        self._runInitialization = False
        self._readyState = False
        self._runThread = False
        self._updateRate = None
        self._alertEnable = True
        self._alertState = False
        self._alertSensitivity = 0.5
        self._distanceLevel = 0.0
        self._enableMagic = False
        self._ledColor = np.zeros((1, 3))
        self._shutdownCallback  = None
        
        self._ambientTemp = float("NAN")
        self._systemTemp = float("NAN")
        self._cpuTemp = float("NAN")
        self._distanceMap = self._tofSensor.getDistance()
        
        self._timeTemp = 0
        self._timeLed = 0
        self._timeToF = 0
        
    
    def __del__(self):
        self.end()
    
    
    def begin(self, updateRate=30):
        if not self._initialized:
            self._initialized = True
            self._runInitialization = True
            self._updateRate = updateRate
            self._runThread = True
            threading.Timer(0, self.update).start()  
    
    
    def end(self, shutdown=False):
        self._readyState = False
        self._runThread = False
        if(self._initialized):
            if shutdown:
                self._hmi.setButtonColor(self.COLOR_BOOT)
            else:
                self._hmi.setButtonColor()
            self._tempSensorAmbient.end()
            self._tempSensorSystem.end()
            self._tofSensor.end()
            if shutdown:
                self._hmi.setButtonColor(self.COLOR_BOOT)
            self._hmi.end(not shutdown)  # Turn off LED if not shutdown
            self._initialized = False
        
    
    def update(self):
        if(self._runInitialization):
            self._runInitialization = False
            if DEBUG:
                print("Asynchronous Sensors Initialization started...")
            self._hmi.registerButtonCallback(self._shutdownEvent)
            self._hmi.begin()
            self._hmi.setButtonColor(self.COLOR_BOOT)
            self._hmi.setFanSpeed(1.0)    # Do a fan test at startup
            self._rotaryEncoder.begin()
            self._tempSensorAmbient.begin()
            self._tempSensorSystem.begin()
            self._tofSensor.begin()       # This takes up to 10s
            self._hmi.setButtonColor(self.COLOR_RUN)
            self._readyState = True
            if DEBUG:
                print("Asynchronous Sensors Initialization done")
        
        if(self._initialized):
            if(self._runThread):
                threading.Timer(1.0 / self._updateRate, self.update).start()            
            else:
                return
            
            if(time.time() - self._timeToF > 1 / self._updateRateToF):            
                if(self._tofSensor.update()):
                    self._timeToF = time.time()
                    self._distanceMap = self._tofSensor.getDistance()
                    event = self._checkDistanceMap(self._distanceMap)
                    if(event == self.EVENT_ALERT):
                        self._alertState = True
                    if(event == self.EVENT_FREE):
                        self._alertState = False
                    if DEBUG:
                        print("Updated ToF Sensor Data")
                    
            
            mute = self.getMute() or self.getAlertState()
            if self._powerSupply:
                self._powerSupply.enableOutput(not mute)
            if self._audioProcessing:
                self._audioProcessing.enableMute(mute)
                
            if self._leds:
                self._leds.enableAlert(self.getAlertState())
                
            if(mute):
                self._ledColor = self.COLOR_MUTE
            else:
                self._ledColor = self.COLOR_RUN
            
            
            if(time.time() - self._timeLed > 1 / self._updateRateLed):
                self._timeLed = time.time()
                if(self._enableMagic):
                    r, g, b = hsv_to_rgb(time.time() / 3, 1, 1)
                    self._ledColor = np.array([r, g, b])
                self._hmi.setButtonColor(self._ledColor)
                
            if(time.time() - self._timeTemp > 1 / self._updateRateTemp):
                self._timeTemp = time.time()
                self._ambientTemp = self._tempSensorAmbient.getTemperature()
                self._systemTemp = self._tempSensorSystem.getTemperature()
                self._cpuTemp = self._getCpuTemperature()
                if not np.isnan(self._systemTemp):
                    fanSpeed = np.clip((self._systemTemp - 40) / 20, 0, 1)
                    self._hmi.setFanSpeed(fanSpeed) # 40°C = 0% .. 60°C = 100%
                
            
    
    def getReadyState(self):
        return self._readyState
    
    
    def registerShutdownCallback(self, callback):
        self._shutdownCallback = callback


    def getTemperature(self, source):
        if(source == self.SRC_AMBIENT):
            return self._ambientTemp
        elif(source == self.SRC_SYSTEM):
            return self._systemTemp
        elif(source == self.SRC_CPU):
            return self._cpuTemp
        return float("NAN")
    
    
    def getCpuLoad(self):
        return psutil.cpu_percent()
    
    
    def getDistanceLevel(self):
        return self._distanceLevel


    def enableAlert(self, state):
        self._alertEnable = state
    
    
    def setAlertSensitivity(self, sensitivity):
        if not(0.0 <= sensitivity <= 1.0):
            raise ValueError("Sensitivity out of bound: 0.0 .. 1.0")
        self._alertSensitivity = sensitivity
        
    def getAlertState(self):
        return self._alertState and self._alertEnable
    
    def setVolume(self, volume):
        if self._rotaryEncoder:
            self._rotaryEncoder.setEncoderValue(volume)
        if self._powerSupply:
            self._powerSupply.setVolume(volume)
        if self._audioProcessing:
            gain = np.clip(volume * 10, 0.0, 1.0)
            self._audioProcessing.setOutputGain(gain)
   
    
    def getVolume(self):
        return self._rotaryEncoder.getEncoderValue()
    
    
    def setMaxVolume(self, maxVolume):
        if self._powerSupply:
            self._powerSupply.setMaxVolume(maxVolume)
    
    
    def setMute(self, state):
        self._rotaryEncoder.setButtonState(state)

    
    def getMute(self):
        return self._rotaryEncoder.getButtonState()   
    
    
    def enableMagic(self, state):
        self._enableMagic = state
        
        
    def _shutdownEvent(self):
        if DEBUG:
            print("Shutdown Event occurred")
        if self._shutdownCallback:
            self._shutdownCallback(True)
    
    
    def _getCpuTemperature(self):
        if LINUX:
            err, msg = subprocess.getstatusoutput('vcgencmd measure_temp')
            if not err:
                m = re.search(r'-?\d\.?\d*', msg)
                try:
                    return float(m.group())
                except ValueError:
                    pass
        return float("NAN")
    
    
    def _checkDistanceMap(self, distanceMap):
        row_size = 3
        column_size = 2
        distance_foreground_on = 2000
        distance_foreground_off = 2500

        sens = max(1,(1 - self._alertSensitivity) * row_size * column_size)
        mask = np.ones((row_size,column_size))
        foreground_map_on = distanceMap <= distance_foreground_on
        foreground_map_off = distanceMap <= distance_foreground_off
        element_foreground_on = convolve2d(mask,foreground_map_on,"same") >= sens 
        element_foreground_off = convolve2d(mask,foreground_map_off,"same") >= sens 

        self._distanceLevel = np.mean(element_foreground_on)
        mute_channel = np.any(element_foreground_on)

        if not mute_channel and not np.any(element_foreground_off):
            mute_channel = False
            return self.EVENT_FREE
        if mute_channel:
            return self.EVENT_ALERT
        return None
    


if __name__ == '__main__':
    sensors = Sensors()
    sensors.begin()

    time.sleep(10)
    sensors.end()
