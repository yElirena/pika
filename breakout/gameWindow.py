from gpiozero import Button
from PIL import Image, ImageDraw
from waveshare_epd import epd2in13_V4
import logging
import time
from signal import pause

class gameWindow:

    try:
        epd = epd2in13_V4.EPD()
        epd.init()
        epd.Clear(0xFF)

    except IOError as e:
        logging.info(e)   