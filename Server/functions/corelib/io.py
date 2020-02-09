import os
import socket
import time
import sys





def read(_f):
    """ Print and read out a file back to the client """
    print(open(_f, 'r').read())
    print("End of file read.")

def write(_f, contents, mode):
    """ Quickly write to a file """
    """ Additionally, the client could merely open(file).write() for some actual pythonic code"""
    open(_f, mode).write(contents)
    print("{size} bytes have been written to file {_file} successfully.".format(
        size = len(contents),
        _file = _f
    ))

def rm(_f):
    """ Remove a file """
    shell('rm {f}'.format(f=_f))
    print("File removed successfully.")


def mv(_f, _new_file):
    """ Move or rename a file """
    shell('mv {f} {newfile}'.format(f=_f, newfile=_new_file))
    print("File moved successfully.")


def upload(filename):
    """ Upload a file """
    global s

    _filename = os.path.basename(filename)
    s.fconnfd.send('{filename}:{size}'.format(filename=_filename, size=(os.path.getsize(filename))).encode())
    s.fconnfd.send(open(filename, 'rb').read())
    print('File upload completed!')


def get_con():
    global s
    s = globals()["server"]
    print(s.recvall(self.socketfd, 256).decode())