from gpiozero import Button
from waveshare_epd import epd2in13_V4
from PIL import Image, ImageDraw
import logging, time
from paddle import paddle

class GameMenu:

    paddle = paddle()

    
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