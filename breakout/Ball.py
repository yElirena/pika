import logging

movement = 10

class Ball:
    def __init__(self, epd):
        self.epd = epd
        self.size = [(40, 45), (45, 50)]
        self.moveX = movement
        self.moveY = movement
        self.life = 1
    
    def initiateBall(self, draw):
        draw.ellipse(self.size, fill=0)
    
    def clearBall(self, draw):
        draw.ellipse(self.size, fill=1)
    
    def move(self, draw):
        self.checkCollisionWithWalls()
        self.clearBall(draw)

        newSize = [(self.size[0][0] - self.moveX, self.size[0][1] - self.moveY),
                    (self.size[1][0] - self.moveX, self.size[1][1] - self.moveY)] 
        self.size = newSize
        self.initiateBall(draw)
        #logging.info(f"Ball coordinates: Top-Left ({self.size[0][0]}, {self.size[0][1]}), Bottom-Right ({self.size[1][0]}, {self.size[1][1]})")
    
    def checkCollisionWithWalls(self):
        #hopefully detects collision left and right walls
        if self.size[0][0] < 0 or self.size[1][0] > 250:
            self.moveX *= -1
            return
        #hopefully detects collision upper wall
        if self.size[0][1] > 110:
            self.moveY *= -1
            return
        #hopefully detects collosion with bottom wall
        if self.size[1][1] < 0:
            self.reset()
            return
    
    def reset(self):
        if self.life > 0:
            self.size = [(40, 45), (45, 50)]
            self.moveX = movement
            self.moveY = movement
            self.life = self.life - 1