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

DEBUG = True
LINUX = (sys.platform == 'linux')

if LINUX:
    from smbus2 import SMBus, i2c_msg
    import RPi.GPIO as GPIO
    

class HMI():
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
    PCA9633_OUTDRV      = 0x04  # bit 2, output driver 0=opendrain, 1=push-ull
    PCA9633_OUTNE1      = 0x02  # bit 1, 2 bits see page 13, 16 pin device only
    PCA9633_OUTNE0      = 0x01  # bit 0, see above
    
    
    def __init__(self, deviceAddresse=0x62):      
        self._i2cBusID = 10     # Represents /dev/i2c-10
        
        self._pinLedR = 3
        self._pinLedG = 2
        self._pinLedB = 1
        self._pinFan = 0
        
        self._gpioButton = 3
        
        self._initialized = False
        self._GAMMA_CORRECT_FACTOR = 2.8
        self._deviceAddress = deviceAddresse
        self._outputState = 0x00
        self._buttonCallback = None
        if LINUX:
            self._i2c_msg = i2c_msg
        
    
    def __del__(self):
        self.end()
    
    
    def begin(self):
        if not self._initialized:
            self._initialized = True
            init = {HMI.PCA9633_LEDOUT: 0x00,   # All Outputs are off
                    HMI.PCA9633_MODE1: 0x00,    # set sleep = 0, turn on oscillator, disable allcall and subaddrs
                    HMI.PCA9633_MODE2: 0x14}    # Enable Push-Pull Outputs and invert PWM
            self._writeRegs(init) 
            self.setFanSpeed(0)
            self.setButtonColor(np.zeros((1, 3)))
            if LINUX:
                GPIO.setwarnings(False)         # Disable Pull-up Warning
                GPIO.setmode(GPIO.BCM)          # Use RaspberryPi GPIO Numbers
                GPIO.setup(self._gpioButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                try:
                    GPIO.add_event_detect(self._gpioButton, GPIO.FALLING, callback=self._buttonPress, bouncetime = 1000)  
                except RuntimeError:
                    GPIO.remove_event_detect(self._gpioButton)
                    GPIO.add_event_detect(self._gpioButton, GPIO.FALLING, callback=self._buttonPress, bouncetime = 1000)
                
    
    def end(self, turnOffLed=True):
        if(self._initialized):
            if turnOffLed:
                self.setButtonColor()
            self.setFanSpeed(0)
            self._initialized = False
            if LINUX:
                try:
                    GPIO.remove_event_detect(self._gpioButton)
                except RuntimeError:
                    pass
            
        
    def registerButtonCallback(self, callback):
        self._buttonCallback = callback
       
            
    def setButtonColor(self, color=np.zeros((1, 3))):
        if(np.shape(color) == (3,)):
            color = np.vstack(color).T    # Transpose Vector if neccessary
        if(np.shape(color) != (1, 3)):
            raise ValueError("Color data format incorrect: (1, 3)")
        data = {self._pinLedR: int(self._gamma(color.T[0]) * 255),
                self._pinLedG: int(self._gamma(color.T[1]) * 255),
                self._pinLedB: int(self._gamma(color.T[2]) * 255)}
        self._pwmWriteMultiple(data)
    
    
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
        self._writeRegs({HMI.PCA9633_LEDOUT: self._outputState})

    
    def _pwmWriteMultiple(self, data):
        regs = {}
        for pin in data:
            if not(0 <= pin <= 3):
                raise ValueError("Pin not available: 0 .. 3")
            if not(0 <= data[pin] <= 255):
                raise ValueError("PWM Value out of bound: 0 .. 255")
            self._outputState &= ~(0x03 << (pin * 2))   # Clear bits first
            self._outputState |= 0x02 << (pin * 2)      # Output in PWM mode
            regs[HMI.PCA9633_LEDOUT] = self._outputState
            regs[HMI.PCA9633_PWM0 + pin]= int(data[pin])
        self._writeRegs(regs)
        

    def _pwmWrite(self, pin, value):
        if not(0 <= pin <= 3):
            raise ValueError("Pin not available: 0 .. 3")
        if not(0 <= value <= 255):
            raise ValueError("PWM Value out of bound: 0 .. 255")
            
        self._outputState &= ~(0x03 << (pin * 2))   # Clear bits first
        self._outputState |= 0x02 << (pin * 2)      # Output in PWM mode
        regs = {HMI.PCA9633_LEDOUT: self._outputState,
                HMI.PCA9633_PWM0 + pin: int(value)}
        self._writeRegs(regs)
        
        
    def _writeRegs(self, regs):
        if LINUX and self._initialized:
            buf = []
            for reg in regs:
                buf.append(self._i2c_msg.write(self._deviceAddress, [reg, regs[reg]]))
            retryCount = 10
            while True:
                try:
                    with SMBus(self._i2cBusID) as bus:
                        bus.i2c_rdwr(*buf)
                    break
                except:
                    print("HMI: Error occured on I2C Bus -> Try again")
                    import time
                    time.sleep(0.5)
                    retryCount -= 1
                    if(retryCount == 0):
                        raise Exception("HMI I2C Bus Error")
   
    def _gamma(self, val):
        return np.clip(np.power(val, self._GAMMA_CORRECT_FACTOR), 0.0, 1.0)
    
    
    def _buttonPress(self, pin):
        if DEBUG:
            print("Button has been pressed")
        if self._buttonCallback:
            self._buttonCallback()


if __name__ == '__main__':
    import time
    
    hmi = HMI()
    hmi.begin()
    hmi.setButtonColor(np.array([1.0, 0.5, 0.0]))  # R, G, B
    hmi.setFanSpeed(1.0)
    time.sleep(1)
    hmi.setButtonColor(np.array([0.0, 1.0, 1.0]))  # R, G, B
    hmi.setFanSpeed(0.5)
    time.sleep(1)
    
    hmi.setButtonColor()                       # No argument means off
    hmi.end()
    