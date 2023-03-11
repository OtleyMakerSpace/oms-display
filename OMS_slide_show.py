#!/usr/bin/env python

import os
import time
import datetime
from tkinter import *
import configparser
import logging
import logging.config

# setup logging
logging.config.fileConfig("logging.ini")
logger = logging.getLogger()
logger.info("starting up")

# read settings from config file
logger.info("reading config settngs")
config = configparser.ConfigParser()
config.read("settings.ini")
settings = config["settings"]
enable_blanking = settings.getboolean("enable-blanking", True)
logger.debug(f"enable_blanking = {enable_blanking}")
slide_time = settings.getint("slide-time", 10)
logger.debug(f"slide_time = {slide_time}")
start_hour = settings.getint("start-hour", 8)
if start_hour < 0 or start_hour > 23:
    raise Exception("start hour must be in the range 0 to 23")
logger.debug(f"start_hour = {start_hour}")
end_hour = settings.getint("end-hour", 22)
if end_hour < 0 or end_hour > 23:
    raise Exception("end hour must be in the range 0 to 23")
logger.debug(f"end_hour = {end_hour}")
oms_images_folder = settings["oms-images-folder"]
logger.debug(f"oms_images_folder = {oms_images_folder}")
wms_images_folder = settings.get("wms-images-folder")
logger.debug(f"wms_images_folder = {wms_images_folder}")


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
    label.config(image=slide)
    root.update_idletasks()
    root.update()


def blank_display():
    if enable_blanking:
        global blanked
        if not blanked:
            # todo: blank the display
            blanked = True


def show_display():
    if enable_blanking:
        global blanked
        if blanked:
            # todo: show the display
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


def during_the_night(slide):
    show_slide(slide)
    while night_time():
        blank_display()
        if midnight():
            reboot()
        time.sleep(1)


def today_slides():
    is_monday = datetime.datetime.now().weekday() == 0
    if is_monday:
        # todo: check if it's a bank holiday
        logger.info("using the Wharfedale Men's Shed images")
        images_folder = wms_images_folder
    else:
        logger.info("using the Otley Maker Space images")
        images_folder = oms_images_folder
    logger.info(f"images_folder = {images_folder}")
    slide_filenames = os.listdir(images_folder)
    slide_filenames.sort()
    slides = [PhotoImage(file=os.path.join(images_folder, f))
              for f in slide_filenames]
    logger.info(f"loaded {len(slides)} slides")
    return slides


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
slides = today_slides()

# load the black slide
black_slide = PhotoImage(file='slide_black.png')

#### main programme ####
while True:
    during_the_day(slides)
    during_the_night(black_slide)
