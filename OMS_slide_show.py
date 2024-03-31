#!/usr/bin/env python

import os
import time
import datetime
from tkinter import *
import configparser
import logging
import logging.config
import json
import requests

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
handle_bank_holidays = settings.getboolean("handle-bank-holidays", True)
logger.debug(f"handle_bank_holidays = {handle_bank_holidays}")
oms_images_folder = settings["oms-images-folder"]
logger.debug(f"oms_images_folder = {oms_images_folder}")
wms_images_folder = settings.get("wms-images-folder")
logger.debug(f"wms_images_folder = {wms_images_folder}")


def day_time():
    hour = datetime.datetime.now().hour
    if start_hour < end_hour:
        return hour >= start_hour and hour < end_hour
    return hour >= start_hour or hour < end_hour


def night_time():
    return not day_time()


def show_slide(slide):
    label.config(image=slide)
    root.update_idletasks()
    root.update()


def blank_display():
    if enable_blanking:
        logger.debug("disabling the screen")
        os.system("./screen-off.sh")


def reboot():
    logger.info("rebooting")
    os.system('sudo reboot')


def during_the_day(slides):
    while day_time():
        for slide in slides:
            if day_time():
                show_slide(slide)
                time.sleep(slide_time)


def during_the_night(slide):
    show_slide(slide)
    while night_time():
        time.sleep(10)


def is_bank_holiday():
    with open("bank-holidays.json") as file:
        data = json.load(file)
    bank_holidays = data["england-and-wales"]["events"]
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    for holiday in bank_holidays:
        if holiday["date"] == today:
            title = holiday["title"]
            logger.debug(f"today is a bank holiday: {title}")
            return True
    logger.debug("today is not a bank holiday")
    return False


def today_slides():
    is_monday = datetime.datetime.today().weekday() == 0
    is_wms_day = False
    if is_monday:
        is_wms_day = True
        logger.debug("today is Monday")
        if handle_bank_holidays:
            logger.debug("checking bank holidays")
            if is_bank_holiday():
                is_wms_day = False
        else:
            logger.debug("ignoring bank holidays")
    else:
        logger.debug("today is not Monday")
    if is_wms_day:
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


def download_bank_holidays():
    logger.info("downloading bank holidays")
    try:
        response = requests.get("https://www.gov.uk/bank-holidays.json")
    except:
        logger.exception("failed to download bank holidays")
        return
    logger.info(f"response code: {response.status_code}")
    if response.status_code == 200:
        logger.info("writing bank holidays to file")
        with open("bank-holidays.json", "w") as file:
            file.write(response.text)
            file.close()


# create the application window and makes it full screen
root = Tk()
root.attributes('-fullscreen', True)

# create a frame
frame = Frame(root)
frame.pack(fill=BOTH, expand=1)

# create a label for slides to be in
label = Label(frame)
label.pack()

#### main programme ####
if handle_bank_holidays:
    download_bank_holidays()
slides = today_slides()
black_slide = PhotoImage(file='slide_black.png')
# show the slides during the day
during_the_day(slides)
# blank screen at the end of the day
blank_display()
# show a black screen during the night
during_the_night(black_slide)
# reboot at the end of the night
reboot()
