#!/usr/bin/env python
from conf import *

import pyaudio
import socket
import sys

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

def main():
    ip_address = sys.argv[1]
    callsign = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", AUDIO_PORT))
    s.listen()

    connfd = ""
    addr = ""

    while True:
        connfd, addr = s.accept()

        if (addr[0] != ip_address):
            connfd.close()
        
        their_callsign = connfd.recv(BUFFER_RECEIVE_SIZE).decode()

        if (their_callsign != callsign):
            connfd.close()

        break




    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    try:
        while True:
            data = connfd.recv(CHUNK)
            stream.write(data)
    except KeyboardInterrupt:
        pass

    print('Shutting down')
    s.close()
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    main()