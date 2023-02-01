#!/usr/bin/env python

##### OMS Slide Show System ####

##### imports and variables ####

import os
import time
import datetime
from tkinter import *

on_hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
slide_time = 10

##### function definitions ####


def day_time():
    hour = datetime.datetime.now().hour
    return hour in on_hours


def night_time():
    return not day_time()


def midnight():
    hour = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    return hour == 0 and min == 0


def show_slide(slide):
    # changes the slide image in the label
    label.config(image=slide)
    # updates tkinter
    root.update_idletasks()
    root.update()


def during_the_day(slides):
    while day_time():
        for slide in slides:
            if day_time():
                show_slide(slide)
                time.sleep(slide_time)


def reboot():
    time.sleep(60)
    os.system('sudo reboot')


def during_the_night():

    blanked = False
    show_slide(slide_black)

    while night_time():
        if midnight():
            reboot()
        if not blanked:
            # blank the display
            blanked = True
        time.sleep(10)

    # unblank the display

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
slides = []
slides.append(PhotoImage(file='slide_1.png'))
slides.append(PhotoImage(file='slide_2.png'))
slides.append(PhotoImage(file='slide_3.png'))
slides.append(PhotoImage(file='slide_4.png'))
slides.append(PhotoImage(file='slide_5.png'))

# loads the black slide
slide_black = PhotoImage(file='slide_black.png')

#### main programme ####
while True:
    during_the_day(slides)
    during_the_night()
