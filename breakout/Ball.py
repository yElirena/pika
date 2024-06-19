from PIL import Image, ImageDraw
from waveshare_epd import epd2in13_V4


class Ball:
    def __init__(self, epd):
        self.epd = epd
        self.size = [(40, 45), (45, 50)]
    
    def initiateBall(self, draw):
        draw.ellipse(self.size, fill=0)
    
    def clearBall(self, draw):
        draw.ellipse(self.size, fill=1)
    
    def move(self, draw):
        self.clearBall(draw)

        newSize = [(self.size[0][0] - 10, self.size[0][1] - 10),
                    (self.size[1][0] - 10, self.size[1][1] - 10)]
        self.size = newSize
        self.initiateBall(draw)