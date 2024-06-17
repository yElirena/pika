#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import gpiozero
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image, ImageDraw, ImageFont
from signal import pause
import random


# GPIO button initialization
btn_links = gpiozero.Button(19)
btn_rechts = gpiozero.Button(20)
btn_oben = gpiozero.Button(16)
btn_unten = gpiozero.Button(26)
btn_a = gpiozero.Button(6)
btn_b = gpiozero.Button(12)
tb = gpiozero.TonalBuzzer(5)


# Main menu program
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)

# images
normal = Image.open(os.path.join(picdir, 'normal.bmp'))
walk = Image.open(os.path.join(picdir, 'walk.bmp'))
animation = [normal, walk]
for img in animation:
    img = img.resize((48, 48), Image.ANTIALIAS)


def loadscreen():
    global image
    load_bmp = Image.open(os.path.join(picdir, 'kona.bmp'))
    load_bmp = load_bmp.resize((epd.height, epd.width), Image.ANTIALIAS)
    image.paste(load_bmp)
    image = image.transpose(Image.ROTATE_180)
    epd.displayPartBaseImage(epd.getbuffer(image))
    time.sleep(1)


def imagesetup():
    global draw, image
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)


def menu():
    global draw, image
    background = Image.open(os.path.join(picdir, 'background.bmp'))
    image.paste(background, (0, 0))


def healthbar():
    num = kona.food
    global draw, image
    heart = Image.open(os.path.join(picdir, 'heart.bmp'))
    x = 10
    for i in range(num):
        image.paste(heart, (10+(i*x), 12))


def updateScreen():
    global image, draw
    imagesetup()
    menu()
    healthbar()
    # draw.rectangle([(kona.x, kona.x), (kona.x+48, kona.x+48)], fill=255)
    image.paste(kona.img, (kona.x, kona.y))
    image = image.transpose(Image.ROTATE_180)
    epd.displayPartial(epd.getbuffer(image))


class Kona:
    age = 0
    bored = 0
    food = 5
    exhausted = 0
    alive = True
    x = 100
    y = 40
    img = normal

    def hatch():
        global draw, image
        egg1 = Image.open(os.path.join(picdir, 'egg1.bmp'))
        egg2 = Image.open(os.path.join(picdir, 'egg2.bmp'))
        egg3 = Image.open(os.path.join(picdir, 'egg3.bmp'))
        egg4 = Image.open(os.path.join(picdir, 'egg4.bmp'))
        egg5 = Image.open(os.path.join(picdir, 'egg5.bmp'))
        egg6 = Image.open(os.path.join(picdir, 'egg6.bmp'))
        eggs = [egg1, egg2, egg1, egg2, egg3, egg4, egg5, egg6]
        c = 0
        for egg in eggs:
            c += 1
            egg = egg.rotate(180)
            egg = egg.resize((48, 48), Image.ANTIALIAS)
            image.paste(egg, (kona.x, kona.y))
            tb.play(gpiozero.tones.Tone.from_frequency(440))
            if c == len(eggs):
                time.sleep(0.5)
            else:
                time.sleep(0.1) 
            tb.stop()
            epd.displayPartial(epd.getbuffer(image))
            time.sleep(1)


    def walk():
        global draw, image
        num = random.randint(1, 9)
        print(num)
        kona.img = walk
        for i in range(num):
            kona.x -= 10
            updateScreen()
        kona.img = normal
        updateScreen()


    def eat():
        kona.food = kona.food + 1



kona = Kona

try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    loadscreen()
    
    updateScreen()

    # kona.hatch()
    kona.food = 8
    updateScreen()
    time.sleep(1)
    kona.eat()
    updateScreen()
    kona.food = 3
    kona.walk()
    time.sleep(1)
    kona.walk()

    #pause()

    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
