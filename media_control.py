#!/usr/bin/env python3
#coding: utf-8
import sys
import subprocess as sp
import time
import os
import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
from tkinter import *






if(len(sys.argv) > 1):
    if sys.argv[1] == "setmac":
       newMAC = str(input("Please enter the BT address of the new device you wish to use as your lock: ")) 
       fileReplacePart("btautolock.conf", newMAC, 1, 0)
       print("new lock MAC is " + newMAC)
       quit()



configFile = open('btautolock.conf', 'r')
configLines = configFile.readlines()
deviceMAC = configLines[0].strip()
lockDelay = int(configLines[1])
configFile.close()

bgColor = "gray50"
fgColor = "black"

devicePlayerPath = "/org/bluez/hci0/dev_" + deviceMAC.replace(":", "_") + "/player0"
deviceTransPath = "/org/bluez/hci0/dev_" + deviceMAC.replace(":", "_") + "/sep1"
bus = dbus.SystemBus()
obj = bus.get_object('org.bluez', "/")
mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
player_iface = dbus.Interface(bus.get_object('org.bluez', devicePlayerPath),'org.bluez.MediaPlayer1')
playerInitialized = False
def MediaControl(option, vol):
 
    if option == "play":
        player_iface.Play()
    elif option == "pause":
        player_iface.Pause()
    elif option == "n":
        player_iface.Next()
    elif option == "pr":
        player_iface.Previous()
    
class Window(Frame):
  
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.master = master
        # widget can take all window
        self.pack(fill=BOTH, expand=1)
      
        playButton = Button(self, text="▶", width=25, height=5, bg=bgColor, fg=fgColor, command = lambda: MediaControl("play", 0))
        pauseButton = Button(self, text="▋▋", width=25, height=5, bg=bgColor, fg=fgColor, command = lambda: MediaControl("pause", 0))
        nextButton = Button(self, text="▶▶", width=25, height=5, bg=bgColor, fg=fgColor,  command = lambda: MediaControl("n", 0))
        prevButton = Button(self, text="◀◀", width=25, height=5, bg=bgColor, fg=fgColor, command = lambda: MediaControl("pr", 0))
        playButton.pack()
        pauseButton.pack()
        nextButton.pack()
        prevButton.pack()
            

      



root = Tk()
window = Window(root)
root.wm_title("BlueTooth Media Controller")
root.mainloop()
