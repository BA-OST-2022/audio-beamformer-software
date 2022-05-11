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

import sys
import threading
import re, subprocess
import numpy as np
from TempSensor import TempSensor
from ToFSensor import ToFSensor
from HMI import HMI
from RotaryEncoder import RotaryEncoder

DEBUG = False
LINUX = (sys.platform == 'linux')



class Sensors():
    def __init__(self, powerSupply=None):  
        self.SRC_AMBIENT = 0
        self.SRC_SYSTEM = 1
        self.SRC_CPU = 2
        
        self._tempSensorAmbient = TempSensor(0x48)
        self._tempSensorSystem = TempSensor(0x49)
        self._hmi = HMI(0x62)
        self._tofSensor = ToFSensor()
        self._rotaryEncoder = RotaryEncoder(pinA=12, pinB=16, pinS=20)
        
        self._initialized = False
        self._runThread = False
        self._updateRate = None
        
        self._ambientTemperature = float("NAN")
        self._systemTemperature = float("NAN")
        self._cpuTemperature = float("NAN")
        self._distanceMap = self._tofSensor.getDistance()
        
    
    def __del__(self):
        self.end()
    
    
    def begin(self, updateRate=30):
        if not self._initialized:
            self._initialized = True
            self._updateRate = updateRate
            
            self._hmi.begin()
            self._hmi.setButtonColor(np.array([0.0, 1.0, 1.0]))
            self._hmi.setFanSpeed(1.0)    # Do a fan test at startup
            self._rotaryEncoder.begin()
            self._tempSensorAmbient.begin()
            self._tempSensorSystem.begin()
            self._tofSensor.begin()       # This takes up to 10s
            self._hmi.setButtonColor(np.array([1.0, 1.0, 1.0]))
            
            self._runThread = True
            self.update()
            
    
    
    def end(self):
        self._runThread = False
        if(self._initialized):
            self._initialized = False
            self._hmi.end()
            self._tempSensorAmbient.end()
            self._tempSensorSystem.end()
            self._tofSensor.end()
        
    
    def update(self):
        if(self._initialized):
            if(self._runThread):
                threading.Timer(1.0 / self._updateRate, self.update).start()            
            else:
                return
            
    

    def getTemperature(self, source):
        if(source == self.SRC_AMBIENT):
            return self._ambientTemperature
        elif(source == self.SRC_SYSTEM):
            return self._systemTemperature
        elif(source == self.SRC_CPU):
            return self._cpuTemperature
        return float("NAN")
    
    
    def getDistance(self):
        # TODO: Implement fancy algorythm out of self._distanceMap
        pass
    
    
    def enableAlert(self, state):
        pass
    
    
    def setAlertCallback(self, callback):
        pass
    
    
    def setFreeCallback(self, callback):
        pass
    
    
    def setAlertSensitivity(self, sensitivity):
        pass
    
    
    def setButtonColor(self, color):
        pass
    
    
    def setVolume(self, volume):
        pass
    
    
    def getVolume(self):
        pass
    
    
    def setMute(self, state):
        pass
    
    
    def getMute(self):
        pass
    
    
    def enableMagic(self, state):
        pass
    
    
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
    


if __name__ == '__main__':
    import time
    
    sensors = Sensors()
    sensors.begin()

    # time.sleep(10)
    sensors.end()
