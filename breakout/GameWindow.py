from gpiozero import Button
from PIL import Image, ImageDraw
import logging
import time
from waveshare_epd import epd2in13_V4
from signal import pause
from paddle import Paddle
from Ball import Ball

class GameWindow:
    def __init__(self):
        self.epd = epd2in13_V4.EPD()
        self.epd.Clear(0xFF)

        self.paddle = Paddle()
        self.ball = Ball()

        self.updateDisplay1()
    
    def updateDisplay1(self):
        image = Image.new('1', (self.epd.height, self.epd.width), 1)
        draw = ImageDraw.Draw(image)

        self.paddle(draw)
        self.ball(draw)

        self.epd.displayPartBaseImage(self.epd.getbuffer(image))
        
        time.sleep(0.5)
        self.updateDisplay1()

if __name__ == "__main__":

    try:
        game = GameWindow()
        pause()
    except IOError as e:
        logging.error("IOError: %s", e)
    except Exception as ex:
        logging.error("Unexpected error: %s", ex)