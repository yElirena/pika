#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


from gpiozero import Button
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image, ImageDraw
from signal import pause


def obenlinks():
    global draw1, final_image
    print("o")
    
    draw1.rectangle([(248, 120), (127, 63)], outline = 0, width=3)
    draw1.rectangle([(123, 120), (2, 59)], outline = 255, width=3)
    draw1.rectangle([(248, 59), (123, 2)], outline = 255, width=3)
    draw1.rectangle([(123, 59), (2, 2)], outline = 255, width=3)
    time.sleep(0.5)
    epd.displayPartial(epd.getbuffer(final_image))


def obenrechts():
    global draw1, final_image
    print("r")
    draw1.rectangle([(248, 120), (127, 63)], outline = 255, width=3)
    draw1.rectangle([(123, 120), (2, 59)], outline = 0, width=3)
    draw1.rectangle([(248, 59), (123, 2)], outline = 255, width=3)
    draw1.rectangle([(123, 59), (2, 2)], outline = 255, width=3)
    time.sleep(0.5)
    epd.displayPartial(epd.getbuffer(final_image))


def untenlinks():
    global draw1, final_image
    print("u")
    draw1.rectangle([(248, 120), (127, 63)], outline = 255, width=3)
    draw1.rectangle([(123, 120), (2, 59)], outline = 255, width=3)
    draw1.rectangle([(248, 59), (127, 2)], outline = 0, width=3)
    draw1.rectangle([(123, 59), (2, 2)], outline = 255, width=3)
    time.sleep(0.5)
    epd.displayPartial(epd.getbuffer(final_image))


def untenrechts():
    global draw1, final_image
    print("l")
    draw1.rectangle([(248, 120), (127, 63)], outline = 255, width=3)
    draw1.rectangle([(123, 120), (2, 59)], outline = 255, width=3)
    draw1.rectangle([(248, 59), (127, 2)], outline = 255, width=3)
    draw1.rectangle([(123, 59), (2, 2)], outline = 0, width=3)
    time.sleep(0.5)
    epd.displayPartial(epd.getbuffer(final_image))


#gpio button
btn_links = Button(19)
btn_rechts = Button(20)
btn_oben = Button(16)
btn_unten = Button(26)
btn_a = Button(6)
btn_b = Button(12)

btn_links.when_pressed = untenlinks
btn_rechts.when_pressed = untenrechts
btn_oben.when_pressed = obenrechts
btn_unten.when_pressed = obenlinks


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

    image.paste(bmp, (20, 5))
    image.paste(bmp1, (140, 5))
    image.paste(bmp2, (20, 64))
    image.paste(bmp3, (140, 64))

    rotated_image = image.rotate(180, expand=True)  # rotate

    epd.displayPartBaseImage(epd.getbuffer(rotated_image))

    original_width, original_height = image.size
    rotated_width, rotated_height = rotated_image.size

    offset_x = (rotated_width - original_width) // 2
    offset_y = (rotated_height - original_height) // 2

    final_image = Image.new('1', (rotated_width, rotated_height), 255)

    #final_image = final_image.rotate(180)
    final_image.paste(rotated_image)
    draw1 = ImageDraw.Draw(final_image)
    

    epd.displayPartial(epd.getbuffer(final_image))


    num = 0
    while (True):
        pause()
        print("wait")

        time.sleep(0.5)
        num = num + 1
        if (num == 4):
            break

    epd.sleep()


except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
