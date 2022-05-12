###############################################################################
# file    RotaryEncoder.py
###############################################################################
# brief   This module controls the rotary encoder
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
    import RPi.GPIO as GPIO

    class Encoder:
        def __init__(self, leftPin, rightPin, callback=None):
            self.leftPin = leftPin
            self.rightPin = rightPin
            self.value = 0
            self.state = '00'
            self.direction = None
            self.callback = callback
            GPIO.setmode(GPIO.BCM)        # Use RaspberryPi GPIO Numbers
            GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            try:
                GPIO.add_event_detect(self.leftPin, GPIO.BOTH, callback=self.transitionOccurred)  
            except RuntimeError:
                GPIO.remove_event_detect(self.leftPin)
                GPIO.add_event_detect(self.leftPin, GPIO.BOTH, callback=self.transitionOccurred)  
            try:
                GPIO.add_event_detect(self.rightPin, GPIO.BOTH, callback=self.transitionOccurred)
            except RuntimeError:
                GPIO.remove_event_detect(self.rightPin)
                GPIO.add_event_detect(self.rightPin, GPIO.BOTH, callback=self.transitionOccurred)
                
        
        def __del__(self):
            try:
                GPIO.remove_event_detect(self.leftPin)  
            except RuntimeError:
                pass
            try:
                GPIO.remove_event_detect(self.rightPin)  
            except RuntimeError:
                pass
            
    
        def transitionOccurred(self, channel):
            p1 = GPIO.input(self.leftPin)
            p2 = GPIO.input(self.rightPin)
            newState = "{}{}".format(p1, p2)
    
            if self.state == "00": # Resting position
                if newState == "01": # Turned right 1
                    self.direction = "R"
                elif newState == "10": # Turned left 1
                    self.direction = "L"
    
            elif self.state == "01": # R1 or L3 position
                if newState == "11": # Turned right 1
                    self.direction = "R"
                elif newState == "00": # Turned left 1
                    if self.direction == "L":
                        self.value = self.value - 1
                        if self.callback is not None:
                            self.callback(self.value, self.direction)
    
            elif self.state == "10": # R3 or L1
                if newState == "11": # Turned left 1
                    self.direction = "L"
                elif newState == "00": # Turned right 1
                    if self.direction == "R":
                        self.value = self.value + 1
                        if self.callback is not None:
                            self.callback(self.value, self.direction)
    
            else: # self.state == "11"
                if newState == "01": # Turned left 1
                    self.direction = "L"
                elif newState == "10": # Turned right 1
                    self.direction = "R"
                elif newState == "00": # Skipped an intermediate 01 or 10 state
                    if self.direction == "L":
                        self.value = self.value - 1
                        if self.callback is not None:
                            self.callback(self.value, self.direction)
                    elif self.direction == "R":
                        self.value = self.value + 1
                        if self.callback is not None:
                            self.callback(self.value, self.direction)
                    
            self.state = newState
    
        def getValue(self):
            return self.value
        
        def setValue(self, value):
            self.value = value
    


class RotaryEncoder():
    def __init__(self, pinA, pinB, pinS):      
        self._pinA = pinA
        self._pinB = pinB
        self._pinS = pinS
        
        self._encoder = None
        self._encoderValue = 0.0
        self._buttonState = False
        
    
    def __del__(self):
        self.end()


    def begin(self):
        if LINUX:
            self._encoder = Encoder(self._pinA, self._pinB, self._valueChanged)
            GPIO.setmode(GPIO.BCM)        # Use RaspberryPi GPIO Numbers
            GPIO.setup(self._pinS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            try:
                GPIO.add_event_detect(self._pinS, GPIO.FALLING, callback=self._buttonChanged)  
            except RuntimeError:
                GPIO.remove_event_detect(self._pinS)
                GPIO.add_event_detect(self._pinS, GPIO.FALLING, callback=self._buttonChanged)
                
                
    def end(self):
        if self._encoder:
            self._encoder.__del__()
        if LINUX:
            try:
                GPIO.remove_event_detect(self._pinS)
            except RuntimeError:
                pass


    def getEncoderValue(self):
        return self._encoderValue
    
    def setEncoderValue(self, value):
        if not(0.0 <= value <= 1.0):
            raise ValueError("Value must be between 0.0 .. 1.0")
        self._encoderValue = value
            
    def getButtonState(self):
        return self._buttonState
    
    def setButtonState(self, state):
        self._buttonState = state


    def _valueChanged(self, value, direction):
        if(value < 0):
            value = 0
        if(value > 100):
            value = 100
        self._encoder.setValue(value)
        self._encoderValue = value / 100.0


    def _buttonChanged(self, channel):
        self._buttonState = not self._buttonState
        
            

if __name__ == '__main__':
    import time
    rotaryEncoder = RotaryEncoder(pinA=16, pinB=12, pinS=20)
    rotaryEncoder.begin()

    for i in range(25):
        print(f"Enocder: {rotaryEncoder.getEncoderValue()}, Button: {rotaryEncoder.getButtonState()}")
        time.sleep(0.5)
        