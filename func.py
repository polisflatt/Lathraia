import os
import sys

from Client.conf import *
from Client.conf import intro_banner
from Client.functions import *

import Server.configuration
import Server.constants

import Client.listener
import Client.conf
import Client.main

import config
import func

import zipapp

SCRIPT_LOCATION = os.path.dirname(__file__)

_ip_address = ""
_callsign = ""

def client_launch_client():
    """ A function for launching the client, with the IP and callsign present in memory."""
    
    # Globals
    global _ip_address
    global _callsign

    # Error messages.
    if (_ip_address == ""):
        print("The client cannot be launched, because there is no ip address selected in memory. Run the listener?")
        return
    
    if (_callsign == ""):
        print("The client cannot be launched, because there is no callsign selected in memory. Run the listener?")
        return

    # Launch the main client.
    Client.main.main(ip_address = _ip_address, provided_callsign = _callsign)


def client_listener():
    """ A function for starting the listener and utilizing its information/data for our usages. """
    
    # Globals
    global _ip_address
    global _callsign

    conns = Client.listener.main()
    
    array_conn = int(input("Which connection? (the number): "))

    # Retrieve the IP address and callsign of the server and store it in memory, for the client.
    _ip_address = conns[array_conn][0]
    _callsign = conns[array_conn][1]

    # Print the status of whomever we're operating on.
    print("Currently operating on: {ip_addr}-{callsign}".format(
        ip_addr = _ip_address,
        callsign = _callsign
    ))


def server_builder():
    """ A function for building the server into a ZIP and/or future formats. """
    
    # Initalization and messages
    print(config.server_builder_text)
    input("Press any key and enter after you've configured the server.")

    # Printing some "basic"--relatively so--information.
    print("Printing some basic information:")

    # Print a fuckton of shit.
    print(config.server_information_text.format(
        version = Server.constants.VERSION,
        callsign = Server.configuration.CALLSIGN,
        ip = Server.configuration.IP_ADDRESS,
        port = Server.configuration.PORT,
        data_port = Server.configuration.DATA_PORT,
        video_port = Server.configuration.VIDEO_PORT,
        audio_port = Server.configuration.AUDIO_PORT
    ))


    print("Building with Python3 Zipapp (other ways of packaging will come in the future)")
    zip_name = input("Choose the output zipapp name: ")
    print(SCRIPT_LOCATION)

    build_dir = SCRIPT_LOCATION + "/" + config.build_dir

    # If the location does not exist, create it.
    # I honestly feel as if this should be a standard option with FS in Python, but alas: it is not.
    if (not os.path.exists(build_dir)):
        os.mkdir(build_dir)

    # Create the ZIP archive in whereever it was requested.
    zipapp.create_archive(SCRIPT_LOCATION + "/Server", build_dir + "/" + zip_name)
    print("Done building!")


def server_menu():
    """ The server options menu """
    
    # Loop, lest there is an error.
    while True:
        print(config.server_options_menu)
        command = input("Option: ")

        # Interpret the options and call functions
        if (command == "0"):
            server_builder()
        
        elif (command == "1"):
            print(config.server_help_text)
        else:
            print("Invalid option")
            continue

def client_menu():
    """ A function for displaying and utilizing the client menu """
    
    # Loop, lest an error occurs.
    while True:
        print(config.client_options_menu)
        command = input("Option: ")
        
        # Interpret the options
        if (command == "0"):
            client_launch_client()
            
        elif (command == "1"):
            client_listener()
        
        elif (command == "2"):
            print(config.client_help)
            
        else:
            print("Invalid option")
            continue
