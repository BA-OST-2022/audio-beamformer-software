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

import os
import sys
from Modules.PowerSupply import powerSupply
from Modules.LEDs import leds
from Modules.AudioProcessing import AudioProcessing
from Modules.Beamsteering import Beamsteering
from Modules.Sensors import Sensors
from Modules.FPGAControl import fpgaControl
from GUI.GUI import GUI
from FaceTracking.FaceTracking import faceTracking

LINUX = (sys.platform == 'linux')

class AudioBeamformer():
    def __init__(self):
        self.audio_processing = AudioProcessing()
        self.sensors = Sensors(powerSupply)
        self.beamsteering = Beamsteering(self.sensors, faceTracking,
                                         fpgaControl)
        self.gui = GUI(self.audio_processing, self.beamsteering, faceTracking,
                       self.sensors, leds)
    
    def begin(self):
        powerSupply.begin()
        fpgaControl.begin()
        leds.begin()
        self.sensors.begin()
        self.sensors.registerShutdownCallback(self.end)
        self.beamsteering.begin()
        self.audio_processing.begin()
        self.gui.registerTerminateCallback(self.end)
        self.gui.run()  # This functioncall is blocking and must be at the end
        
    def end(self, shutdown=False):
        leds.end()
        powerSupply.end()
        fpgaControl.end()
        self.beamsteering.end()
        self.sensors.end()
        self.audio_processing.end()
        print("Main Application terminated...")
        if shutdown:
            print("Shut down system...")
            if LINUX:
                os.system("sudo shutdown -h now")  



audioBeamformer = AudioBeamformer()
audioBeamformer.begin()
