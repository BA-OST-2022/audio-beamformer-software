###############################################################################
# file    LEDs.py
###############################################################################
# brief   This module handles the communication with the RGB-LEDs
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
import threading
import numpy as np
import time
from colorsys import hsv_to_rgb

DEBUG = False
LINUX = (sys.platform == 'linux')

if(LINUX or DEBUG):
    from apa102_pi.driver import apa102


class LEDs():    
    def __init__(self, updateRate = 30, channelCount = 5, ringCount = 20):
        self.OFF = 0
        self.SEARCHING = 1
        self.TRACKING = 2
        
        self._initialized = False
        self._runThread = False
        self._updateRate = updateRate
        self._channelCount = channelCount   # 19
        self._ringCount = ringCount
        self._brightness = 31
        self._enableChannels = True
        self._enableCamera = True
        self._enableMagic = False
        self._ringColors = np.zeros((self._ringCount, 3))
        self._channelColors = np.zeros((self._channelCount, 3))
        self._cameraAnimation = self.OFF
    
    def __del__(self):
        self.end()
    
    def begin(self, framerate = 30):
        if not self._initialized:
            self._initialized = True
            self._updateRate = framerate
            
            if(LINUX or DEBUG):
                ledCount = self._channelCount * 2 + self._ringCount
                self.strip = apa102.APA102(num_led=ledCount, spi_bus=5,
                                           bus_speed_hz=8000000,
                                           global_brightness=self._brightness)
                self.strip.clear_strip()

            self._runThread = True
            self.update()

    
    def end(self):
        if(self._initialized):
            if(LINUX or DEBUG):
                self.strip.clear_strip()
                self.strip.cleanup()

        self._runThread = False
        self._initialized = False
    
    def enableCamera(self, state):
        self._enableCamera = state
    
    def enableChannels(self, state):
        self._enableChannels = state
    
    def enableMagic(self, state):
        self._enableMagic = state
      
    def setBrightness(self, brightness):
        self._brightness = np.clip(brightness * 31, 0, 31)
        if(LINUX or DEBUG):
            self.strip.set_global_brightness(self._brightness)
    
    def setChannelColors(self, colors):
        if(np.shape(colors) != (self._channelCount, 3)):
            raise ValueError("Channel color data format incorrect")
        self._channelColors = colors
    
    def setCameraAnimation(self, animation):
        self._cameraAnimation = animation
    
    
    def update(self):
        if(self._initialized):
            if(self._runThread):
                threading.Timer(1.0 / self._updateRate, self.update).start()            
            else:
                return
            
            if(self._cameraAnimation == self.OFF):
                self._ringColors = np.zeros((self._ringCount, 3))
            elif(self._cameraAnimation == self.SEARCHING):
                speed = 10
                grad = np.linspace(0, 1, self._ringCount)
                grad = np.roll(grad, int(time.time() * speed))
                self._ringColors[:,0] = grad * 0.0  # Red
                self._ringColors[:,1] = grad * 1.0  # Green
                self._ringColors[:,2] = grad * 1.0  # Blue
            elif(self._cameraAnimation == self.TRACKING):
                speed = 5
                val = np.abs((time.time() * 0.1 * speed) % 2 - 1) # Triangle
                val = np.ones(self._ringCount) * val
                self._ringColors[:,0] = val * 1.0   # Red
                self._ringColors[:,1] = val * 1.0   # Green
                self._ringColors[:,2] = val * 1.0   # Blue
                
            
            # TODO: Check if LUT for gamma correction is necessary
            if(LINUX or DEBUG):
                for i in range(self._channelCount):
                    r = g = b = 0
                    if self._enableChannels:
                        r = int(self._channelColors[i][0] * 255)
                        g = int(self._channelColors[i][1] * 255)
                        b = int(self._channelColors[i][2] * 255)
                    if self._enableMagic:
                        val = (time.time() / 2 + i // 4)
                        val /= i // self._channelCount
                        r, g, b = [int(c * 255) for c in hsv_to_rgb(val, 1, 1)]
                    self.strip.set_pixel(i, r, g, b)
                    self.strip.set_pixel(i + self._channelCount, r, g, b)
                
                for i in range(self._ringCount):
                    r = g = b = 0
                    if self._enableCamera:
                        r = int(self._ringColors[i][0] * 255)
                        g = int(self._ringColors[i][1] * 255)
                        b = int(self._ringColors[i][2] * 255)
                    if self._enableMagic:
                        val = (time.time() / 2 + i // 4)
                        val /= i // self._ringCount
                        r, g, b = [int(c * 255) for c in hsv_to_rgb(val, 1, 1)]
                    self.strip.set_pixel(i + self._channelCount * 2, r, g, b)
                
                self.strip.show()


leds = LEDs()

if __name__ == '__main__':
    leds.begin()
    leds.setBrightness(0.1)
    leds.setCameraAnimation(leds.SEARCHING)
    leds.enableMagic(True)
    
    time.sleep(3)
    leds.end()
    