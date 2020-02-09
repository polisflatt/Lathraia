# Latharia Screen Client!
# Supports remote mouse and keyboard!
# ... for GNU/Linux!

# Inspiration was taken from https://stackoverflow.com/questions/48950962/screen-sharing-in-python.


import socket
import threading
import time

from zlib import decompress

from conf import *
from functions import *

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# Disable Pygame's annoying prompt

from pygame.locals import *

import pygame
import sys

def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


# The thread which does a lot of the pygame detections
# Needs to be separate for preformance reasons
def pygame_update(conn, remote_mouse, remote_keyboard, w, h):
    """ Update pygame """
    while True:
        for event in pygame.event.get():
            # Window is resizing, so scale the image!
            if event.type == pygame.VIDEORESIZE:
                globals()["w"] = event.w
                globals()["h"] = event.h
            
            # Key was pressed, so lets send it over to the server
            # In order for the server to detect a keyboard press, we prefix it with
            # the arbitrary 'k:'
            # The format is in k:key

            elif event.type == pygame.KEYDOWN:
                if (remote_keyboard):
                    conn.send("k:{key}".format(key = pygame.key.name(event.key)).encode()) 

            # Mouse click was detected on PyGames window
            # Here's the tricky part. How can we get the correct, corrosponding coordinates
            # when the screen is (most likely!) scaled?
            # Here's where the bit of math comes in!

            # We will prefix this with m:
            # The format is in: m:x/y

            elif event.type == pygame.MOUSEBUTTONUP:
                if (remote_mouse):
                    pos = pygame.mouse.get_pos()

                    # Use ratios?
                    # rX = x3 * (x1/x2)
                    # real x = clicked x * (actual x/scaled x)
                    #----------------------^
                    #^ Scale factor

                    real_coord_x = str(round(pos[0] * (w/globals()["w"])))
                    real_coord_y = str(round(pos[1] * (h/globals()["h"])))

                    conn.send("m:{x}/{y}".format(
                        x = real_coord_x,
                        y = real_coord_y
                    ).encode())
        #time.sleep(client_screen_sleeping_interval)
        time.sleep(.01)

def main(ip_address = "", callsign = "", remote_keyboard = "", remote_mouse = ""):
    pygame.init()

    # If this program is not being started by the client, then we shall receive parameters
    # through command line arguments.

    if (ip_address == ""):
        ip_address = sys.argv[1]

    if (callsign == ""):
        callsign = sys.argv[2]

    if (remote_keyboard == ""):
        remote_keyboard = int(sys.argv[3])

    if (remote_mouse == ""):
        remote_mouse = int(sys.argv[4])

    print(intro_banner)
    print("Video client!")
    print("Waiting for connections...")

    # Socket setup
    # This is fairly standard for you now. I can see that.

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", VIDEO_PORT))
    sock.listen()

    conn = ""
    addr = ""

    

    while True:
        conn, addr = sock.accept()
        print("A connection from {ip} has been made!".format(ip = addr[0]))

        their_callsign = conn.recv(BUFFER_RECEIVE_SIZE).decode()

        # Detect interference
        if (addr[0] != ip_address):
            dprint("VIDEO: Incorrect IP Address, returning!")
            continue


        if (their_callsign != callsign):
            dprint("VIDEO: Incorrect callsign '{callsign}', returning!".format(
                callsign = their_callsign
            ))

            continue

        break


        


    try:
        # Receive the dimensions of the image being sent to us
        # This imperative!
        
        w = int(conn.recv(BUFFER_RECEIVE_SIZE).decode())
        h = int(conn.recv(BUFFER_RECEIVE_SIZE).decode())

        # Initalize the screen, so that it allows resizing!
        screen = pygame.display.set_mode((w, h), HWSURFACE|DOUBLEBUF|RESIZABLE)
        clock = pygame.time.Clock()

        # Set up the pygame display captions
        pygame.display.set_caption("Desktop/Camera from: {ip}:{port}".format(
            ip = addr[0],
            port = addr[1]
        ))

        # Set defaults, in case of an error with the below statement.
        globals()["w"] = w
        globals()["h"] = h


        threading._start_new_thread(pygame_update, (conn, remote_mouse, remote_keyboard, w, h,))
        while True:
            
            # Detect a change within the window size and reset the variables corrosponding
            # to the width and height of the window I love fucking typing this !!!!
            
            # Retreive the size of the pixels length, the pixels length and pixels
            size_len = int.from_bytes(conn.recv(1), byteorder='big')
            size = int.from_bytes(conn.recv(size_len), byteorder='big')
            pixels = decompress(recvall(conn, size))
            
            # Create the Surface from raw pixels
            img = pygame.image.fromstring(pixels, (w, h), 'RGB')
            #_w, _h = pygame.display.get_surface().get_size()

            # Scale image by new size
            img = pygame.transform.scale(img, (int(globals()["w"]), int(globals()["h"])))

            _w, _h = pygame.display.get_surface().get_size()            
            
            # Display the picture
            screen.blit(img, (0, 0))
            pygame.display.flip()
            clock.tick(60)
    except Exception as error:
        dprint(str(error))
    finally:
        conn.close()


if __name__ == '__main__':
    main()