# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:18:51 2022

@author: flori
"""

from PyQt5.QtGui  import QGuiApplication
from PyQt5.QtQml  import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl


class Main(QObject):
    def __init__(self):
        QObject.__init__(self)

    # signal sending string
    # necessarily give the name of the argument through arguments=['textLabel']
    # otherwise it will not be possible to pick it up in QML
    textResult = pyqtSignal(str, arguments=['textLabel'])

    @pyqtSlot(str)
    def textLabel(self, arg1):
        # do something with the text and emit a signal
        arg1 = arg1.upper()
        self.textResult.emit(arg1)


if __name__ == "__main__":
    import sys
    app    = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    main   = Main()
    engine.rootContext().setContextProperty("main", main)
    engine.load(QUrl('main.qml'))
    engine.quit.connect(app.quit)
    sys.exit(app.exec_())