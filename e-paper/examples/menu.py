#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from gpiozero import Button
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


a = 10
b = 20
c = 50
d = 50

old = [5, 5, 84, 50]
new = [50, 50, 184, 100]

def btn():
    global a, b, c, d, text, time_draw
    a = 50
    b = 60
    c = 70
    d = 90
    print("ttt")
    text = "new text"
    time_draw.rectangle((5, 5, 84, 50))


button = Button(16)
text = "test"




button.when_pressed = btn

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
    

    
    # # partial update
    logging.info("4.show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    bmp = Image.open(os.path.join(picdir, 'cat1.bmp'))
    bmp1 = Image.open(os.path.join(picdir, 'cat2.bmp'))
    bmp2 = Image.open(os.path.join(picdir, 'cat3.bmp'))
    bmp3 = Image.open(os.path.join(picdir, 'cat4.bmp'))
    time_image.paste(bmp, (5,5)) 
    time_image.paste(bmp1, (84,5)) 
    time_image.paste(bmp2, (0,64)) 
    time_image.paste(bmp3, (84,64))
    
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    num = 0
    while (True):
        time_draw.rectangle([(0,0),(50,50)],outline = 0)
        #time_draw.rectangle((5, 5, 84, 50))
        epd.displayPartial(epd.getbuffer(time_image))
        button.wait_for_press()
        time.sleep(0.5)
        num = num + 1
        if(num == 10):
            break
    
    logging.info("Clear...")
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

