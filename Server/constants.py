import os

# This file is to be used for defining constants
# It is useful, for instance, for home directories, etc. 
# So that you can easily find it!

# Server information
VERSION = "v1.0 - First release"

# Paths
PATH_HOME_FOLDER = os.path.expanduser("~")
H = PATH_HOME_FOLDER # Condensed home folder var name
PATH_DOWNLOADS = PATH_HOME_FOLDER + "/Downloads/"
PATH_CACHE = PATH_HOME_FOLDER + "/.cache/"
PATH_CONFIG = PATH_HOME_FOLDER + "/.config/"
PATH_TMP = "/tmp/"
PATH_SYS_PROGRAMS = "/bin/"
PATH_USR_PROGRAMS = "/usr/bin/"
PATH_ROOT_HOME = "/root/" # Requires root access

# Environment 'variables'/constants
USERNAME = os.getenv("USER")
HOSTNAME = os.getenv("HOSTNAME")
TERM = os.getenv("TERM")
OSTYPE = os.getenv("OSTYPE")
LANG = os.getenv("LANG")

