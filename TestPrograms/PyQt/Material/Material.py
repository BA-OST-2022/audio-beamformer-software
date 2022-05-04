# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 15:23:57 2022

@author: flori
"""

import sys

# from PySide6 import QtWidgets
# from PySide2 import QtWidgets
# from PyQt5 import QtWidgets
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

from qt_material import apply_stylesheet



themes = ['dark_amber.xml',
 'dark_blue.xml',
 'dark_cyan.xml',
 'dark_lightgreen.xml',
 'dark_pink.xml',
 'dark_purple.xml',
 'dark_red.xml',
 'dark_teal.xml',
 'dark_yellow.xml',
 'light_amber.xml',
 'light_blue.xml',
 'light_cyan.xml',
 'light_cyan_500.xml',
 'light_lightgreen.xml',
 'light_pink.xml',
 'light_purple.xml',
 'light_red.xml',
 'light_teal.xml',
 'light_yellow.xml']

# create the application and the main window
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

# setup stylesheet
apply_stylesheet(app, theme='dark_blue.xml')


widget = QWidget()
button1 = QPushButton(window)
button1.setText("Button1")
button1.move(64,32)

# run
window.show()

if hasattr(app, 'exec'):
    app.exec()
else:
    app.exec_()