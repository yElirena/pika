from PIL import Image, ImageDraw
from waveshare_epd import epd2in13_V4

class Ball:
    def __init__(self, epd):
        self.epd = epd
        self.upperX = 50
        self.upperY = 60
        self.lowerX = 80
        self.lowerY = 85
    
    def initiateBall(self, draw):
        draw.ellipse([(self.upperX, self.upperY), (self.lowerX, self.lowerY)], fill=0)