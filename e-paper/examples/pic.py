#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging 
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V4 Demo")
    
    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
    epd.init()


	# read bmp file 
    logging.info("2.read bmp file...")
    image = Image.open(os.path.join(picdir, 'oca.bmp'))
    width, height = epd.height, epd.width

    # read bmp file on window
    logging.info("3.read bmp file on window...")
    image = image.resize((width, int(image.height * width / image.width)), Image.ANTIALIAS) 
    epd.display(epd.getbuffer(image))
    time.sleep(20)


# Resize the image to fit the display width
width, height = epd.height, epd.width
image = image.resize((width, int(image.height * width / image.width)), Image.ANTIALIAS)

def display_image(image):
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    epd.sleep()

def scroll_image(image, step=10, delay=0.5):
    width, height = epd.height, epd.width
    img_width, img_height = image.size

    for y in range(0, img_height - height + 1, step):
        cropped_image = image.crop((0, y, width, y + height))
        display_image(cropped_image)
        time.sleep(delay)

    # Scroll back to the top
    for y in range(img_height - height, -1, -step):
        cropped_image = image.crop((0, y, width, y + height))
        display_image(cropped_image)
        time.sleep(delay)



scroll_image(image)

       

    
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
