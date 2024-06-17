#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import gpiozero
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image, ImageDraw, ImageFont
from signal import pause


# GPIO button initialization
btn_links = gpiozero.Button(19)
btn_rechts = gpiozero.Button(20)
btn_oben = gpiozero.Button(16)
btn_unten = gpiozero.Button(26)
btn_a = gpiozero.Button(6)
btn_b = gpiozero.Button(12)


# Main menu program
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)


def loadscreen():
    global image
    load_bmp = Image.open(os.path.join(picdir, 'kona.bmp'))
    load_bmp = load_bmp.resize((epd.height, epd.width), Image.ANTIALIAS)
    image.paste(load_bmp)
    image = image.transpose(Image.ROTATE_180)  # Rotate the image
    epd.displayPartBaseImage(epd.getbuffer(image))
    time.sleep(2)


def imagesetup():
    global draw, image
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)


def move():
    global draw, image
    print('move')
    draw.rectangle([(10, 20), (50, 50)], fill=255)
    draw.rectangle([(10, 20), (50, 50)], fill=0)
    image = image.transpose(Image.ROTATE_180)  # Rotate the image
    epd.displayPartial(epd.getbuffer(image))


def menu():
    print()
    global draw, image
    floor = Image.open(os.path.join(picdir, 'background.bmp'))
    image.paste(floor, (0, 0))


def healthbar(num):
    heart = Image.open(os.path.join(picdir, 'heart.bmp'))
    x = 5
    for i in range(num):
        image.paste(heart, (num * x, 12))


try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    loadscreen()

    imagesetup()
    # draw.rectangle([(20, 20), (50, 50)], fill=0)

    menu()

    healthbar(5)
    # draw.text((12, 8), 'Health', font=font15, fill=0)

    # kona = Image.open(os.path.join(picdir, 'heart.bmp'))
    # image.paste(kona, (4, 8))

    image = image.transpose(Image.ROTATE_180)  # Rotate the image
    # epd.display_fast(epd.getbuffer(image))
    # epd.displayPartial(epd.getbuffer(image))
    epd.displayPartBaseImage(epd.getbuffer(image))


    #pause()

    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
