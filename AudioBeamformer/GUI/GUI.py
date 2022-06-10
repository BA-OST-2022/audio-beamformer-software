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

from doctest import ELLIPSIS_MARKER
import os
import sys
import datetime
import numpy as np
from PyQt5 import QtGui, QtCore, QtQuick, QtQml
#from PyQt5.QtGui  import QGuiApplication
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml  import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl, pyqtProperty
from pathlib import Path

DEBUG = False
LINUX = (sys.platform == 'linux')
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(__file__) + "/PyCVQML")

sys_argv = sys.argv
sys_argv += ['--style', 'Material']
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication.instance()
if app == None:
    app = QApplication(sys.argv)
if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()
engine = QQmlApplicationEngine()

# Important: Must be imported after creating Qt instance, this is a known bug.
import cv2
import PyCVQML


class GUI: 
    def __init__(self,
                audio_processing = None,
                beamsteering = None,
                faceTracking = None,
                sensors = None,
                leds = None,
                bluetooth = None):
        
        self.MODULE_AUDIO_PROCESSING = 0
        self.MODULE_BEAMSTEERING = 1
        self.MODULE_FACE_TRACKING = 2
        self.MODULE_SENSORS = 3
        self.MODULE_LEDS = 4
        
        self._callback = None
        self._audio_processing = audio_processing
        self._beamsteering = beamsteering
        self._faceTracking = faceTracking
        self._sensors = sensors
        self._leds = leds
        self._bluetooth = bluetooth
        
    def run(self):
        PyCVQML.registerTypes()
        PyCVQML.registerCallback(self.imageCallback)
        QtQml.qmlRegisterType(ImageProcessing, "Filters", 1, 0, "CaptureImage")
        
        main = MainWindow(self._audio_processing,
                        self._beamsteering,
                        self._faceTracking,
                        self._sensors,
                        self._leds,
                        self._bluetooth)
        engine.rootContext().setContextProperty("backend", main)
        if LINUX and not DEBUG:
            engine.load(os.path.join(os.path.dirname(__file__), "qml/main_Linux.qml"))
        else:
            engine.load(os.path.join(os.path.dirname(__file__), "qml/main_Windows.qml"))
        app.lastWindowClosed.connect(self.terminate)   
        sys.exit(app.exec())
    
    def registerTerminateCallback(self, callback):
        self._callback = callback
        
        
    def setModuleReference(self, module, reference):
        if(module == self.MODULE_AUDIO_PROCESSING):
            self._audio_processing = reference
        elif(module == self.MODULE_BEAMSTEERING):
            self._beamsteering = reference
        elif(module == self.MODULE_FACE_TRACKING):
            self._faceTracking = reference
        elif(module == self.MODULE_SENSORS):
            self._sensors = reference
        elif(module == self.MODULE_LEDS):
            self._leds = reference
     
        
    def terminate(self):
        PyCVQML.stopCamera()
        if(self._callback):
            self._callback()
            
    def imageCallback(self, src):
        if LINUX:
            src = cv2.rotate(src, cv2.ROTATE_180)
        if self._faceTracking:
            return self._faceTracking.runDetection(src)
        return src

    
class ImageProcessing(PyCVQML.CVAbstractFilter):
    def process_image(self, src):
        pass   # Placeholder Class


