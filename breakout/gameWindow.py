from gpiozero import Button
from PIL import Image, ImageDraw
from waveshare_epd import epd2in13_V4
import logging
import time
from signal import pause
from paddle import Paddle
from ball import Ball

class GameWindow:

    game_paused = True

    paddle = Paddle()
    ball = Ball()
    
    def startPause(self):
        global game_paused, epd
        if game_paused:
            epd.sleep()
            game_paused = False
        else:
            game_paused = True

    try:
        epd = epd2in13_V4.EPD()
        epd.init()
        epd.Clear(0xFF)

    except IOError as e:
        logging.info(e)   