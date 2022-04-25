# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 16:10:39 2022

@author: flori
"""

import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

runThreads = True

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        global runThreads
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)
        while runThreads:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
      		    gray,
           		scaleFactor=1.1,
           		minNeighbors=5,
           		minSize=(30, 30)
           		#flags = cv2.CV_HAAR_SCALE_IMAGE
            )

            print("Found {0} faces!".format(len(faces)))
    
            	# Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.changePixmap.emit(p)
        
        cap.release()
        cv2.destroyAllWindows()
        print("Thread Terminated...")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1000, 1000)
        # create a label
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()
   
    def terminate(self):
        global runThreads
        runThreads = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.lastWindowClosed.connect(ex.terminate)   
    sys.exit(app.exec_())