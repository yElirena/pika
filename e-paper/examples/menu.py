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
    
    
    # read bmp file 
    
    # read bmp file on window
    epd.Clear(0xFF)
    image1 = Image.new('1', (epd.height, epd.width), 122)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, 'cat1.bmp'))
    bmp1 = Image.open(os.path.join(picdir, 'cat2.bmp'))
    bmp2 = Image.open(os.path.join(picdir, 'cat3.bmp'))
    bmp3 = Image.open(os.path.join(picdir, 'cat4.bmp'))
    #bmp = bmp.resize((122, 250), Image.ANTIALIAS)
    
    image1.paste(bmp, (0, 0))
    image1.paste(bmp1, (0, 50))
    image1.paste(bmp2, (96, 0))
    image1.paste(bmp3, (96, 50))
    epd.display_fast(epd.getbuffer(image1))
    time.sleep(15)

    
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
