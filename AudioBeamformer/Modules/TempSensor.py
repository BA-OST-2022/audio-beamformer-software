###############################################################################
# file    TempSensor.py
###############################################################################
# brief   This module communicates with the Temperature Sensors (TMP112)
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

DEBUG = False
LINUX = (sys.platform == 'linux')

if LINUX:
    from adafruit_extended_bus import ExtendedI2C as I2C
    
    
# TMP112 Register Map
TMP112_REG_TEMP					= 0x00
TMP112_REG_CONFIG				= 0x01
TMP112_REG_THIGH				= 0x02
TMP112_REG_TLOW					= 0x03

# TMP112 Configuration Register
TMP112_REG_CONFIG_CONTINOUS		= 0x0000 # Continuous Conversion Mode
TMP112_REG_CONFIG_SHUTDOWN		= 0x0100 # Shutdown Mode enabled
TMP112_REG_CONFIG_INTERRUPT		= 0x0200 # Interrupt Mode enabled
TMP112_REG_CONFIG_POL_H			= 0x0400 # Polarity Active HIGH
TMP112_REG_CONFIG_FQ_1			= 0x0000 # Fault Queue = 1
TMP112_REG_CONFIG_FQ_2			= 0x0800 # Fault Queue = 2
TMP112_REG_CONFIG_FQ_4			= 0x1000 # Fault Queue = 4
TMP112_REG_CONFIG_FQ_6			= 0x1800 # Fault Queue = 6
TMP112_REG_CONFIG_RES			= 0x6000 # 12-bits Resolution
TMP112_REG_CONFIG_OS			= 0x8000 # One-shot enabled
TMP112_REG_CONFIG_CR_0_25		= 0x0000 # Conversion Rate = 0.25 Hz
TMP112_REG_CONFIG_CR_1			= 0x0040 # Conversion Rate = 1 Hz
TMP112_REG_CONFIG_CR_4			= 0x0080 # Conversion Rate = 4 Hz
TMP112_REG_CONFIG_CR_8			= 0x00C0 # Conversion Rate = 8 Hz
TMP112_REG_CONFIG_AL_H			= 0x0020 # When the POL bit = 0, AL is HIGH


class TempSensor():
    def __init__(self, deviceAdresse=0x48):      
        self._i2cBusID = 20                     # /dev/i2c-20
        self._i2cBusFrequency = 400000          # I2C Bus Speed
        
        self._initialized = False
        self._deviceAdress = deviceAdresse
        self._i2c = None
        
    
    def __del__(self):
        self.end()
    
    
    def begin(self):
        if not self._initialized:
            self._initialized = True
            if LINUX:
                TEMP_CONFIG = (TMP112_REG_CONFIG_CONTINOUS |
                               TMP112_REG_CONFIG_FQ_1 |
                               TMP112_REG_CONFIG_RES |
                               TMP112_REG_CONFIG_FQ_1 |
                               TMP112_REG_CONFIG_CR_4 |
                               TMP112_REG_CONFIG_AL_H)
                
                self._i2c = I2C(self._i2cBusID, self._i2cBusFrequency)
                self._i2c.write_byte_data(self._deviceAdress,
                                          TMP112_REG_CONFIG, TEMP_CONFIG)
                
                # https://github.com/mp-extras/vl53l5cx/blob/c7476877e96fabe81516176fbe8c575923d368b1/vl53l5cx/cp.py
                
    
    def end(self):
        if(self._initialized):
            self._initialized = False
            if LINUX:
                self._i2c.deinit()
                
    def getTemperature(self):
        
        if LINUX and self._initialized:
            data = self._i2c.read_i2c_block_data(self._deviceAdress,
                                                 TMP112_REG_TEMP, 2)
            temp =(data[0] * 256 + data[1]) / 16  # Convert the data to 12-bits
            if temp > 2047:
                temp -= 4096
                temp *= 0.0625
            return temp
        return float("nan")


if __name__ == '__main__':
    tempSensorAmbient = TempSensor(0x48)
    tempSensorSystem = TempSensor(0x49)
    tempSensorAmbient.begin()
    tempSensorSystem.begin()
    
    print(f"Ambient Temperature: {tempSensorAmbient.getTemperature():.1f} °C")
    print(f"System Temperature: {tempSensorSystem.getTemperature():.1f} °C")
    
    tempSensorAmbient.end()
    tempSensorSystem.end()
    