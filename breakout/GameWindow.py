from gpiozero import Button
from PIL import Image, ImageDraw
import logging
import time
from waveshare_epd import epd2in13_V4
from signal import pause
from paddle import Paddle
from Ball import Ball

#logging.basicConfig(level=logging.DEBUG)

class GameWindow:
    def __init__(self):
        try:
            self.epd = epd2in13_V4.EPD()
            #logging.info("Start EDP init")
            self.epd.init()
            #logging.info("init successfull")
            self.epd.Clear(0xFF)

            self.paddle = Paddle(self.epd)
            self.ball = Ball(self.epd)

            self.running = True
            self.initiateDisplay()
            self.updateDisplay()
        except IOError as e:
            logging.error("IOError: %s", e)
        except Exception as ex:
            logging.error("Unexpected error: %s", ex)

    def initiateDisplay(self):
        image = Image.new('1', (self.epd.height, self.epd.width),1)
        draw = ImageDraw.Draw(image)

        self.paddle.initiatePaddle(draw)
        self.ball.initiateBall(draw)
        
        self.epd.displayPartBaseImage(self.epd.getbuffer(image))
        

    
    def updateDisplay(self):
        try:
            while self.running:
                image = Image.new('1', (self.epd.height, self.epd.width), 1)
                draw = ImageDraw.Draw(image)

                self.paddle.initiatePaddle(draw)
                self.ball.move(draw)

                self.epd.displayPartial(self.epd.getbuffer(image))
                #logging.info("Display updated")
                
                time.sleep(0.5)
        except IOError as e:
            logging.error("IOError: %s", e)
        except Exception as ex:
            logging.error("Unexpected error: %s", ex)
        finally:
            self.cleanup()
    
    def cleanup(self):
        try:
            self.epd.sleep()
            self.epd.Clear(0xFF)
            #logging.info("EPD cleaned up")
        except Exception as e:
            logging.error("Error during cleanup: %s", e)

if __name__ == "__main__":

    try:
        game = GameWindow()
        pause()
    except IOError as e:
        logging.error("IOError: %s", e)
    except Exception as ex:
        logging.error("Unexpected error: %s", ex)