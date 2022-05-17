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

import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 44100
BUFFER_SIZE = 20
BLOCK_SIZE = 4096
FILE_NAME = "files/magic.wav"
OUTPUT_DEVICE = 3


q = queue.Queue(maxsize=BUFFER_SIZE)
event = threading.Event()


def callback(outdata, frames, time, status):
    assert frames == BLOCK_SIZE
    if status.output_underflow:
        print('Output underflow: increase blocksize?', file=sys.stderr)
        raise sd.CallbackAbort
    assert not status
    try:
        data = q.get_nowait()
    except queue.Empty:
        print('Buffer is empty: increase buffersize?', file=sys.stderr)
        raise sd.CallbackAbort
    if len(data) < len(outdata):
        outdata[:len(data)] = data
        outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
        raise sd.CallbackStop
    else:
        outdata[:] = data


try:
    with sf.SoundFile(FILE_NAME) as f:
        for _ in range(BUFFER_SIZE):
            data = f.buffer_read(BLOCK_SIZE, dtype='float32')
            if not data:
                break
            q.put_nowait(data)  # Pre-fill queue
        stream = sd.RawOutputStream(
            samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE,
            device=OUTPUT_DEVICE, channels=f.channels, dtype='float32',
            callback=callback, finished_callback=event.set)
        with stream:
            timeout = BLOCK_SIZE * BUFFER_SIZE / SAMPLE_RATE
            while data:
                data = f.buffer_read(BLOCK_SIZE, dtype='float32')
                q.put(data, timeout=timeout)
            event.wait()  # Wait until playback is finished
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
    