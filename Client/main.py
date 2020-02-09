import os
import sys
import threading
import time
import socket

import blessed

import readline

from conf import *
from functions import *
from client import *


# This program is getting far more bloated than I wanted it to be.
# I am striving for maximum readability, but it's becoming difficult as the complexity of
# this program augments far beyond my control!

def main(ip_address = "", provided_callsign = ""):
    """ Main function. """
    # We cleaned up a lot here.

    # Set up the terminal.
    t = blessed.Terminal()

    # Detect whether we are starting through a library or through directly executing this file.
    if (ip_address == ""):
        ip_address = sys.argv[1]

    if (provided_callsign == ""):
        provided_callsign = sys.argv[2]

    # Display our branding.
    print(t.bold_red(intro_banner))
    sys.stdout.write(intro_message)

    # Start the client 
    # I finally made all of this object oriented!
    # I feel so proud!

    c = Client(ip_address, provided_callsign)

    # Setup readline, so that we can enjoy it
    readline.parse_and_bind("tab: complete")    

    # Main loop.
    # You can see that it is superlatively primitive. It is quite meant to be like that.


    # Make the client global, for other functions which want to use it
    client_global(c)

    print("\nYou are now fully connected!\n")
    while True:
        command = input(PROMPT.format(
            cwd = c.cwd()
        ))
        
        c.interpret_command(command)


        


if __name__ == "__main__":
    main()