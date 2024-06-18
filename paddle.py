from gpiozero import Button
from PIL import Image, ImageDraw
import logging
import time
from waveshare_epd import epd2in13_V4
from signal import pause

logging.basicConfig(level=logging.DEBUG)

class Paddle:

    def __init__(self):
        self.btn_links = Button(19)
        self.btn_rechts = Button(20)
        self.btn_a = Button(6)
        self.btn_b = Button(12)
        self.x_0 = 112
        self.x_1 = 140
        self.y_0 = 4
        self.y_1 = 8

        self.btn_links.when_pressed = self.moveLeft
        self.btn_rechts.when_pressed = self.moveRight
        self.btn_b.when_pressed = self.goBack

    def moveLeft(self):
        if self.btn_links.is_pressed:
            print("Left button is being pressed")
        else:
            print("Button was pushed once.")

    def moveRight(self):
        pass

    def goBack(self):
        pass

try:
    logging.info("Start of EPD init")
    epd = epd2in13_V4.EPD()
    epd.init()
    logging.info("EPD init successfull")
    epd.Clear(0xFF)
    paddle = Image.new('1', (epd.height, epd.width), 1)

    drawPaddle = ImageDraw.Draw(paddle)
    drawPaddle.rectangle([(112, 4), (140, 8)], fill=0, width=1)
    epd.displayPartBaseImage(epd.getbuffer(paddle))
    pause()
    logging.info("Display updated")

except IOError as e:
    logging.error("IOError: %s", e)
except Exception as ex:
    logging.error("Unexpected error: %s", ex)

