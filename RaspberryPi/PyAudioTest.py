#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 22:32:19 2022

@author: root
"""

"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).
This is the callback (non-blocking) version.
"""


# https://www.tutonaut.de/raspberry-pi-als-bluetooth-airplay-empfaenger-kombi/


import pyaudio
import time

WIDTH = 2
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)

for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()