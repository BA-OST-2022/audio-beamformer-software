###############################################################################
# file    AudioBeamformer.py
###############################################################################
# brief   Main Application
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

from Modules.PowerSupply import powerSupply
from Modules.LEDs import leds
from GUI.GUI import GUI
from Modules.AudioProcessing import AudioProcessing

class AudioBeamformer():
    def __init__(self):
        self.audio_processing = AudioProcessing()
        
        self.gui = GUI(self.audio_processing)  # GUI get all object references
    
    def begin(self):
        powerSupply.begin()
        leds.begin()
        
        self.gui.registerTerminateCallback(self.end)
        self.gui.run()  # This functioncall is blocking and must be at the end
        
    def end(self):
        leds.end()
        powerSupply.end()
        print("Main Application terminated...")


if __name__ == '__main__':
    audioBeamformer = AudioBeamformer()
    audioBeamformer.begin()