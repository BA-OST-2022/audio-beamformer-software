###############################################################################
# file    ToFSensor.py
###############################################################################
# brief   This module controls the communication with the ToF-Sensor (VL53L5CX)
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
import numpy as np
import time

DEBUG = False
LINUX = (sys.platform == 'linux')

if LINUX:
    from vl53l5cx.vl53l5cx import VL53L5CX
    from vl53l5cx.api import *
    

class ToFSensor():
    def __init__(self, updateRate=15):      
        self._i2cBusID = 10                     # Represents /dev/i2c-10
        self._maxRetry = 5                      # Max number of init retrying
        
        self._initialized = False
        self._driver = None
        self._updateRate = updateRate           # Update-Rate in Hz
        self._resolution = 8                    # 4x4 or 8x8 zones
        self._distanceData = np.ones((self._resolution, self._resolution))*4E3
        self._errorCount = 0
        
    
    def __del__(self):
        self.end()
    
    
    def begin(self):
        retryCount = 0
        if LINUX:
            while not self._initialized:
                try:
                    self._driver = VL53L5CX(bus_id=self._i2cBusID)
                    if not self._driver.is_alive():
                        raise IOError("VL53L5CX Device is not alive")
                    self._driver.init()             # This takes up to 10s
                    self._driver.set_ranging_mode(VL53L5CX_RANGING_MODE_CONTINUOUS)
                    self._driver.set_sharpener_percent(0)
                    self._driver.set_target_order(VL53L5CX_TARGET_ORDER_STRONGEST)
                    self._driver.set_resolution(self._resolution**2)
                    self._driver.set_ranging_frequency_hz(self._updateRate)
                    self._driver.start_ranging()
                    self._errorCount = 0
                    break   # Successful
                except Exception as e:
                    retryCount += 1
                    print("Failed to init ToF-Sensor, try again...")
                    print(e)
                    time.sleep(1)  # Wait and try again some time later
                    if retryCount >= self._maxRetry:
                        raise Exception("Could not initialize ToF-Sensor")
            self._initialized = True
                
    
    def end(self):
        if(self._initialized):
            self._initialized = False
            if LINUX:
                self._driver.stop_ranging()
                
    
    def update(self):
        if LINUX:
            try:
                if self._driver.check_data_ready():
                    ranging_data = self._driver.get_ranging_data()
                    for i in range(self._resolution**2):
                        val = 4000
                        if(ranging_data.target_status[i] != 255):
                            val = ranging_data.distance_mm[i]
                        if(val == 0):
                            val = 4000  
                        self._distanceData[i // self._resolution,
                                            i % self._resolution] = val
                    self._errorCount = 0
                    return True
            except:
                self._errorCount += 1
                if self._errorCount > 10:
                    print("Failed to read data from ToF-Sensor, reinitialize...")
                    self._initialized = False
                    self.begin()
        return False
    
    
    def getDistance(self):
        return self._distanceData
    
    
    def getResolution(self):
        return self._resolution
    
    
    
if __name__ == '__main__':
    import cv2
    
    SCALEUP = 50
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SIZE = 0.4
    FONT_COLOR = (0,0,0)
    FONT_THICKNESS = 1
    
    tofSensor = ToFSensor()
    print("Start Initializing...")
    tofSensor.begin()               # This takes up to 10s
    print("Initialization Done!")
    
    while True:
        time.sleep(0.01)
        if(tofSensor.update()):
            image = (tofSensor.getDistance() * 0.06375).astype('uint8')
            w = np.shape(image)[0]
            h = np.shape(image)[1]
            resized = cv2.resize(image, (w * SCALEUP, h * SCALEUP),
                                 interpolation= cv2.INTER_NEAREST)
            for y in range(h):
                for x in range(w):
                    cv2.putText(resized,
                                '%d' % tofSensor.getDistance()[x,y],
                                (y*SCALEUP+SCALEUP//4,x*SCALEUP+SCALEUP//2),
                                FONT, FONT_SIZE, FONT_COLOR, FONT_THICKNESS,
                                cv2.LINE_AA)
            
            cv2.imshow('VL53L5 [ESC to quit]', resized)
            if cv2.waitKey(1) == 27:
                break

    tofSensor.end()
    cv2.destroyAllWindows()