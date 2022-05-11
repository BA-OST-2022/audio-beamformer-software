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
import numpy as np

DEBUG = False
LINUX = (sys.platform == 'linux')

if LINUX:
    from smbus2 import SMBus


PCA9633_BASEADDR    = 0x60

PCA9633_MODE1       = 0x00  # mode register 1
PCA9633_MODE2       = 0x01  # mode register 2
PCA9633_PWM0        = 0x02  # PWM0 brightness control led0
PCA9633_PWM1        = 0x03  # PWM0 brightness control led0
PCA9633_PWM2        = 0x04  # PWM0 brightness control led0
PCA9633_PWM3        = 0x05  # PWM0 brightness control led0
PCA9633_GRPPWM      = 0x06  # group brightness (duty cycle)
PCA9633_GRPFREQ     = 0x07  # group frequency
PCA9633_LEDOUT      = 0x08  # LED output state
PCA9633_SUBADR1     = 0x09  # i2c bus sub address 1
PCA9633_SUBADR2     = 0x0A  # i2c bus sub address 1
PCA9633_SUBADR3     = 0x0B  # i2c bus sub address 1
PCA9633_ALLCALLADR  = 0x0C  # LED All Call i2c address

PCA9633_SLEEP       = 0x10  # bit 4, low power mode enable, RW
PCA9633_SUB1        = 0x08  # bit 3, PCA9633 responds to sub address 1
PCA9633_SUB2        = 0x04  # bit 2, PCA9633 responds to sub address 2
PCA9633_SUB3        = 0x02  # bit 1, PCA9633 responds to sub address 3
PCA9633_ALLCALL     = 0x01  # bit 0, PCA9633 responds to all call address

PCA9633_DMBLINK     = 0x20  # bit 5, group control dim or blink
PCA9633_INVRT       = 0x10  # bit 4, output logic invert (1=yes, 0=no)
PCA9633_OCH         = 0x08  # bit 3, 0=output change on stop, 1=on ACK
PCA9633_OUTDRV      = 0x04  # bit 2, output drivers 0=open drain, 1=push-pull
PCA9633_OUTNE1      = 0x02  # bit 1, 2 bits see page 13, 16 pin device only
PCA9633_OUTNE0      = 0x01  # bit 0, see above


class HMI():
    def __init__(self, deviceAddresse=0x62):      
        self._i2cBusID = 0                      # TODO: Change to /dev/i2c-20
        
        self._pinLedR = 3
        self._pinLedG = 2
        self._pinLedB = 1
        self._pinFan = 0
        
        self._initialized = False
        self._GAMMA_CORRECT_FACTOR = 2.8
        self._deviceAddress = deviceAddresse
        self._outputState = 0x00
        
    
    def __del__(self):
        self.end()
    
    
    def begin(self):
        if not self._initialized:
            self._initialized = True
            self._writeReg(PCA9633_LEDOUT, 0x00)  # All Outputs are off
            self._writeReg(PCA9633_MODE1, 0x00)   # set sleep = 0, turn on oscillator, disable allcall and subaddrs
            self._writeReg(PCA9633_MODE2, 0x14)   # Enable Push-Pull Outputs and invert PWM
            self.setFanSpeed(0)
            self.setButtonColor(np.zeros((1, 3)))
                
    
    def end(self):
        if(self._initialized):
            self._initialized = False
            self.setFanSpeed(0)
            # Do not turn off LED, since it can be used as stanby indicator
       
            
    def setButtonColor(self, color=np.zeros((1, 3))):
        if(np.shape(color) == (3,)):
            color = np.vstack(color).T    # Transpose Vector if neccessary
        if(np.shape(color) != (1, 3)):
            raise ValueError("Color data format incorrect: (1, 3)")
        self._pwmWrite(self._pinLedR, int(self._gamma(color.T[0]) * 255))
        self._pwmWrite(self._pinLedG, int(self._gamma(color.T[1]) * 255))
        self._pwmWrite(self._pinLedB, int(self._gamma(color.T[2]) * 255))
    
    
    def setFanSpeed(self, speed):
        if not(0.0 <= speed <= 1.0):
            raise ValueError("Value out of bound: 0.0 .. 1.0")
        self._pwmWrite(self._pinFan, int(speed * 255))
        
    
    def _digitalWrite(self, pin, state):
        if not(0 <= pin <= 3):
            raise ValueError("Pin not available: 0 .. 3")
            
        self._outputState &= ~(0x03 << (pin * 2))   # Output fully off
        if(state):
            self._outputState |= 0x01 << (pin * 2)  # Output fully on
        self._writeReg(PCA9633_LEDOUT, self._outputState)

    
    def _pwmWrite(self, pin, value):
        if not(0 <= pin <= 3):
            raise ValueError("Pin not available: 0 .. 3")
        if not(0 <= value <= 255):
            raise ValueError("PWM Value out of bound: 0 .. 255")
            
        self._outputState &= ~(0x03 << (pin * 2))   # Clear bits first
        self._outputState |= 0x02 << (pin * 2)      # Output in PWM mode
        self._writeReg(PCA9633_LEDOUT, self._outputState);
        self._writeReg(PCA9633_PWM0 + pin, int(value));


    def _writeReg(self, reg, data):
        if LINUX and self._initialized:
            with SMBus(self._i2cBusID) as bus:
                bus.write_byte_data(self._deviceAddress, reg, data)
                
    def _gamma(self, val):
        return np.clip(np.power(val, self._GAMMA_CORRECT_FACTOR), 0.0, 1.0)


if __name__ == '__main__':
    import time
    
    hmi = HMI()
    hmi.begin()
    hmi.setButtonColor(np.array([0.5, 0, 1]))  # R, G, B
    hmi.setFanSpeed(0.5)
    time.sleep(3)
    
    hmi.setButtonColor()                       # No argument means off
    hmi.end()
    