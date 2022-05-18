###############################################################################
# file    AudioPlayer.py
###############################################################################
# brief   This module handles asynchronous playing of audio wav files
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-05-18
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

import queue
import sys
import threading
import numpy as np
import soundfile as sf


class AudioPlayer:
    def __init__(self, sampleRate=44100, blockSize=4096, bufferSize=20):
        self.event = threading.Event()
        
        self._runThread = False
        self._sampleRate = sampleRate
        self._blockSize = blockSize
        self._bufferSize = bufferSize
        self._filename = None
        self._q = queue.Queue(maxsize=self._bufferSize)
        


    def begin(self, filename):
        self._filename = filename
        self._runThread = True
        threading.Thread(target=self._run).start()


    def end(self):
        self._runThread = False
        
    
    def getData(self):
        try:
            return self._q.get_nowait()
        except queue.Empty:
            print('Buffer is empty: increase buffersize?', file=sys.stderr)
            return np.zeros(self._blockSize)


    def _run(self):
        try:
            with sf.SoundFile(self._filename) as f:
                for _ in range(self._bufferSize):
                    data = f.read(self._blockSize, dtype=np.int32)
                    self._q.put_nowait(data)  # Pre-fill queue
                
                timeout = self._blockSize * self._bufferSize / self._sampleRate
                while self._runThread:
                    data = f.read(self._blockSize, dtype=np.int32)
                    self._q.put(data, timeout=timeout)
                self.event.wait()  # Wait until playback is finished
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))


if __name__ == '__main__':
    import time
    import sounddevice as sd
    
    SAMPLE_RATE = 44100
    BLOCK_SIZE = 4096
    INPUT_DEVICE = 0
    OUTPUT_DEVICE = 3
    INPUT_COUNT = 2
    
    player = AudioPlayer(SAMPLE_RATE, BLOCK_SIZE)
    
    def callback(indata, outdata, frames, time, status):
        assert frames == BLOCK_SIZE
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        
        data = player.getData()
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data
    
    
    stream = sd.Stream(samplerate=SAMPLE_RATE,
                       blocksize=BLOCK_SIZE,
                       device=(INPUT_DEVICE , OUTPUT_DEVICE), 
                       channels=(INPUT_COUNT, 2),
                       dtype=np.int32,
                       callback=callback,
                       finished_callback=player.event.set)
    
    stream.start()
    print("Stream started...")
    
    player.begin("files/magic.wav")
    print("Player started")
    
    time.sleep(5)
    player.end()
    stream.close()
    print("Stop Stream and Player")
    
    