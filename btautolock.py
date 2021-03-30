#!/usr/bin/env python3
import sys
import subprocess as sp
import time
import os
import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
import tkinter as tk



#Replaces only part of the file, keeping one line
def fileReplacePart(dest, toWrite, toKeep, toReplace):
    read = open(dest, 'r')
    readLines = read.readlines()
    if len(readLines) > toKeep:
        keep = readLines[toKeep]
        read.close()
        read = open(dest, 'w')
        if toKeep > toReplace:
            read.write(toWrite + keep)
        else:
            read.write(keep + "\n" + toWrite)
        read.close()



if(len(sys.argv) > 1):
    if sys.argv[1] == "setmac":
       newMAC = str(input("Please enter the BT address of the new device you wish to use as your lock: ")) 
       fileReplacePart("btautolock.conf", newMAC, 1, 0)
       print("new lock MAC is " + newMAC)
       quit()
        
    elif sys.argv[1] == "setdelay":
        newDelay = str(input("Please enter the delay (in ms) you want between your lock device disonnecting and your computer locking: "))
        fileReplacePart("btautolock.conf", newDelay, 0, 1)
        print("delay successfully set to " + newDelay + " ms.")
        quit()
        
    elif sys.argv[1] == "help":
        print("Bluetooth Auto Lock\nOPTIONS:\n\t\"setdelay\": set the time to wait (in ms) after the device disconnects from bluetooth to lock the machine\n\t\"setmac\": set the Bluetooth MAC address of your device\n\t\"help\": Display this message.\n")
        quit()
        

#read the configfile and set the configs appropriately
configFile = open('btautolock.conf', 'r')
configLines = configFile.readlines()
deviceMAC = configLines[0].strip()
lockDelay = int(configLines[1])
configFile.close()

locked = False
connected = False
playerInitialized = False

os.system('nohup ./media_control.py')
while (True):
    btcon = sp.getoutput("hcitool con")
    if not (deviceMAC in btcon):
        connected = False
    elif (deviceMAC in btcon):
        connected = True
    if not (deviceMAC in btcon) and locked == False:
        time.sleep(lockDelay/1000)
        locked = True
        
        os.popen('cinnamon-screensaver-command --lock')
    elif deviceMAC in btcon and locked == True:
        os.popen('cinnamon-screensaver-command -d')
        locked = False



    
    



