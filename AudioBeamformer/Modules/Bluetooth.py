###############################################################################
# file    Bluetooth.py
###############################################################################
# brief   Handels connection to Bluetooth devices
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-06-08
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
import threading

DEBUG = False
LINUX = (sys.platform == 'linux')
sys.path.insert(0, os.path.dirname(__file__)) 
sys.path.insert(0, os.path.dirname(__file__) + "/Modules")

if LINUX:
    import pydbus

class Bluetooth():
    def __init__(self, audioProcessing=None):
        self.audioProcessing = audioProcessing
        
        self._connectedDevices = []
        self._connectedDevicesCount = None
        self._runThread = False
        
        if LINUX:
            self.bus = pydbus.SystemBus()
            self.adapter = self.bus.get('org.bluez', '/org/bluez/hci0')
            self.mngr = self.bus.get('org.bluez', '/')
            
    def __del__(self):
        self.end()
    
    def begin(self, updateRate=2):
        self._runThread = True
        self._updateRate = updateRate
        threading.Timer(0, self.update).start()  
        
    def end(self):
        self._runThread = False
    
    def update(self):
        if self._runThread :
            threading.Timer(1.0 / self._updateRate, self.update).start()            
        else:
            return
        
        if LINUX:
            mngd_objs = self.mngr.GetManagedObjects()
            for path in mngd_objs:
                con_state = mngd_objs[path].get('org.bluez.Device1', {}).get('Connected', False)
                if con_state:
                    addr = mngd_objs[path].get('org.bluez.Device1', {}).get('Address')
                    name = mngd_objs[path].get('org.bluez.Device1', {}).get('Name')
                    self._connectedDevices.append(name)
                    if DEBUG:
                        print(f'Device {name} [{addr}] is connected')
        
        count = len(self._connectedDevices)
        if not self._connectedDevicesCount:
            self._connectedDevicesCount = count
        
        if count != self._connectedDevicesCount:
            if self.audioProcessing:
                self.audioProcessing.getSourceList()
            self._runThread = False
            print("Bluetooth Devices Updated, terminating module...")
        
            
    def getDevices(self):
        return self._connectedDevices


if __name__ == '__main__':
    bluetooth = Bluetooth()
    bluetooth.begin()
    print(f"Connected Devices: {bluetooth.getDevices()}")
    bluetooth.end()
    
    # Device Florians iPhone [40:9C:28:5C:A6:90] is connected
    # Device iPhone von Thierry [A8:81:7E:D2:BE:E9] is connected