#!/usr/bin/env python3
"""Play an audio file using a limited amount of memory.

The soundfile module (https://PySoundFile.readthedocs.io/) must be
installed for this to work.  NumPy is not needed.

In contrast to play_file.py, which loads the whole file into memory
before starting playback, this example program only holds a given number
of audio blocks in memory and is therefore able to play files that are
larger than the available RAM.

A similar example could of course be implemented using NumPy,
but this example shows what can be done when NumPy is not available.

"""
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
            
            
    
    # def callback(self, indata, outdata, frames, time, status):
    #     indata_oneCh = indata[:,0] * self._tot_gain 
    #     self.setSourceLevel(indata_oneCh)
    #     indata_oneCh *= self._output_enable
    #     if self._equalizer_enable:
    #         indata_oneCh = np.hstack((self.__previousWindow,
    #                                 indata_oneCh))
            
    #         outdata_oneCh = np.convolve(indata_oneCh,
    #                                     self._equalizer_filter,
    #                                     "valid")
    #         outdata_oneCh = np.float32(outdata_oneCh)
    #     else:
    #         outdata_oneCh = indata[:,0]
    #     # Modulation
    #     second_channel_data = self.__modulation_dict[self._modulation_index](outdata_oneCh)
    #     # Stich output together
    #     outdata[:] = np.column_stack((outdata_oneCh, second_channel_data))
    #     self.__previousWindow = indata_oneCh[-self.equ_window_size+1:]
    
    
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
    
    