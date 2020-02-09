import os
import time
import sys
import socket
import requests
import json
import threading
import multiprocessing


from functions import *
from conf import *

# Lazily placed function, I know.
# However, it does not readily matter.

listen_on = True

mem_people = {

}

array_mem_people = [

]

# This program is a very simple one. It acts as if it is the client, but instead of sending commands
# it checks for everyone who is connecting to it, prints them out, and makes sure it doesn't
# print them again. This will give you a rough image of who you can connect to at the moment and
# who is currently online now.

# This listens for incoming connections
def _listener(socketfd):

    # Global declarations
    global mem_people
    global array_mem_people
    global listen_on
    
    while listen_on:
        connfd, addr = socketfd.accept()
        callsign = connfd.recv(BUFFER_RECEIVE_SIZE).decode()

        # We've already got this person
        try:
            if (mem_people[addr[0]] == callsign):
                connfd.close()
                continue
        except:
            pass

        # Memorize that we've got a signal from this person
        mem_people[addr[0]] = callsign
        
        # Also take note of who we had so that we can return it later, making it easier to 
        # select who we want to connect to.

        array_mem_people.append(
            [addr[0], callsign]
        )

        # Tell you who's connected

        ip = addr[0]
        port = addr[1]

        # Execute each custom listener display
        for ldisplay in listener_displays:
            try:
                exec(ldisplay)
            except Exception as error:
                print("Error executing listener display: {error}".format(error = str(error)))


        connfd.close()


def main():
    print(intro_banner)
    print("Listener!")
    print("See who's connecting to you!")

    global mem_people
    global array_mem_people
    global listen_on

    socketfd = socket.socket()
    socketfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketfd.bind(("", PORT))
    socketfd.listen()

    # Start actual listener
    threading._start_new_thread(_listener, (socketfd,))

    print("Type 'quit' to quit the listener.")

    while True:
        cmd = input("Lathraia-Listener> ")
        if (cmd == "quit"):
            socketfd.close()
            listen_on = False
            return array_mem_people


if __name__ == "__main__":
    main()
