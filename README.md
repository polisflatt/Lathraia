
# Lathraia
An array of tools for "pentesting" GNU/Linux (as well as other systems which are compatible, namely BSD and whatnot). 

## Foreword
I do not condone the actions of Lathraia, despite creating it myself. It is disgraceful in my opinion, especially to the philosophy of Linux and free software (and yes, I am advocate of free software). I have mainly created this program as an experiment--a test of some sorts--of how much I could control another GNU/Linux machine, using software that I wrote myself. As a result, this software will not be sold under my name, ever; the purposes of which I have created this program for do not align with the wanting of financial gain. 

Additionally, I do not condone the usage of this program for malicious usage, but ultimately it is your decision whether you want to or not. This program is licensed under MIT so you can essentially do whatever you please. 

## What does Lathraia do? What is it?
Lathraia, as aforementioned, is, in essence, a program which is for pentesting and spyware purposes, for GNU/Linux and possibly the BSD variants. It seeks to give a person full control of one's computer, with stealth and surveillance capabilities. Additionally, Lathraia strives to be highly configurable, open source, and written in a very simple and versatile language: Python. 

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
