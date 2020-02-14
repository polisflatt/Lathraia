
# Lathraia
An array of tools for "pentesting" GNU/Linux (as well as other systems which are compatible, namely BSD and whatnot). 

## Screenshots
Basic Python:
![Basic python](https://i.ibb.co/pZfFq2Y/2020-02-09-054739-1074x212-scrot.png)

Remote Desktop/Screen Server:
![enter image description here](https://i.ibb.co/DkxV01J/2020-02-14-065750-1366x768-scrot.png)



## Foreword
I do not condone the actions of Lathraia, despite creating it myself. It is disgraceful in my opinion, especially to the philosophy of Linux and free software (and yes, I am advocate of free software). I have mainly created this program as an experiment--a test of some sorts--of how much I could control another GNU/Linux machine, using software that I wrote myself. As a result, this software will not be sold under my name, ever; the purposes of which I have created this program for do not align with the wanting of financial gain. 

Additionally, I do not condone the usage of this program for malicious usage, but ultimately it is your decision whether you want to or not. This program is licensed under MIT so you can essentially do whatever you please. 

## What does Lathraia do? What is it?
Lathraia, as aforementioned, is, in essence, a program which is for pentesting and spyware purposes, for GNU/Linux and possibly the BSD variants. It seeks to give a person full control of one's computer, with stealth and surveillance capabilities. Additionally, Lathraia strives to be highly configurable, open source, well-commented, and written in a very simple and versatile language: Python. 

One of the major differences between Lathraia and another program of this type is that the functions which one may wish to execute are within Pythonic format. Lathraia is minimalist to such a degree that it is literally executing all Python code sent to it, meaning that you can make variables and import libraries, as you would in regular Python. Lathraia is similar to SSH, but it is packed with many more functions.

## What are the specific capabilities?
One should keep in mind that this program is not maintained very often, due to personal reasons; additionally, it should be noted that this program is at version 1.0, on its official release. The capabilities here will be improved in the future.

With that professed, Lathraia offers the following features:

 - Remote Python execution (effectively allowing everything)
 - OS & FS Functions (sh, copying and deleting, downloading, executing)
 - Remote desktop with remote mouse and remote keyboard (Truly).  
 - Camera stream (Note: this will turn on the webcam light, beware!)
 - Microphone recording (Note: this is experimental as of version 1.0)
 - Speech synthesis logging (Note: this is experimental as of version 1.0)
 - Keylogging, encoded in JSON.
 - Downloading and uploading files.
 - Fakesudo (Note: this is experimental as of version 1.0)
 
## Capabilities for the future
As aforementioned, we have several capabilities already configured on Lathraia, some fully and some not. However, as with all programs, we must look into the future, as we do with the present. We plan to include the following, under theoretical means (meaning that we'll try it, but it cannot be promised):

- FTP Uploading (if you want automatic uploads)
- Persistence
- LD_PRELOAD hacks (hide process name, etc)
- Include many ways to bind to startup
- Disabling the webcam light
- System log
- More complete and useful library, for the client and the server.

## Instructions
In order to run the server program, all you must do is run the main.py or compress it into a .zip with the main.py at the root directory, which does not obfuscate the program whatsoever, so please be wary of your IP address being leaked.

However, when running the client, you have many options, due to the fact that Lathraia is not monolithic, in the sense that it is made of other programs, working together to create what is known as Lathraia. You can choose to run Client/main.py, providing the IP address and the callsign of your server manually, or you can run the main program, run the listener, select which server you want to connect to, then the process is automatic. It is your choice. (Additionally, because of the nature of the program, you can reuse the programs for your own rat, especially the remote desktop, which harbors many features).

From here, once connected to the server, you can execute any Python command or function you wish -- which allows us to create versatile libraries and functions, because of Python's utter simplicity. If you want to read what is in the corelib, run help(functions.corelib).

I will relay some basic commands below that you can use. However, you can make your own easily, by adding a library into the functions folder, then explicitly importing it either automatically (through imports.py) or manually, through the import command. Additionally, some commands are under 'quick commands' where you do not have to add function braces or commas to run them.

Here are the aforementioned commands:

- cd() - Changes the current working directory.
- ls(dir="") - Lists the current working directory or a specific directory
- rm() - Deletes a file
- start_screen() - Starts the screen server on the server end. (To start the screen client, type $start_screen(), which runs the program on the client end)

Honestly, you can merely peer into the functions folder, and see for yourself what functions are included with Lathraia.


## Notes
Lathraia is not fully finished, but I decided to release the code anyway (mostly because I do not trust any of my hard drives to hold the sources; it would not be to my advantage if I were to lose all of my data). There will be many bugs -- and if you're a Python programmer, it should be quite simple to mend them, which is why I do not consider this program to be for the inexperienced; it is powerful, but you need Python knowledge to gain access full access to its power.

If you want this program to be improved, or if you want more features to be added, you can open an issue here on GitHub, or you can mend the program yourself and request it to be added to the main branch. I encourage the editing of this program -- to your hearts content, but please, although not required on basis of the licensing, cite the program's source.
