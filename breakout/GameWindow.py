from gpiozero import Button
from PIL import Image, ImageDraw
import logging
import time
from waveshare_epd import epd2in13_V4
from signal import pause
from Ball import Ball

logging.basicConfig(level=logging.DEBUG)

class GameWindow:
    def __init__(self):
        try:
            self.epd = epd2in13_V4.EPD()
            #logging.info("Start EDP init")
            self.epd.init()
            #logging.info("init successfull")
            self.epd.Clear(0xFF)

            self.btn_a = Button(6)
            self.btn_b = Button(12)

            self.btn_links = Button(19)
            self.btn_rechts = Button(20)

            self.paddleX0 = 112
            self.paddleX1 = 140
            self.paddleY0 = 4
            self.paddleY1 = 8


            self.ball = Ball(self.epd)

            self.running = False
            self.initiateDisplay()
        except IOError as e:
            logging.error("IOError: %s", e)
        except Exception as ex:
            logging.error("Unexpected error: %s", ex)

    def initiateDisplay(self):
        image = Image.new('1', (self.epd.height, self.epd.width),1)
        draw = ImageDraw.Draw(image)

        draw.text((25, 50), "Do you want to play? A: Yes B: No", fill=0)
        self.btn_a.when_pressed = self.startGame
        self.btn_b.when_pressed = self.pauseOrBackToMenu

        image = image.rotate(180)        
        self.epd.displayPartBaseImage(self.epd.getbuffer(image))
    
    def startGame(self):

        self.epd.Clear(0xFF)
        image = Image.new('1', (self.epd.height, self.epd.width), 1)
        draw = ImageDraw.Draw(image)
        draw.rectangle([(self.paddleX0, self.paddleY0), (self.paddleX1, self.paddleY1)], fill=0, width=1)               
        self.ball.move(draw)
        self.epd.displayPartBaseImage(self.epd.getbuffer(image))
        self.running = True
        self.updateDisplay()        

    def pauseOrBackToMenu(self):
        if self.running:
            self.running = False
            self.epd.sleep()
        else:
            pass

    def paddleMoveLeft(self):
        logging.info("Paddle L Button pressed")
        if self.paddleX1 < 250:
            self.paddleX0 = self.paddleX0 + 10
            self.paddleX1 = self.paddleX1 + 10
            logging.info(f"New coordinates {self.paddleX0}, {self.paddleX1}")

    def paddleMoveRight(self):
        logging.info("Paddle R Button pressed")
        if self.paddleX0 > 0:
            self.paddleX0 = self.paddleX0 - 10
            self.paddleX1 = self.paddleX1 - 10
            logging.info(f"New coordinates {self.paddleX0}, {self.paddleX1}")

    
    def updateDisplay(self):
        try:
            while self.running:
                self.btn_links.when_pressed =  self.paddleMoveLeft
                self.btn_rechts.when_pressed = self.paddleMoveRight
                image = Image.new('1', (self.epd.height, self.epd.width), 1)
                draw = ImageDraw.Draw(image)
                if self.ball.life: 
                    draw.rectangle([(self.paddleX0, self.paddleY0), (self.paddleX1, self.paddleY1)], fill=0, width=1)               
                    self.ball.move(draw)
                    self.epd.displayPartial(self.epd.getbuffer(image))
                    time.sleep(0.1)
                    #logging.info("Display updated")
                    
                else:
                    self.running = False
                    self.epd.Clear(0xFF)
                    draw.text((50, 50), "You died", fill=0)
                    image = image.rotate(180)
                    self.epd.displayPartBaseImage(self.epd.getbuffer(image))

        except IOError as e:
            logging.error("IOError: %s", e)
        except Exception as ex:
            logging.error("Unexpected error: %s", ex)

if __name__ == "__main__":

    try:
        game = GameWindow()
        pause()
    except IOError as e:
        logging.error("IOError: %s", e)
    except Exception as ex:
        logging.error("Unexpected error: %s", ex)