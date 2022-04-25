import sys
import os
import cv2


from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import * #QObject#, Slot, Signal

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

class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)
        
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

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
            
    @pyqtSlot(QImage)
    def setImage(self, image):
        # self.label.setPixmap(QPixmap.fromImage(image))
        print(f"Update image: {image.width()} x {image.height()}")
        
        
    def terminate(self):
        global runThreads
        runThreads = False



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
    engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))

    app.lastWindowClosed.connect(main.terminate)   
    sys.exit(app.exec())
