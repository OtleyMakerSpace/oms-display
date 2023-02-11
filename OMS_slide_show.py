#!/usr/bin/env python

import os
import time
import datetime
from tkinter import *
import configparser
import logging
import logging.config

# setup logging
logging.config.fileConfig("logging.conf")
logger = logging.getLogger()
logger.info("starting up")

# read settings from config file
logging.info("reading config settngs")
config = configparser.ConfigParser()
config.read("settings.ini")
settings = config["settings"]
enable_blanking = settings.getboolean("enable-blanking", True)
logging.debug(f"enable_blanking = {enable_blanking}")
slide_time = settings.getint("slide-time", 10)
logging.debug(f"slide_time = {slide_time}")
start_hour = settings.getint("start-hour", 8)
if start_hour < 0 or start_hour > 23:
    raise Exception("start hour must be in the range 0 to 23")
logging.debug(f"start_hour = {start_hour}")
end_hour = settings.getint("end-hour", 22)
if end_hour < 0 or end_hour > 23:
    raise Exception("end hour must be in the range 0 to 23")
logging.debug(f"end_hour = {end_hour}")
images_folder = settings.get("images-folder")
logging.debug(f"images_folder = {images_folder}")


# globals
blanked = False


def day_time():
    hour = datetime.datetime.now().hour
    if start_hour < end_hour:
        return hour >= start_hour and hour < end_hour
    return hour >= start_hour or hour < end_hour


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


def blank_display():
    if enable_blanking:
        global blanked
        if not blanked:
            # blank the display
            blanked = True


def show_display():
    if enable_blanking:
        global blanked
        if blanked:
            # show the display
            blanked = False


def reboot():
    logger.info("rebooting soon")
    time.sleep(60)
    logger.info("rebooting")
    os.system('sudo reboot')


def during_the_day(slides):
    while day_time():
        for slide in slides:
            if day_time():
                show_display()
                show_slide(slide)
                time.sleep(slide_time)


def during_the_night():
    show_slide(slide_black)
    while night_time():
        blank_display()
        if midnight():
            reboot()
        time.sleep(10)

#### tkinter setup ####


# create the application window and makes it full screen
root = Tk()
root.attributes('-fullscreen', True)

# setup escape key to quit the program
root.bind("<Escape>", lambda event: root.destroy())

# create a frame
frame = Frame(root)
frame.pack(fill=BOTH, expand=1)

# create a label for slides to be in
label = Label(frame)
label.pack()

# load the slide images
slide_filenames = os.listdir(images_folder)
slide_filenames.sort()
slides = [PhotoImage(file=os.path.join(images_folder, f))
          for f in slide_filenames]
logging.info(f"loaded {len(slides)} slides")


# load the black slide
slide_black = PhotoImage(file='slide_black.png')

#### main programme ####
while True:
    during_the_day(slides)
    during_the_night()
