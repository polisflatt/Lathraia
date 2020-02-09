from configuration import *

import pyaudio
import socket
import select
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

fd = ""

def callback(in_data, frame_count, time_info, status):
    global fd
    fd.send(in_data)
    return (None, pyaudio.paContinue)

def main():
    while True:
        try:
            global fd
            # Initalize
            print("Initalizing PyAudio...")
            audio = pyaudio.PyAudio()

            # Sockets
            print("Creating sockets...")
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            fd = serversocket

            # Connect
            print("Connecting...")
            serversocket.connect((IP_ADDRESS, AUDIO_PORT))

            # Exchange callsign
            print("Giving callsign...")
            serversocket.send(CALLSIGN.encode())

            # Initalize
            print("Opened audio stream...")
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)
            # stream.start_stream()

            read_list = [serversocket]
            print("Recording...")

            
            while True:
                continue

            print("Exited.")

            serversocket.close()
            # stop Recording
            stream.stop_stream()
            stream.close()
            audio.terminate()
        except Exception as error:
            print(str(error))
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()