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

import numpy as np
from PyQt5 import QtGui, QtCore, QtQuick, QtQml
from PyQt5.QtGui  import QGuiApplication
from PyQt5.QtQml  import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl

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


class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

    # Static Info
    staticUser = "wanderson"
    staticPass = "123456"

    # Signals To Send Data
    #signalUser = Signal(str)
    #signalPass = Signal(str)
    #signalLogin = Signal(bool)

    # Function To Check Login
    #@Slot(str, str)
    def checkLogin(self, getUser, getPass):
        if(self.staticUser.lower() == getUser.lower() and self.staticPass == getPass):
            # Send User And Pass
            self.signalUser.emit("Username: " + getUser)
            self.signalPass.emit("Password: " + getPass)

            # Send Login Signal
            self.signalLogin.emit(True)
            print("Login passed!")
        else:
            self.signalLogin.emit(False)
            print("Login error!")
                  

if __name__ == "__main__":
    gui = GUI()
    gui.run()