#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from gpiozero import Button
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image, ImageDraw, ImageFont
from signal import pause

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


def obenlinks():
    global draw1, final_image
    print("o")

    draw1.rectangle([(231, 89), (134, 57)], outline=0, width=3)
    draw1.rectangle([(115, 89), (19, 57)], outline=255, width=3)
    draw1.rectangle([(231, 40), (134, 8)], outline=255, width=3)
    draw1.rectangle([(115, 40), (19, 8)], outline=255, width=3)

    epd.displayPartial(epd.getbuffer(final_image))


def obenrechts():
    global draw1, final_image
    print("r")
    draw1.rectangle([(231, 89), (134, 57)], outline=255, width=3)
    draw1.rectangle([(115, 89), (19, 57)], outline=0, width=3)
    draw1.rectangle([(231, 40), (134, 8)], outline=255, width=3)
    draw1.rectangle([(115, 40), (19, 8)], outline=255, width=3)

    epd.displayPartial(epd.getbuffer(final_image))


def untenlinks():
    global draw1, final_image
    print("u")
    draw1.rectangle([(231, 89), (134, 57)], outline=255, width=3)
    draw1.rectangle([(115, 89), (19, 57)], outline=255, width=3)
    draw1.rectangle([(231, 40), (134, 8)], outline=0, width=3)
    draw1.rectangle([(115, 40), (19, 8)], outline=255, width=3)
    epd.displayPartial(epd.getbuffer(final_image))


def untenrechts():
    global draw1, final_image
    print("l")
    draw1.rectangle([(231, 89), (134, 57)], outline=255, width=3)
    draw1.rectangle([(115, 89), (19, 57)], outline=255, width=3)
    draw1.rectangle([(231, 40), (134, 8)], outline=255, width=3)
    draw1.rectangle([(115, 40), (19, 8)], outline=0, width=3)
    epd.displayPartial(epd.getbuffer(final_image))


# gpio button
btn_links = Button(19)
btn_rechts = Button(20)
btn_oben = Button(16)
btn_unten = Button(26)
btn_a = Button(6)
btn_b = Button(12)

btn_links.when_pressed = untenlinks
btn_rechts.when_pressed = obenrechts
btn_oben.when_pressed = obenlinks
btn_unten.when_pressed = untenrechts

font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)

try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    image = Image.new('1', (epd.height, epd.width), 255)

    draw = ImageDraw.Draw(image)

    bmp = Image.open(os.path.join(picdir, 'cat1.bmp'))
    bmp1 = Image.open(os.path.join(picdir, 'cat2.bmp'))
    bmp2 = Image.open(os.path.join(picdir, 'cat3.bmp'))
    bmp3 = Image.open(os.path.join(picdir, 'cat4.bmp'))

    draw.text((115, 8), 'Pika', font = font15, fill = 0)

    image.paste(bmp, (19, 27))
    image.paste(bmp1, (135, 27))
    image.paste(bmp2, (19, 75))
    image.paste(bmp3, (135, 75))

    rotated_image = image.rotate(180, expand=True)  # rotate

    epd.displayPartBaseImage(epd.getbuffer(rotated_image))

    original_width, original_height = image.size
    rotated_width, rotated_height = rotated_image.size

    offset_x = (rotated_width - original_width) // 2
    offset_y = (rotated_height - original_height) // 2

    final_image = Image.new('1', (rotated_width, rotated_height), 255)

    # final_image = final_image.rotate(180)
    final_image.paste(rotated_image)
    draw1 = ImageDraw.Draw(final_image)

    # while (True):
    #     draw1.rectangle((29, 100, 8, 20), fill = 255)
    #     draw1.text((29, 100), time.strftime('%H:%M:%S'), font = font15, fill = 0)
    #     epd.displayPartial(epd.getbuffer(final_image))
    pause()
    epd.sleep()


except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
