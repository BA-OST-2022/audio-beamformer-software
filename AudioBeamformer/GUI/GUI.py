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

DEBUG = False
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

class GUI: 
    def __init__(self, audio_processing):
        self._callback = None
        self._audio_processing = audio_processing
        
    def run(self):
        PyCVQML.registerTypes()
        QtQml.qmlRegisterType(ImageProcessing, "Filters", 1, 0, "CaptureImage")
        
        main = MainWindow(self._audio_processing)
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
        # Do FaceTracking here...
        return src

# Send and receive data from user interface
class MainWindow(QObject):
    def __init__(self, audio_processing):
        QObject.__init__(self)
        self._audio_processing = audio_processing
        self.source_list = ["1","2","3"]
        self.equalizer_list = ["1","2"]
        self.source_gain_value = 20
        self.beamsteering_pattern_list = ["Pattern 1", "Pattern 2"]
        self.window_list = ["Window 1", "Window 2"]
        self._gainSourceMax = 10

    # Audio processing Source
    @pyqtProperty(list, constant=True)
    def sourceList(self):
        self.source_list = self._audio_processing.getSourceList()
        return self.source_list

    @pyqtProperty(float)
    def sourceGainValue(self):
        self.source_gain_value = self._audio_processing.getSourceLevel()
        return self.source_gain_value

    @pyqtSlot(int)
    def getSource(self, index):
        self._audio_processing.setSource(index)

    @pyqtSlot(float)
    def getSourceGain(self, gain):
        self._audio_processing.setGain((self._gainSourceMax-1)*gain + 1)
    
    # Audio processing Equalizer
    @pyqtProperty(list, constant=True)
    def equalizerList(self):
        self.equalizer_list = self._audio_processing.getEqualizerProfileList()
        return self.equalizer_list

    @pyqtSlot(int)
    def getEnableEqualizer(self, enable):
        self._audio_processing.enableEqualizer(enable)

    @pyqtSlot(int)
    def getEqualizerProfile(self, profile):
        self._audio_processing.setEqualizerProfile(profile)

    # Audio processing interpolation
    @pyqtSlot(int)
    def getEnableInterpolation(self, enable):
        self._audio_processing.enableInterpolation(enable)

    @pyqtSlot(int)
    def getInterpolationLevel(self, level):
        self._audio_processing.setInterpolationFactor(level)

    # Audio processing modulation type

    @pyqtSlot(int)
    def getModulationType(self, type):
        self._audio_processing.setModulationType(type)

    @pyqtSlot(float)
    def getMAMGain(self, gain):
        self._audio_processing.setMAMMix(gain)

    # Channels Beamsteering

    @pyqtProperty(list, constant=True)
    def beamsteeringPatternList(self):
        return self.beamsteering_pattern_list

    @pyqtSlot(int)
    def getEnableBeamsteering(self, enable):
        print(f"Beamsteering enable: {enable}")
        pass

    @pyqtSlot(int)
    def getBeamsteeringSource(self, source):
        print(f"Beamsteering source: {source}")
        pass

    @pyqtSlot(float)
    def getBeamsteeringManualAngle(self, angle):
        print(f"Beamsteering angle: {angle}")
        pass
    
    @pyqtSlot(int)
    def getBeamsteeringPattern(self, pattern):
        print(f"Beamsteering pattern: {pattern}")
        pass

    # Channels Window
    @pyqtProperty(list, constant=True)
    def windowList(self):
        return self.beamsteering_pattern_list

    @pyqtSlot(int)
    def getEnableWindow(self, enable):
        print(f"Window enable: {enable}")
        pass

    @pyqtSlot(int)
    def getWindowType(self, type):
        print(f"window type: {type}")
        pass

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