###############################################################################
# file    PacketInstaller.py
###############################################################################
# brief   Automaticaly checks for uninstalled packages and installs them
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-10-07
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

import importlib
import subprocess
import sys

LINUX = (sys.platform == 'linux')

class PacketInstaller:
    def __init__(self):
        self.packetList = [
            {"pip": "sounddevice", "import": "sounddevice"},
            {"pip": "soundfile", "import": "soundfile"},
            #{"pip": "opencv-python", "import": "cv2"}, # Do not import befor PyQt
            {"pip": "MNN", "import": "MNN"},
            {"pip": "torch", "import": "torch"},
            {"pip": "python-vlc", "import": "vlc"},
            {"pip": "netifaces", "import": "netifaces"},
            {"pip": "kaleido", "import": "kaleido"}]
            
        
    
    def check(self):
        for i in self.packetList:
            try:
                importlib.import_module(i["import"], package=None)
            except ModuleNotFoundError:
                print(f"Module <{i['import']}> not installed, try to install it...")
                self.install(i["pip"])
                try:
                    importlib.import_module(i["import"], package=None)
                except ModuleNotFoundError as e:
                    print(f"Could not install module, error: {e}")
        print("All necessary modules are installed")
                    
                

    def install(self, pck):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", pck])

pckInstaller = PacketInstaller()
pckInstaller.check()
if not LINUX:
    pckInstaller.install("PyQtChart")
