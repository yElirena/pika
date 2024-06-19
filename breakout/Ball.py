from PIL import Image, ImageDraw
from waveshare_epd import epd2in13_V4

movement = 10

class Ball:
    def __init__(self, epd):
        self.epd = epd
        self.size = [(40, 45), (45, 50)]
        self.moveX = movement
        self.moveY = movement
    
    def initiateBall(self, draw):
        draw.ellipse(self.size, fill=0)
    
    def clearBall(self, draw):
        draw.ellipse(self.size, fill=1)
    
    def move(self, draw):
        self.clearBall(draw)

        newSize = [(self.size[0][0] + self.moveX, self.size[0][1] + self.moveY),
                    (self.size[1][0] + self.moveX, self.size[1][1] + self.moveY)]
        self.size = newSize
        self.initiateBall(draw)
    
    def checkCollisionWithWalls(self):
        #hopefully detects collision left and right walls
        if self.size[0][0] < -self.epd.width or self.size[0][0] > self.epd.width:
            self.moveX *= -1
            return
        #hopefully detects collision upper wall
        if self.size[0][1] > self.epd.height:
            self.moveY *= -1
            return
        #hopefully detects collosion with bottom wall
        if self.size[0][1] < -self.epd.height:
            self.reset()
            return
    
    def reset(self):
        self.size = [(40, 45), (45, 50)]
        self.moveX = movement
        self.moveY = movement