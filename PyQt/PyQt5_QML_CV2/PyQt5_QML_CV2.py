# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:29:59 2022

@author: flori
"""

import cv2
import numpy as np
from PyQt5 import QtGui, QtCore, QtQuick, QtQml
import PyCVQML

from PyQt5.QtGui  import QGuiApplication
from PyQt5.QtQml  import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl


class ImageProcessing(PyCVQML.CVAbstractFilter):
    def process_image(self, src):
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
                  
        
    def terminate(self):
        global runThreads
        runThreads = False



if __name__ == '__main__':
    import os
    import sys

    sys_argv = sys.argv
    sys_argv += ['--style', 'Material']
    app = QGuiApplication.instance()
    if app == None:
        app = QGuiApplication(sys.argv)
    if not QGuiApplication.instance():
        app = QGuiApplication(sys.argv)
    else:
        app = QGuiApplication.instance()

    PyCVQML.registerTypes()
    QtQml.qmlRegisterType(ImageProcessing, "Filters", 1, 0, "CaptureImage")
    
    # view = QtQuick.QQuickView()
    # view.setTitle("PyCVQML Example")
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # view.setSource(QtCore.QUrl.fromLocalFile(QtCore.QDir(dir_path).absoluteFilePath("main.qml")))
    # view.show()
    # sys.exit(app.exec_())
    
    engine = QQmlApplicationEngine()
    
    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    app.lastWindowClosed.connect(main.terminate)   
    sys.exit(app.exec())