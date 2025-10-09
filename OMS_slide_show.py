#!/usr/bin/env python

from glhelper import GlHelper
import mqtthelper

import os
import time
import datetime
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
logger.info("reading config settings")
config = configparser.ConfigParser()
config.read("settings.ini")

# global settings
settings = config["settings"]
enable_blanking = settings.getboolean("enable-blanking", True)
logger.info(f"enable_blanking = {enable_blanking}")
slide_time = settings.getint("slide-time", 10)
logger.info(f"slide_time = {slide_time}")
transition_time = settings.getfloat("transition-time", 2)
logger.info(f"transition_time = {transition_time}")
start_hour = settings.getint("start-hour", 8)
if start_hour < 0 or start_hour > 23:
    raise Exception("start hour must be in the range 0 to 23")
logger.info(f"start_hour = {start_hour}")
end_hour = settings.getint("end-hour", 22)
if end_hour < 0 or end_hour > 23:
    raise Exception("end hour must be in the range 0 to 23")
logger.info(f"end_hour = {end_hour}")
enable_reboot = settings.getboolean("enable-reboot", True)
logger.info(f"enable_reboot = {enable_reboot}")
handle_bank_holidays = settings.getboolean("handle-bank-holidays", True)
logger.info(f"handle_bank_holidays = {handle_bank_holidays}")
oms_images_folder = settings.get("oms-images-folder", "")
logger.info(f"oms_images_folder = {oms_images_folder}")
wms_images_folder = settings.get("wms-images-folder", "")
logger.info(f"wms_images_folder = {wms_images_folder}")

# MQTT settings
mqtt_settings = config["mqtt"]
enable_mqtt = mqtt_settings.getboolean("enable", False)
logger.info(f"enable_mqtt = {enable_mqtt}")
mqtt_host = mqtt_settings.get("host", "localhost")
logger.info(f"mqtt_host = {mqtt_host}")


def day_time():
    hour = datetime.datetime.now().hour
    if start_hour < end_hour:
        return hour >= start_hour and hour < end_hour
    return hour >= start_hour or hour < end_hour


def night_time():
    return not day_time()


def reboot():
    logger.info("rebooting")
    os.system('sudo reboot')


def during_the_day(images: list[str], transitions: list[str]):
    if enable_blanking:
        logger.debug("enabling the screen")
        os.system("./screen-on.sh")
    if len(images) == 1:
        image = images[0]
        logger.debug(f"showing the only image: {image}")
        gl_helper.show_image(image)
        while day_time():
            time.sleep(10)
    else:
        image_index: int = 0
        trans_index: int = 0
        while day_time():
            from_image = images[image_index]
            image_index = (image_index + 1) % len(images)
            to_image = images[image_index]
            transition = transitions[trans_index]
            trans_index = (trans_index + 1) % len(transitions)
            gl_helper.transition_images(from_image, to_image, transition, transition_time)
            time.sleep(slide_time)


def during_the_night(night_slide):
    mqtt_helper.off()
    if enable_blanking:
        logger.debug("disabling the screen")
        os.system("./screen-off.sh")
    gl_helper.show_image(night_slide)
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


def today_slides() -> list[str]:
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
        mqtt_helper.theme('wms')
    else:
        logger.info("using the Otley Maker Space images")
        images_folder = oms_images_folder
        mqtt_helper.theme('oms')
    logger.info(f"images_folder = {images_folder}")
    img_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')
    slide_filenames = [f for f in os.listdir(images_folder) if f.lower().endswith(img_exts)]
    logger.info(f"loaded {len(slide_filenames)} slides")
    slide_pathnames = [os.path.join(images_folder, f) for f in sorted(slide_filenames)]
    return slide_pathnames


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


def get_transitions(folder: str) -> list[str]:
    files = [f for f in os.listdir(folder) if f.lower().endswith('.glsl')]
    if len(files) == 0:
        raise ValueError(f"no fragment .glsl transitions found in folder: {folder}")
    return [os.path.join(folder, f) for f in sorted(files)]


#### main programme ####
mqtt_helper = mqtthelper.get(enable_mqtt, mqtt_host)
black_image = 'slide_black.png'
while True:
    if handle_bank_holidays:
        download_bank_holidays()

    # get list of images for today
    slides = today_slides()

    # setup GL helper for displaying images / transitions
    preload_images = list(slides)
    preload_images.append(black_image)
    gl_helper = GlHelper(preload_images)

    # get list of transitions
    transitions = get_transitions("transitions")

    # show the slides during the day
    during_the_day(slides, transitions)

    # show a black screen during the night
    during_the_night(black_image)

    # reboot at the end of the night
    if enable_reboot:
        reboot()
