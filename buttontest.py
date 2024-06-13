#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from waveshare_epd import epd2in13_V4
from gpiozero import Button
from signal import pause
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
from PIL import Image,ImageDraw,ImageFont


picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


def sb1():
    print("GPIO 16 Button 'oben' was pressed!")
    draw.rectangle((20, 80, 220, 105), fill = 255)
    draw.text((20, 80), 'GPIO 16 Button: oben', font = font15, fill = 0)
    epd.displayPartial(epd.getbuffer(image))
    global tb
    f = 392.0
    tb.play(Tone.from_frequency(f))
    sleep(0.2)
    tb.stop()
        

def sb2():
    print("GPIO 19 Button 'links' was pressed!")
    draw.rectangle((20, 80, 220, 105), fill = 255)
    draw.text((20, 80), 'GPIO 19 Button: links', font = font15, fill = 0)
    epd.displayPartial(epd.getbuffer(image))
    global tb
    f = 440.0
    tb.play(Tone.from_frequency(f))
    sleep(0.2)
    tb.stop()

def sb3():
    print("GPIO 20 Button 'rechts' was pressed!")
    draw.rectangle((20, 80, 220, 105), fill = 255)
    draw.text((20, 80), 'GPIO 20 Button: rechts', font = font15, fill = 0)
    epd.displayPartial(epd.getbuffer(image))
    global tb
    f = 493.88
    tb.play(Tone.from_frequency(f))
    sleep(0.2)
    tb.stop()

def sb4():
    print("GPIO 26 Button 'unten' was pressed!")
    draw.rectangle((20, 80, 220, 105), fill = 255)
    draw.text((20, 80), 'GPIO 26 Button: unten', font = font15, fill = 0)
    epd.displayPartial(epd.getbuffer(image))
    global tb
    f = 523.25
    tb.play(Tone.from_frequency(f))
    sleep(0.2)
    tb.stop()

def sb5():
    print("Goodbye! 6 a")
    global tb
    f = 587.33
    tb.play(Tone.from_frequency(f))
    sleep(0.2)
    tb.stop()

def sb6():
    draw.text
    print("Goodbye! 12 b")
    global tb
    f = 659.25
    tb.play(Tone.from_frequency(f))
    sleep(0.2)
    tb.stop()


# gpio setup
# gpio setup
tb = TonalBuzzer(5)
btn_links = Button(19)
btn_rechts = Button(20)
btn_oben = Button(16)
btn_unten = Button(26)
btn_a = Button(6)
btn_b = Button(12)

btn_oben.when_pressed = sb1
btn_links.when_pressed = sb2
btn_rechts.when_pressed = sb3
btn_unten.when_pressed = sb4
btn_a.when_pressed = sb5
btn_b.when_pressed = sb6

font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)

try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    draw.text((115, 8), 'Buttontest:', font = font15, fill = 0)
    epd.display_fast(epd.getbuffer(image))


    pause()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()