###############################################################################
# file    WebRadio.py
###############################################################################
# brief   This module enables Web-Radio support
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-10-10
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

# https://www.srf.ch/hilfe/hilfe-sendetechnik/sendetechnik-live-radio-im-internet

import os
import sys
import vlc
import requests

DEBUG = False
LINUX = (sys.platform == 'linux')
# sys.path.insert(0, os.path.dirname(__file__)) 
# sys.path.insert(0, os.path.dirname(__file__) + "/Modules")


urls = ['http://stream.srg-ssr.ch/drs3/mp3_128.m3u'],
        # 'http://stream.srg-ssr.ch/drsmw/mp3_128.m3u']


class WebRadio:
    def __init__(self):
        if LINUX:
            self.instance = vlc.Instance("--aout=alsa", "--alsa-audio-device=dmix:CARD=Loopback,DEV=0")
        else:
            self.instance = vlc.Instance()
        self.playlists = set(['pls','m3u'])
        self.playState = False
        
        self.channels = [
            {"name": "SRF 1", "url": "http://stream.srg-ssr.ch/drs1/mp3_128.m3u"},
            {"name": "SRF 2", "url": "http://stream.srg-ssr.ch/drs2/mp3_128.m3u"},
            {"name": "SRF 3", "url": "http://stream.srg-ssr.ch/drs3/mp3_128.m3u"},
            {"name": "SRF 4 News", "url": "http://stream.srg-ssr.ch/drs4news/mp3_128.m3u"},
            {"name": "SRF Musikwelle", "url": "http://stream.srg-ssr.ch/drsmw/mp3_128.m3u"},
            {"name": "SRF Virus", "url": "http://stream.srg-ssr.ch/drsvirus/mp3_128.m3u"},
            {"name": "Energy Basel", "url": "https://energybasel.ice.infomaniak.ch/energybasel-high.mp3"},
            {"name": "Energy Bern", "url": "https://energybern.ice.infomaniak.ch/energybern-high.mp3"},
            {"name": "Energy Luzern", "url": "https://energyluzern.ice.infomaniak.ch/energyluzern-high.mp3"},
            {"name": "Energy St. Gallen", "url": "https://energystgallen.ice.infomaniak.ch/energystgallen-high.mp3"},
            {"name": "Energy Zürich", "url": "https://energyzuerich.ice.infomaniak.ch/energyzuerich-high.mp3"},
            {"name": "Radio Zürisee", "url": "http://mp3.radio.ch/radiozuerisee128k"},]
    
    
    def __del__(self):
        self.stop()
        
    
    def play(self, url):
        self.stop() 
        self.ext = (url.rpartition(".")[2])[:3]
        test_pass = False    
        try:
            if url[:4] == 'file':
                test_pass = True
            else:
                r = requests.get(url, stream=True)
                test_pass = r.ok
        except Exception as e:
            print(f'Failed to get stream: {e}')
            test_pass = False
        else:
            if test_pass:
                if DEBUG:
                    print('Start Web-Radio Stream')
                self.player = self.instance.media_player_new()
                if LINUX:
                    pass#self.player.audio_output_device("Loopback", 0)
                Media = self.instance.media_new(url)
                Media_list = self.instance.media_list_new([url])
                Media.get_mrl()
                self.player.set_media(Media)
                if self.ext in self.playlists:
                    self.list_player = self.instance.media_list_player_new()
                    self.list_player.set_media_list(Media_list)
                    if self.list_player.play() == -1:
                        print("Error playing playlist")
                else:
                    if self.player.play() == -1:
                        print("Error playing Stream")
                self.playState = True
            else:
                print('Error getting the audio')
    
    def stop(self):
        if self.playState:
            if self.ext in self.playlists:
                self.list_player.stop()
            else:
               self.player.stop()
            self.playState = False
            
    def getChannels(self):
        return [i["name"] for i in self.channels]

    
if __name__ == '__main__':
    from time import sleep
    
    radio = WebRadio()
    radio.play(radio.channels[0]["url"])
    print("Playing Radio for 15s...")
    sleep(15)
    radio.stop()
    print("Radio Stopped")
    
    