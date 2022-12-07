#!/usr/bin/env python

##### OMS Slide Show System ####

##### imports and variables ####

import os
import time
import datetime
from tkinter import *
import requests
import json
from oauth2client.service_account import ServiceAccountCredentials

on_hours = ['08','09','10','11','12','13','14','15','16','17','18','19','20','21']
slides = []
slide_time = 10

##### function definitions ####

def during_the_day():
    # loop that runs forever
    while True:
        # gets the current hour of the time
        the_hour = datetime.datetime.now().strftime('%H')
        # checks if current hour is an hour the display is on
        if the_hour in on_hours:
            # loops through slide list and puts each image on screen
            for slide in slides:
                # changes the slide image in the label 
                label.config(image=slide)
                # updates tkinter 
                root.update_idletasks()
                root.update()
                # pauses before next slide 
                time.sleep(slide_time)
        # the current hour is when display is off
        else:
            # swaps to night time display
            during_the_night()

def during_the_night():
    # defines a variable to track changes to black slide
    showing_black_slide = False
    # loop that runs forever
    while True:
        # gets the current hour and minute of the time
        the_hour = datetime.datetime.now().strftime('%H')
        the_min = datetime.datetime.now().strftime('%M')
        # checks if it is midnight
        if the_hour == '00' and the_min == '00':
            # reboots the computer
            time.sleep(60)
            os.system('sudo reboot')
        # checks if current hour is an hour the display is on
        if the_hour in on_hours:
            # swaps to daytime display
            during_the_day()
        # checks if the slide is not black yet
        if not showing_black_slide:
            # changes the slide image in the label to all black
            label.config(image=slide_black)
            # updates tkinter 
            root.update_idletasks()
            root.update()
            # changes state of the tracker variable
            showing_black_slide = True
        # pauses before next slide 
        time.sleep(50)

#### tkinter setup ####

# creates the application window and makes it full screen
root = Tk()
root.attributes('-fullscreen', True)

# sets up escape key to quit the program
root.bind("<Escape>", lambda event: root.destroy())

# creates a frame
frame = Frame(root)
frame.pack(fill=BOTH, expand=1)

# creates a label for slides to be in
label = Label(frame)
label.pack()

# loads the slide images
slides.append(PhotoImage(file = 'slide_1.png'))
slides.append(PhotoImage(file = 'slide_2.png'))
slides.append(PhotoImage(file = 'slide_3.png'))
slides.append(PhotoImage(file = 'slide_4.png'))
slides.append(PhotoImage(file = 'slide_5.png'))

# loads the black slide
slide_black = PhotoImage(file = 'slide_black.png')

#### main programme ####

during_the_night()
