###############################################################################
# file    HMI.py
###############################################################################
# brief   This module controls the RGB-Button and the fans (PCA9633)
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-05-10
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

DEBUG = False
LINUX = (sys.platform == 'linux')

if LINUX:
    from smbus2 import SMBus


REG_MODE1 =       0x00  # Mode register 1
REG_MODE2 =       0x01  # Mode register 2
REG_PWM0 =        0x02  # Brightness control LED0
REG_PWM1 =        0x03  # Brightness control LED1
REG_PWM2 =        0x04  # Brightness control LED2
REG_PWM3 =        0x05  # Brightness control LED3
REG_GRPPWM =      0x06  # Group duty cycle control
REG_GRPFREQ =     0x07  # Group frequency
REG_LEDOUT =      0x08  # LED output state
REG_SUBADR1 =     0x09  # I2C-bus subaddress 1
REG_SUBADR2 =     0x0A  # I2C-bus subaddress 2
REG_SUBADR3 =     0x0B  # I2C-bus subaddress 3
REG_ALLCALLADR =  0x0C  # LED All Call I2C-bus address

# Frequency of 24 Hz is used
BLINKING_PERIOD_125_MS  =  3     # ((1 / 24 Hz) * 3 cycles)
BLINKING_PERIOD_250_MS  =  6     # ((1 / 24 Hz) * 6 cycles)
BLINKING_PERIOD_500_MS  =  12    # ((1 / 24 Hz) * 12 cycles)
BLINKING_PERIOD_1_S     =  24    # ((1 / 24 Hz) * 24 cycles)
BLINKING_PERIOD_MAX     =  255   # 10.73 s
BLINKING_RATIO_BALANCED =  0.5




class HMI():
    def __init__(self, deviceAddresse=0x62):      
        self._i2cBusID = 0                      # TODO: Change to /dev/i2c-20
        
        self._initialized = False
        self._deviceAddress = deviceAddresse
        
    
    def __del__(self):
        self.end()
    
    
    def begin(self):
        if not self._initialized:
            self._initialized = True
            if LINUX:
                pass
                
    
    def end(self):
        if(self._initialized):
            self._initialized = False
       
            
    def setButtonColor(self, color):
        pass
    
    
    def setFanSpeed(self, speed):
        pass


if __name__ == '__main__':
    hmi = HMI()
    hmi.begin()

    hmi.end()

    