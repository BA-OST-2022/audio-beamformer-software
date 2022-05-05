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

DEBUG = False
LINUX = (sys.platform == 'linux')

if(LINUX or DEBUG):
    from apa102_pi.driver import apa102


class LEDs():
    def __init__(self):
        self._initialized = False
        self._runThread = False
        self._updateRate = 30
        self._channelCount = 5   # 19
        self._ringCount = 20
        self._brightness = 1
        self._enableChannels = True
        self._enableCamera = True
    
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
        pass
    
    def enableChannels(self, state):
        pass
    
    def setBrightness(self, brightness):
        self._brightness = np.clip(brightness * 31, 0, 31)
        self.strip.set_global_brightness(self._brightness)
        self.strip.show()
    
    def setChannelColors(self, colors):
        pass
    
    def setCameraAnimation(self, animation):
        pass
    
    
    def update(self):
        if(self._initialized):
            if(self._runThread):
                threading.Timer(1.0 / self._updateRate, self.update).start()            
            
            # Prepare a few individual pixels
            self.strip.set_pixel_rgb(0, 0xFF0000)  # Red
            self.strip.set_pixel_rgb(1, 0xFFFFFF)  # White
            self.strip.set_pixel_rgb(2, 0x00FF00)  # Green
            
            self.strip.set_pixel_rgb(11, 0x00FF00)  # Green
            
            self.strip.show()
            # print("Update")



leds = LEDs()

if __name__ == '__main__':
    import time
    leds.begin()
    leds.setBrightness(0.1)
    
    time.sleep(3)
    leds.end()