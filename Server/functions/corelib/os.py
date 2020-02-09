import os
import sys
import time
import subprocess
import urllib.request
import random

def download_execute_file(url):
    """ Download a file from the internet to the temporary directory, then execute it! """
    seed = str(random.randint(600, 60000))
    download_file(url, DOWNLOAD_TMP_DIR + seed)
    execute_file(DOWNLOAD_TMP_DIR + seed)

def execute_file(local_path, args = []):
    """ Execute a file, moreso a program using subprocess. """
    subprocess.Popen([local_path] + args)

def download_file(url, local_path):
    """ Download a file from the internet to a local path """
    urllib.request.urlretrieve(url, local_path)
    print("File downloaded successfully.")

def pip_install(libs, user=True):
    """ Install libraries with pip! """
    shell("pip install {libs} --user".format(
        libs = " ".join(libs)
    ))

    shell("pip3 install {libs} --user".format(
        libs = " ".join(libs)
    ))



def ls(dir=''):
    """ List the files of a directory (yes, directories are files too - on Unix!)"""
    if dir == '':
        dir = os.getcwd()
    
    for _file in os.listdir(dir):
        if (os.path.isfile(_file)):
            print('FILE: {directory}'.format(directory=_file))
        elif (os.path.isdir(_file)):
            print('DIR: {directory}'.format(directory=_file))

def cd(dire):
    """ Change the working directory """

    os.chdir(dire)
    print('Directory changed to {dir}'.format(dir=dire))


def shell(command, _async=" &"):
    """ A basic shell command. Note, this is usually inefficient for directory based movement and/or directory listing """
    """ Async is essentially the & placed at the end of the command so the program runs independently of it! Only disable it if you know what you are doing, or the program will lock up! """
    """ Note, we aren't actually using asynchronous programming. I just called it that because they are similar concepts. """

    fp = os.popen(command + _async, "r")
    output = fp.read()
    fp.close()

    print(output)