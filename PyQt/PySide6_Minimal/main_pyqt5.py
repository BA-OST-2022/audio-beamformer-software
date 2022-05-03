import sys
import os

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import * #QObject#, Slot, Signal


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

    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)
    engine.load(os.path.join(os.path.dirname(__file__), "qml/main_qt5.qml"))

    sys.exit(app.exec())