# Send and receive data from user interface
class MainWindow(QObject):
    def __init__(self, 
                audio_processing = None,
                beamsteering = None,
                faceTracking = None,
                sensors = None,
                leds = None,
                bluetooth = None):

        QObject.__init__(self)
        self._audio_processing = audio_processing
        self._beamsteering = beamsteering
        self._faceTracking = faceTracking
        self._sensors = sensors
        self._leds = leds
        self._bluetooth = bluetooth

        self.source_list = []
        self.equalizer_list = []
        self.source_gain_value = 20
        self.beamsteering_pattern_list = []
        self.window_list = []
        self._windowProfileIndex = 0
        self._gainSourceMax = 10
        self._maxAngleSlider = 45
        self.__enableChannels = np.zeros(19)
        self.__mutePath = Path("images") / "Mute_grey.png"
        self.__unmutePath = Path("images") / "Unmute_grey.png"
        self.__eq_1_int_1_am_1 = Path("images") / "All_active_AM.svg"
        self.__eq_0_int_1_am_1 = Path("images") / "eq_0_int_1_AM.svg"
        self.__eq_0_int_0_am_1 = Path("images") / "eq_0_int_0_AM.svg"
        self.__eq_1_int_0_am_1 = Path("images") / "eq_1_int_0_AM.svg"
        self.__eq_1_int_1_am_0 = Path("images") / "All_active_MAM.svg"
        self.__eq_0_int_1_am_0 = Path("images") / "eq_0_int_1_MAM.svg"
        self.__eq_0_int_0_am_0 = Path("images") / "eq_0_int_0_MAM.svg"
        self.__eq_1_int_0_am_0 = Path("images") / "eq_1_int_0_MAM.svg"
        self.__am_holder = Path("images") / "AM_Holder.svg"
        self.__loadingImage = Path("images") / "Audio-Beamformer_Gray.png"
        self.__eq_path = Path("images") / "eq_"
        self.__window_path = Path("images") / "window_" 
        self.__interpol_path = Path("images") / "Interpolation_" 
        self.__elvision_path = Path("images") / "Elvision.jpg"
        self.__frame_path = Path("images") / "Rahmen.svg"
        self.__play_img = Path("images") / "play.svg"
        self.__pause_img = Path("images") / "pause.svg"
        self.__speech_bubble = Path("images") / "SpeechBubble.svg"
        self.__equalizer_profile = 0
        if self._audio_processing:
            self.__equalizer_holder = self._audio_processing.getEqualizerList()
        


    @pyqtProperty(bool)
    def readyState(self):
        if self._sensors:
            return self._sensors.getReadyState()    
        else:
            return True

    # Audio processing Source
    @pyqtProperty(list,constant=True)
    def sourceList(self):
        if not self._audio_processing == None:
            self.source_list = self._audio_processing.getSourceList()
            self._audio_processing.setupStream()
            self._audio_processing.startStream()
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
            self._audio_processing.setGain(10**(24*(gain-0.5)/20))
        else:
            print(f"Gain value: {10**(24*(gain-0.5)/20)}")
    
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
            self._equalizer_profile = profile
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
        if self._beamsteering:
            self._beamsteering.enableWindow(enable)
        else:
            print(f"Window enable: {enable}")

    @pyqtSlot(int)
    def getWindowType(self, type):
        self._windowProfileIndex = type
        if not self._beamsteering == None:
            self._beamsteering.setWindowProfile(self._windowProfileIndex)
        else:
            print(f"Window type: {self._windowProfileIndex}")

    # Settings LEDS
    @pyqtSlot(int)
    def getEnableLED(self, enable):
        if not self._leds == None:
            self._leds.enableChannels(enable)
            self._leds.enableCamera(enable)
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
        return 1.0

    @pyqtSlot(int)
    def getEnableToF(self, enable):
        if not self._sensors == None:
            self._sensors.enableAlert(enable)
        else:
            print(f"ToF enable: {enable}")

    @pyqtSlot(float)
    def getToFDistance(self, value):
        if not self._sensors == None:
            self._sensors.setAlertSensitivity(value)
        else:
            print(f"ToF distance: {value}")

    # Settings max. volume
    @pyqtSlot(float)
    def getMaxVolume(self, value):
        if not self._sensors == None:
            self._sensors.setMaxVolume(value)
        else:
            print(f"Max. volume: {value}")

    # Beamfocusing
    @pyqtSlot(float)
    def getFocusDistance(self, distance):
        if self._beamsteering:
            self._beamsteering.setBeamfocusingRadius(1 + 9*distance)
        else:
            print(f"Focus distance: {10*distance}")

    @pyqtSlot(bool)
    def enableBeamfocusing(self, enable):
        if self._beamsteering:
            self._beamsteering.enableBeamfocusing(enable)
        else:
            print(f"Beamfocusing enable: {enable}")
    # Settings stats
    
    @pyqtProperty(str)
    def AmbientTemperature(self):
        if not self._sensors == None:
            return f"{self._sensors.getTemperature(self._sensors.SRC_AMBIENT):.1f} °C"
        else:
            return "None"

    @pyqtProperty(str)
    def SystemTemperature(self):
        if not self._sensors == None:
            return f"{self._sensors.getTemperature(self._sensors.SRC_SYSTEM):.1f} °C"
        else:
            return "None" 

    @pyqtProperty(str)
    def CPUTemperature(self):
        if not self._sensors == None:
            return f"{self._sensors.getTemperature(self._sensors.SRC_CPU):.1f} °C"
        else:
            return "None" 

    @pyqtProperty(str)
    def deviceCount(self):
        if self._bluetooth:
            return str(len(self._bluetooth.getDevices()))
        else:
            return "None"

    @pyqtProperty(str)
    def deviceList(self):
        if self._bluetooth:
            return "\n".join(self._bluetooth.getDevices())
        else:
            return "Test 1 \nTest 2"


    @pyqtProperty(str)
    def CPULoad(self):
        if not self._sensors == None:
            return f"{self._sensors.getCpuLoad():.1f} %"
        else:
            return "None" 

    # Settings channel
    @pyqtSlot(list)
    def getEnableChannels(self, list):
        if not all(i==u for i,u in zip(self.__enableChannels,list)):
            if self._beamsteering:
                self._beamsteering.setChannelEnable(list)
            else:
                print(f"Channel Gains: {list}")
            self.__enableChannels = list

    # General information
    @pyqtProperty(float)
    def mainGainValue(self):
        if not self._sensors == None:
            return self._sensors.getVolume()
        else:
            return 0

    @pyqtProperty(bool)
    def muteEnable(self):
        if not self._sensors == None:
            return self._sensors.getMute()
        else:
            return False

    @pyqtSlot(float)
    def getMainGain(self, gain):
        if not self._sensors == None:
            self._sensors.setVolume(gain)
        else:
            print(f"Main gain: {gain}")

    @pyqtSlot(int)
    def getMuteEnable(self, enable):
        if not self._sensors == None:
            self._sensors.setMute(enable)
        else:
            print(f"Mute enable: {enable}")

    @pyqtProperty(str, constant=True)
    def getMuteImagePath(self):
        return str(self.__mutePath)

    @pyqtProperty(str, constant=True)
    def getUnmuteImagePath(self):
        return str(self.__unmutePath)

    @pyqtProperty(str, constant= True)
    def path_0_0_0(self):
        return str(self.__eq_0_int_0_am_0)

    @pyqtProperty(str, constant= True)
    def path_0_0_1(self):
        return str(self.__eq_0_int_0_am_1)

    @pyqtProperty(str, constant= True)
    def path_0_1_0(self):
        return str(self.__eq_0_int_1_am_0)

    @pyqtProperty(str, constant= True)
    def path_0_1_1(self):
        return str(self.__eq_0_int_1_am_1)

    @pyqtProperty(str, constant= True)
    def path_1_0_0(self):
            return str(self.__eq_1_int_0_am_0)

    @pyqtProperty(str, constant= True)
    def path_1_0_1(self):
        return str(self.__eq_1_int_0_am_1)

    @pyqtProperty(str, constant= True)
    def path_1_1_0(self):
            return str(self.__eq_1_int_1_am_0)

    @pyqtProperty(str, constant= True)
    def path_1_1_1(self):
        return str(self.__eq_1_int_1_am_1)
    
    @pyqtProperty(str, constant= True)
    def amHolder(self):
        return str(self.__am_holder)
    
    @pyqtProperty(str, constant= True)
    def eqPath(self):
        return str(self.__eq_path)

    @pyqtProperty(str, constant= True)
    def interpolPath(self):
        return str(self.__interpol_path)

    @pyqtProperty(str, constant = True)
    def windowPath(self):
        return str(self.__window_path)

    @pyqtProperty(str, constant=True)
    def loadingImage(self):
        return str(self.__loadingImage)

    @pyqtProperty(str, constant = True)
    def framePath(self):
        return str(self.__frame_path)

    @pyqtProperty(str, constant=True)
    def elvisionPath(self):
        return str(self.__elvision_path)

    @pyqtProperty(str, constant=True)
    def pausePath(self):
        return str(self.__pause_img)

    @pyqtProperty(str, constant=True)
    def playPath(self):
         return str(self.__play_img)
     
    @pyqtProperty(bool)
    def getAlertState(self):
        if self._sensors:
            return self._sensors.getAlertState() 
        else:
            return False

    @pyqtProperty(str, constant=True)
    def speechPath(self):
        return str(self.__speech_bubble)

    @pyqtProperty(list)
    def getEqualizerList(self):
        if self._audio_processing:
            return self.__equalizer_holder[self.__equalizer_profile]
        else:
            return [[1,2],[2,3],[4,5],[6,7]]


    # Magic Mode
    @pyqtSlot(bool)
    def enableMagicMode(self, enable):
        if self._audio_processing:
            self._audio_processing.enableMagic(enable)

        if self._faceTracking:
            self._faceTracking.enableMagic(enable)

        if self._leds:
            self._leds.enableMagic(enable)

        if self._sensors:
            self._sensors.enableMagic(enable)

    # AudioPlayer
    @pyqtSlot(bool)
    def enablePlayer(self,enable):
        if self._audio_processing:
            self._audio_processing.playPausePlayer()
        else:
            print(f"Audio Player: {enable}")

    @pyqtSlot(int)
    def audioFileIndex(self,index):
        if self._audio_processing:
            self._audio_processing.setAudioFileIndex(index)
        else:
            print(f"Audio Player index: {index}")

    @pyqtProperty(list)
    def getAudioFiles(self):
        if self._audio_processing:
            return self._audio_processing.getAudioFiles()
        else:
            return ["Test 1","Test 2","Test 3"]

    @pyqtProperty(bool)
    def getPlayerState(self):
        if self._audio_processing:
            return self._audio_processing.getPlayerState()
        else:
            return False



if __name__ == "__main__":
    gui = GUI()
    gui.run()