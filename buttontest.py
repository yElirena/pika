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


def sb1():
    print("GPIO 16 Button 'oben' was pressed!")
    global tb
    f = 392.0
    tb.play(Tone.from_frequency(f))
    sleep(0.2)
    tb.stop()
        

def sb2():
    print("Goodbye! 19 links")
    global tb
    f = 440.0
    tb.play(Tone.from_frequency(f))
    sleep(0.2)
    tb.stop()

def sb3():
    print("Goodbye! 20 rechts" )
    global tb
    f = 493.88
    tb.play(Tone.from_frequency(f))
    sleep(0.2)
    tb.stop()

def sb4():
    print("Goodbye! 26 unten")
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
    print("Goodbye! 12 b")
    global tb
    f = 659.25
    tb.play(Tone.from_frequency(f))
    sleep(5.2)
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

btn_links.when_pressed = sb1
btn_rechts.when_pressed = sb2
btn_oben.when_pressed = sb3
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


    pause()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()