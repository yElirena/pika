from gpiozero import Button
from PIL import Image, ImageDraw
import logging
import time
from waveshare_epd import epd2in13_V4
from signal import pause

logging.basicConfig(level=logging.DEBUG)


class Paddle:

    def __init__(self, epd):
        self.epd = epd
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


    def initialPaddle(self, draw):
        draw.rectangle([(self.x_0, self.y_0), (self.x_1, self.y_1)], fill=0, width=1)

    """ def updateDisplay(self):
        self.epd.Clear(0xFF)
        self.paddle = Image.new('1', (self.epd.height, self.epd.width), 1)
        self.drawPaddle = ImageDraw.Draw(self.paddle)
        self.drawPaddle.rectangle([(self.x_0, self.y_0), (self.x_1, self.y_1)], fill=0, width=1)
        self.epd.displayPartial(self.epd.getbuffer(self.paddle)) """

    def moveLeft(self):
        if self.x_1 < 198:
            self.x_0 = self.x_0 + 10
            self.x_1 = self.x_1 + 10
            self.updateDisplay()

    def moveRight(self):
        if self.x_0 > 0:
            self.x_0 = self.x_0 - 10
            self.x_1 = self.x_1 - 10
            self.updateDisplay()

    def goBack(self):
        pass