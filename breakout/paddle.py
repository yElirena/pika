from gpiozero import Button
from PIL import Image, ImageDraw
from waveshare_epd import epd2in13_V4
import logging
import time

class paddle:
    game_paused = True

    def __init__(self):
        pass


    def moveLeft(self):
        global btn_links
        if btn_links.is_pressed:
            print("Left button is being pressed")
        else:
            print("Button was pushed once.")


        pass

    def moveRight(self):
        pass

    def startPause(self):
        global game_paused, epd
        if game_paused:
            epd.sleep()
            game_paused = False
        else:
            game_paused = True


    def goBack(self):
        pass
    

    btn_links = Button(19)
    btn_rechts = Button(20)
    btn_a = Button(6)
    btn_b = Button(12)

    btn_links.when_pressed = moveLeft
    btn_rechts.when_pressed = moveRight
    btn_a.when_pressed = startPause
    btn_b.when_pressed = goBack
    
    try:
        epd = epd2in13_V4
        epd.init()
        epd.Clear(0xFF)
        paddle = Image.new('1', (epd.height, epd.width), 0)

        drawPaddle = ImageDraw.Draw(paddle)
        drawPaddle.rounded_rectangle([(112, 4), (122, 8)], radius= 1, fill = 0, width = 1)
        epd.displayPartial(epd.getbuffer(paddle))
        time.sleep(0.5)
    
    except IOError as e:
        logging.info(e)