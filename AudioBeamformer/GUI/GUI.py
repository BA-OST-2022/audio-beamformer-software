###############################################################################
# file    GUi.py
###############################################################################
# brief   Main GUI Handler
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-05-05
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
import datetime
import numpy as np
from PyQt5 import QtGui, QtCore, QtQuick, QtQml
from PyQt5.QtGui  import QGuiApplication
from PyQt5.QtQml  import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl, pyqtProperty

DEBUG = True
LINUX = (sys.platform == 'linux')
sys.path.insert(0, os.getcwd() + "/GUI")   # Add this subdirectory to python path

sys_argv = sys.argv
sys_argv += ['--style', 'Material']
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QGuiApplication.instance()
if app == None:
    app = QGuiApplication(sys.argv)
if not QGuiApplication.instance():
    app = QGuiApplication(sys.argv)
else:
    app = QGuiApplication.instance()
engine = QQmlApplicationEngine()

# Important: Must be imported after creating Qt instance, this is a known bug.
import cv2
import PyCVQML

globalFaceTracking = None

class GUI: 
    def __init__(self,
                audio_processing = None,
                beamsteering = None,
                faceTracking = None,
                sensors = None,
                leds = None):
        global globalFaceTracking
        self._callback = None
        self._audio_processing = audio_processing
        self._beamsteering = beamsteering
        self._faceTracking = globalFaceTracking = faceTracking
        self._sensors = sensors
        self._leds = leds
        
    def run(self):
        PyCVQML.registerTypes()
        QtQml.qmlRegisterType(ImageProcessing, "Filters", 1, 0, "CaptureImage")
        
        main = MainWindow(self._audio_processing,
                        self._beamsteering,
                        self._faceTracking,
                        self._sensors,
                        self._leds)
        engine.rootContext().setContextProperty("backend", main)
        if LINUX and not DEBUG:
            engine.load(os.path.join(os.path.dirname(__file__), "qml/main_Linux.qml"))
        else:
            engine.load(os.path.join(os.path.dirname(__file__), "qml/main_Windows.qml"))
        app.lastWindowClosed.connect(self.terminate)   
        sys.exit(app.exec())
    
    def registerTerminateCallback(self, callback):
        self._callback = callback
        
    def terminate(self):
        PyCVQML.stopCamera()
        if(self._callback):
            self._callback()
    

class ImageProcessing(PyCVQML.CVAbstractFilter):
    def process_image(self, src):
        if globalFaceTracking:
            return globalFaceTracking.runDetection(src)
        return src

