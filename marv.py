#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import gpiozero
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image, ImageDraw, ImageFont
from signal import pause


# gpio button
btn_links = gpiozero.Button(19)
btn_rechts = gpiozero.Button(20)
btn_oben = gpiozero.Button(16)
btn_unten = gpiozero.Button(26)
btn_a = gpiozero.Button(6)
btn_b = gpiozero.Button(12)


# Main Menü Programm
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

# setup font
font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)


# display setup
try:
    epd = epd2in13_V4.EPD()
    epd.init_fast()
    epd.Clear(0xFF)
    #image setup
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    # rotate screen
    image = image.transpose(Image.ROTATE_180)
    # rotated_image = image.rotate(180, expand=True)  # rotate


    #draw.text((5, 5), 'rotated draw 5.5', font=font15, fill=0)
    load_bmp = Image.open(os.path.join(picdir, 'kona.bmp'))
    load_bmp  = load_bmp.resize((epd.height, epd.width), Image.ANTIALIAS)
    image.paste(load_bmp)
    image.show ()
    
    # darw image to screen
    epd.displayPartBaseImage(epd.getbuffer(image))
    epd.sleep()


except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
