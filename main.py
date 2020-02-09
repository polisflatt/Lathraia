import os
import sys
import json
import blessed
import Client.conf

import func
import config

from func import *
from config import *

os.chdir(os.path.dirname(Client.main.__file__))

# This is the main program, where everything happens.
# It's not too special, it just links everything together nicely.
# Due to its simplicity, please do not expect such eloquent code commenting as is present with the other programs.

def main():

    # Initalize blessed - the curses wrapper.
    t = blessed.Terminal()
    globals()["t"] = t

    # Print the introduction method and alike things.
    print(t.bold_red(Client.conf.intro_banner))
    print("Welcome to Latharia.")
    print("This is the main console, where you can do various things!")

    print(options_menu)

    # Interpret and execute options
    while True:
        command = input("Option: ")
        
        if (command == "0"):
            func.client_menu()
            break
        elif (command == "1"):
            func.server_menu()
            break
        else:
            print("Invalid option")
            continue



if __name__ == "__main__":
    main()