# Send and receive data from user interface
class MainWindow(QObject):
    def __init__(self, 
                audio_processing = None,
                beamsteering = None,
                faceTracking = None,
                sensors = None,
                leds = None):

        QObject.__init__(self)
        self._audio_processing = audio_processing
        self._beamsteering = beamsteering
        self._faceTracking = faceTracking
        self._sensors = sensors
        self._leds = leds

        self.source_list = []
        self.equalizer_list = []
        self.source_gain_value = 20
        self.beamsteering_pattern_list = []
        self.window_list = []
        self._gainSourceMax = 10
        self._maxAngleSlider = 45

    # Audio processing Source
    @pyqtProperty(list,constant=True)
    def sourceList(self):
        if not self._audio_processing == None:
            self.source_list = self._audio_processing.getSourceList()
            return self.source_list
        else:
            return ["Test 1","Test 2","Test 3"]


    @pyqtProperty(float)
    def sourceGainValue(self):
        if not self._audio_processing == None:
            self.source_gain_value = self._audio_processing.getSourceLevel()
            return self.source_gain_value
        else:
            return 1.0

    @pyqtSlot(int)
    def getSource(self, index):
        if not self._audio_processing == None:
            self._audio_processing.setSource(index)
        else:
            print(f"Source index: {index}")

    @pyqtSlot(float)
    def getSourceGain(self, gain):
        if not self._audio_processing == None:
            self._audio_processing.setGain((self._gainSourceMax-1)*gain + 1)
        else:
            print(f"Gain value: {(self._gainSourceMax-1)*gain + 1}")
    
    # Audio processing Equalizer
    @pyqtProperty(list, constant=True)
    def equalizerList(self):
        if not self._audio_processing == None:
            self.equalizer_list = self._audio_processing.getEqualizerProfileList()
            return self.equalizer_list
        else:
            return ["Test 1","Test 2","Test 3"]

    @pyqtSlot(int)
    def getEnableEqualizer(self, enable):
        if not self._audio_processing == None:
            self._audio_processing.enableEqualizer(enable)
        else:
            print(f"Equalizer enable: {enable}")

    @pyqtSlot(int)
    def getEqualizerProfile(self, profile):
        if not self._audio_processing == None:
            self._audio_processing.setEqualizerProfile(profile)
        else:
            print(f"Equalizer Profile: {profile}")

    # Audio processing interpolation
    @pyqtSlot(int)
    def getEnableInterpolation(self, enable):
        if not self._audio_processing == None:
            self._audio_processing.enableInterpolation(enable)
        else:
            print(f"Interpolation enable: {enable}")

    @pyqtSlot(int)
    def getInterpolationLevel(self, level):
        if not self._audio_processing == None:
            self._audio_processing.setInterpolationFactor(level)
        else:
            print(f"Interpolation level: {level}")

    # Audio processing modulation type
    @pyqtSlot(int)
    def getModulationType(self, type):
        if not self._audio_processing == None:
            self._audio_processing.setModulationType(type)
        else:
             print(f"Modulation type: {type}")

    @pyqtSlot(float)
    def getMAMGain(self, gain):
        if not self._audio_processing == None:
            self._audio_processing.setMAMMix(gain)
        else:
            print(f"MAM Distortion: {gain}")

    # Channels Beamsteering
    @pyqtProperty(list, constant=True)
    def beamsteeringPatternList(self):
        if not self._beamsteering == None:
            self.beamsteering_pattern_list = self._beamsteering.getBeamsteeringPattern()
            return self.beamsteering_pattern_list
        else:
             return ["Test 1","Test 2","Test 3"]

    @pyqtSlot(int)
    def getEnableBeamsteering(self, enable):
        if not self._beamsteering == None:
            self._beamsteering.enableBeamsteering(enable)
        else:
            print(f"Beamsteering enable: {enable}")

    @pyqtSlot(int)
    def getBeamsteeringSource(self, source):
        if not self._beamsteering == None:
            self._beamsteering.setBeamsteeringSource(source)
        else:
            print(f"Source: {source}")

    @pyqtSlot(float)
    def getBeamsteeringManualAngle(self, angle):
        if not self._beamsteering == None:
            self._beamsteering.setBeamsteeringAngle((2*angle - 1)*self._maxAngleSlider)
        else:
            print(f"Angle: {angle}")
    
    @pyqtSlot(int)
    def getBeamsteeringPattern(self, pattern):
        if not self._beamsteering == None:
            self._beamsteering.setBeamsteeringPattern(pattern)
        else:
            print(f"Beamsteering pattern: {pattern}")

    # Channels Window
    @pyqtProperty(list, constant=True)
    def windowList(self):
        if not self._beamsteering == None:
            self.window_list = self._beamsteering.getWindowProfileList()
            return self.window_list
        else:
            return ["Test 1","Test 2", "Test 3"]

    @pyqtSlot(int)
    def getEnableWindow(self, enable):
        if not self._beamsteering == None:
            self._beamsteering.setWindowProfile(0)
        else:
            print(f"Window enable: {enable}")

    @pyqtSlot(int)
    def getWindowType(self, type):
        if not self._beamsteering == None:
            self._beamsteering.setWindowProfile(type)
        else:
            print(f"Window type: {type}")

    # Settings LEDS
    @pyqtSlot(int)
    def getEnableLED(self, enable):
        if not self._leds == None:
            self._leds.enableChannels(enable)
        else:
            print(f"LEDs enable: {enable}")

    @pyqtSlot(float)
    def getLEDBrightness(self, value):
        if not self._leds == None:
            self._leds.setBrightness(value)
        else:
            print(f"LED: {value}")

    # Settings ToF
    @pyqtProperty(float)
    def ToFDistanceLevel(self):
        if not self._sensors == None:
            return self._sensors.getDistanceLevel()
        else:
            return 1.0

    @pyqtSlot(int)
    def getEnableToF(self, enable):
        print(f"ToF enable: {enable}")

    @pyqtSlot(float)
    def getToFDistance(self, value):
        print(f"ToF distance: {value}")

    # Settings max. volume
    @pyqtSlot(float)
    def getMaxVolume(self, value):
        print(f"Max. volume: {value}")

    # Settings stats
    
    @pyqtProperty(str)
    def AmbientTemperature(self):
        return "22.5 C"

    @pyqtProperty(str)
    def SystemTemperature(self):
        return "32.5 C" 

    @pyqtProperty(str)
    def CPUTemperature(self):
        return "42.5 C"

    @pyqtProperty(str)
    def CPULoad(self):
        return "50 %"

    # General information
    @pyqtProperty(int)
    def mainGainValue(self):
        return self.source_gain_value

    @pyqtSlot(float)
    def getMainGain(self, gain):
        print(f"Main gain: {gain}")
        pass
    @pyqtSlot(int)
    def getMuteEnable(self, enable):
        print(f"Mute enable: {enable}")
        pass

    




        
                  

if __name__ == "__main__":
    gui = GUI()
    gui.run()