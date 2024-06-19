from gpiozero import Button
from PIL import Image, ImageDraw
from waveshare_epd import epd2in13_V4

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



    def initiatePaddle(self, draw):
        draw.rectangle([(self.x_0, self.y_0), (self.x_1, self.y_1)], fill=0, width=1)

    def moveLeft(self):
        if self.x_1 < 198:
            self.x_0 = self.x_0 + 10
            self.x_1 = self.x_1 + 10

    def moveRight(self):
        if self.x_0 > 0:
            self.x_0 = self.x_0 - 10
            self.x_1 = self.x_1 - 10

    def goBack(self):
        pass