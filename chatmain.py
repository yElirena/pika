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
    global menu, menu_screen
    print("o")
    menu_screen = menu_screen.rotate(180)
    menu.rectangle([(86, 44), (0, 0)], outline=0)
    menu.rectangle([(20, 60), (0, 50)], outline=255)
    menu.rectangle([(80, 80), (50, 0)], outline=255)
    menu.rectangle([(80, 80), (50, 50)], outline=255)
    menu_screen = menu_screen.rotate(180)
    time.sleep(0.5)
    epd.displayPartial(epd.getbuffer(menu_screen))
 
def obenrechts():
    global menu, menu_screen
    print("r")
    menu_screen = menu_screen.rotate(180)
    menu.rectangle([(50, 50), (0, 0)], outline=255)
    menu.rectangle([(20, 60), (0, 50)], outline=0)
    menu.rectangle([(80, 80), (50, 0)], outline=255)
    menu.rectangle([(80, 80), (50, 50)], outline=255)
    menu_screen = menu_screen.rotate(180)
    time.sleep(0.5)

    epd.displayPartial(epd.getbuffer(menu_screen))
 
def untenlinks():
    global menu, menu_screen
    print("u")
    menu_screen = menu_screen.rotate(180)
    menu.rectangle([(50, 50), (0, 0)], outline=255)
    menu.rectangle([(20, 60), (0, 50)], outline=255)
    menu.rectangle([(80, 80), (50, 0)], outline=0)
    menu.rectangle([(80, 80), (50, 50)], outline=255)
    menu_screen = menu_screen.rotate(180)
    time.sleep(0.5)
    epd.displayPartial(epd.getbuffer(menu_screen))
 
def untenrechts():
    global menu, menu_screen
    print("l")
    menu_screen = menu_screen.rotate(180)
    menu.rectangle([(86, 44), (2, 2)], outline=255)
    menu.rectangle([(20, 60), (0, 50)], outline=255)
    menu.rectangle([(80, 80), (50, 0)], outline=255)
    menu.rectangle([(80, 80), (50, 50)], outline=0)
    menu_screen = menu_screen.rotate(180)
    time.sleep(0.5)
    epd.displayPartial(epd.getbuffer(menu_screen))
 
links = Button(19)
rechts = Button(20)
oben = Button(16)
unten = Button(26)
 
links.when_pressed = untenlinks
rechts.when_pressed = untenrechts
oben.when_pressed = obenrechts
unten.when_pressed = obenlinks
 
try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)
 
    menu_screen = Image.new('1', (epd.height, epd.width), 255)
    #menu = ImageDraw.Draw(menu_screen)
 
    bmp = Image.open(os.path.join(picdir, 'cat1.bmp'))
    bmp1 = Image.open(os.path.join(picdir, 'cat2.bmp'))
    bmp2 = Image.open(os.path.join(picdir, 'cat3.bmp'))
    bmp3 = Image.open(os.path.join(picdir, 'cat4.bmp'))
    menu_screen.paste(bmp, (20, 5))
    menu_screen.paste(bmp1, (140, 5))
    menu_screen.paste(bmp2, (20, 64))
    menu_screen.paste(bmp3, (140, 64))
 
    # Drehe das Bild um 180 Grad
    menu_screen = menu_screen.rotate(180)
    menu_screen.show()
    epd.displayPartBaseImage(epd.getbuffer(menu_screen))
 
    num = 0
    while True:
        pause()
        print("wait")
 
        time.sleep(0.5)
        num += 1
        if num == 4:
            break
 
    epd.sleep()
 
except IOError as e:
    logging.info(e)
 
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()