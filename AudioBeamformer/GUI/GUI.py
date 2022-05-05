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
    def __init__(self):
        self._callback = None
        
    def run(self):
        PyCVQML.registerTypes()
        QtQml.qmlRegisterType(ImageProcessing, "Filters", 1, 0, "CaptureImage")
        
        main = MainWindow()
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
    def __init__(self):
        QObject.__init__(self)
        self.source_list = ["1","2","3"]
        self.equalizer_list = ["1","2"]
        self.source_gain_value = 20

    # Audio processing Source
    @pyqtProperty(list, constant=True)
    def sourceList(self):
        return self.source_list

    @pyqtProperty(int)
    def sourceGainValue(self):
        print("Call")
        return self.source_gain_value

    @pyqtSlot(str)
    def getSource(self, name):
        print(f"Source: {name}")
        pass

    @pyqtSlot(float)
    def getSourceGain(self, gain):
        print(f"Gain: {gain}")
        pass
    
    # Audio processing Equalizer
    @pyqtProperty(list, constant=True)
    def equalizerList(self):
        return self.equalizer_list

    @pyqtSlot(int)
    def getEnableEqualizer(self, enable):
        print(f"Equalizer: {enable}")
        pass

    @pyqtSlot(int)
    def getEqualizerProfile(self, profile):
        print(f"Equalizer profile: {profile}")
        pass

    # Audio processing interpolation
    @pyqtSlot(int)
    def getEnableInterpolation(self, enable):
        print(f"Interpolation enable: {enable}")
        pass

    @pyqtSlot(int)
    def getInterpolationLevel(self, level):
        print(f"Interpolation level: {level}")
        pass

    # Audio processing modulation type

    @pyqtSlot(int)
    def getModulationType(self, type):
        print(f"Modulation type: {type}")
        pass

    @pyqtSlot(int)
    def getMAMGain(self, gain):
        print(f"Interpolation level: {gain}")
        pass


    




        
                  

if __name__ == "__main__":
    gui = GUI()
    gui.run()