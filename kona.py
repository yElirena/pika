#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import gpiozero
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image, ImageDraw, ImageFont
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

font25 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 25)
font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)


# setup variables
courser = 0
poopPosX = 0
poopPosY = 0
poopSwitch = 0
menuSwitch = False
foodOnScreen = 0
mealLeft = 0


# images age 1
bread1 = Image.open(os.path.join(picdir, 'bread1.bmp'))
bread2 = Image.open(os.path.join(picdir, 'bread2.bmp'))
bread3 = Image.open(os.path.join(picdir, 'bread3.bmp'))
poop1 = Image.open(os.path.join(picdir, 'poop1.bmp'))
poop2 = Image.open(os.path.join(picdir, 'poop2.bmp'))
normal = Image.open(os.path.join(picdir, 'ynormal.bmp'))
walk = Image.open(os.path.join(picdir, 'ywalk.bmp'))
bored1 = Image.open(os.path.join(picdir, 'ybored1.bmp'))
bored2 = Image.open(os.path.join(picdir, 'ybored2.bmp'))
sleep1 = Image.open(os.path.join(picdir, 'ysleep1.bmp'))
sleep2 = Image.open(os.path.join(picdir, 'ysleep2.bmp'))
sleep3 = Image.open(os.path.join(picdir, 'ysleep3.bmp'))
eat = Image.open(os.path.join(picdir, 'yeat.bmp'))
happy1 = Image.open(os.path.join(picdir, 'yhappy1.bmp'))
happy2 = Image.open(os.path.join(picdir, 'yhappy2.bmp'))
happy3 = Image.open(os.path.join(picdir, 'happy3.bmp'))
# images age 0
# ynormal = Image.open(os.path.join(picdir, 'ynormal.bmp'))
# ywalk = Image.open(os.path.join(picdir, 'ywalk.bmp'))
# ybored1 = Image.open(os.path.join(picdir, 'ybored1.bmp'))
# ybored2 = Image.open(os.path.join(picdir, 'ybored2.bmp'))
# ysleep1 = Image.open(os.path.join(picdir, 'ysleep1.bmp'))
# ysleep2 = Image.open(os.path.join(picdir, 'ysleep2.bmp'))
# ysleep3 = Image.open(os.path.join(picdir, 'ysleep3.bmp'))
# yeat = Image.open(os.path.join(picdir, 'yeat.bmp'))
# yhappy1 = Image.open(os.path.join(picdir, 'yhappy1.bmp'))
# yhappy2 = Image.open(os.path.join(picdir, 'yhappy2.bmp'))

# animationPictures = [normal, walk]
# for img in animationPictures:
#     img = img.resize((48, 48), Image.ANTIALIAS)


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


def background():
    global draw, image
    background = Image.open(os.path.join(picdir, 'background.bmp'))
    image.paste(background, (0, 0))


def healthbar():
    num = kona.food
    global draw, image
    heart = Image.open(os.path.join(picdir, 'heart.bmp'))
    x = 10
    for i in range(num):
        image.paste(heart, (10 + (i * x), 12))


def drawpoop():
    global image, poopPosX, poopPosY, poopSwitch
    poopSwitch += 1
    if kona.haspooped:
        if poopSwitch % 2 == 0:
            image.paste(poop1, (poopPosX, poopPosY))
        else:
            image.paste(poop2, (poopPosX, poopPosY))


def drawFood():
    global image, foodOnScreen
    if foodOnScreen == 3:
        image.paste(bread1, (110, 76))
    elif foodOnScreen == 2:
        image.paste(bread2, (110, 76))
    elif foodOnScreen == 1:
        image.paste(bread3, (110, 76))


def updateScreen():
    global image, draw
    imagesetup()
    background()
    healthbar()
    drawpoop()
    drawFood()
    image.paste(kona.img, (kona.x, kona.y))
    drawMenuScreen()
    image = image.transpose(Image.ROTATE_180)
    epd.displayPartial(epd.getbuffer(image))


def printsStats():
    print(f'{kona.age}  age')
    print(f'{kona.boredness} bored')
    print(f'{kona.food} food')
    print(f'{kona.exhausted} exhausted')


def drawMenuScreen():
    global draw, courser, mealLeft
    if menuSwitch:
        draw.rectangle((20, 20, 230, 100), fill=255)
        draw.rectangle((20, 20, 230, 100), outline=0, width=4)
        x = 0
        y = 0
        if courser == 0:
            x = 25
            y = x + 56
        elif courser == 1:
            x = 85
            y = x + 63
        elif courser == 2:
            x = 150
            y = x + 67
        draw.rectangle((x, 37, y, 78), outline=0, width=2)
        draw.text((30, 42), 'quiz', font=font25, fill=0)
        draw.text((90, 42), 'Meal', font=font25, fill=0)
        draw.text((155, 42), 'clean', font=font25, fill=0)
        draw.text((94, 24), f'Meal left: {mealLeft}', font=font10, fill=0)


def menuOnOff():
    global menuSwitch
    if menuSwitch:
        menuSwitch = False
    else:
        menuSwitch = True


# selectable menu function
def courserleft():
    global courser
    if courser - 1 >= 0:
        courser -= 1
    else:
        courser = 2


def courserright():
    global courser
    if courser + 1 <= 2:
        courser += 1
    else:
        courser = 0


def select():
    global courser
    if courser == 2 and menuSwitch:
        clean()
        menuOnOff()
    elif courser == 1 and menuSwitch:
        meal()
        menuOnOff()
    elif courser == 0 and menuSwitch:
        quiz()
        menuOnOff()


def clean():
    kona.haspooped = False


def meal():
    global foodOnScreen, mealLeft
    foodOnScreen = 3
    mealLeft -= 1


def quiz():
    global mealLeft
    mealLeft += 1


btn_a.when_pressed = select
btn_b.when_pressed = menuOnOff

btn_links.when_pressed = courserleft
btn_rechts.when_pressed = courserright


class Kona:
    age = 0
    boredness = 0
    food = 5
    exhausted = 0
    alive = True
    x = 100
    y = 45
    img = normal
    haspooped = False

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
            egg = egg.resize((64, 64), Image.ANTIALIAS)
            image.paste(egg, (kona.x, kona.y - 20))
            tb.play(gpiozero.tones.Tone.from_frequency(440))
            if c == len(eggs):
                time.sleep(0.5)
            else:
                time.sleep(0.1) 
            tb.stop()
            epd.displayPartial(epd.getbuffer(image))
            time.sleep(1)

    def walkRight():
        global draw, image
        num = random.randint(1, 9)
        kona.img = walk
        for i in range(num):
            kona.exhausted += 1
            if kona.x - 10 > 0:
                kona.x -= 10
                updateScreen()
            else:
                break
        kona.img = normal

    def walkleft():
        global draw, image
        num = random.randint(1, 9)
        kona.img = walk.transpose(Image.FLIP_LEFT_RIGHT)
        for i in range(num):
            kona.exhausted += 1
            if kona.x + 10 < 190:
                kona.x += 10
                updateScreen()
            else:
                break
        kona.img = normal

    def eat():
        global foodOnScreen
        while foodOnScreen > 0:
            kona.img = eat
            kona.food = kona.food + 1
            updateScreen()
            kona.img = normal
            foodOnScreen -= 1
            updateScreen()

    def happy():
        kona.img = happy1
        updateScreen()
        kona.img = happy2
        if kona.age > 1:
            updateScreen()
            kona.img = happy3

    def bored():
        kona.img = bored1
        updateScreen()
        kona.img = bored2
        updateScreen()
        kona.img = normal

    def sleep():
        global image, sleep
        for i in range(1, 25):
            kona.img = sleep1
            updateScreen()
            kona.img = sleep2
            updateScreen()
            kona.img = sleep3
            updateScreen()
        kona.exhausted = 0
        kona.img = normal

    def evolve():
        global normal, walk, bored1, bored2, sleep1, sleep2, sleep3, eat, happy1, happy2, happy3
        kona.y = 35
        # ynormal = Image.open(os.path.join(picdir, 'ynormal.bmp'))
        # ywalk = Image.open(os.path.join(picdir, 'ywalk.bmp'))
        # ybored1 = Image.open(os.path.join(picdir, 'ybored1.bmp'))
        # ybored2 = Image.open(os.path.join(picdir, 'ybored2.bmp'))
        # ysleep1 = Image.open(os.path.join(picdir, 'ysleep1.bmp'))
        # ysleep2 = Image.open(os.path.join(picdir, 'ysleep2.bmp'))
        # ysleep3 = Image.open(os.path.join(picdir, 'ysleep3.bmp'))
        # yeat = Image.open(os.path.join(picdir, 'yeat.bmp'))
        # yhappy1 = Image.open(os.path.join(picdir, 'yhappy1.bmp'))
        # yhappy2 = Image.open(os.path.join(picdir, 'yhappy2.bmp'))
        normal = Image.open(os.path.join(picdir, 'normal.bmp'))
        walk = Image.open(os.path.join(picdir, 'walk.bmp'))
        bored1 = Image.open(os.path.join(picdir, 'bored1.bmp'))
        bored2 = Image.open(os.path.join(picdir, 'bored2.bmp'))
        sleep1 = Image.open(os.path.join(picdir, 'sleep1.bmp'))
        sleep2 = Image.open(os.path.join(picdir, 'sleep2.bmp'))
        sleep3 = Image.open(os.path.join(picdir, 'sleep3.bmp'))
        eat = Image.open(os.path.join(picdir, 'eat.bmp'))
        happy1 = Image.open(os.path.join(picdir, 'happy1.bmp'))
        happy2 = Image.open(os.path.join(picdir, 'happy2.bmp'))
        happy3 = Image.open(os.path.join(picdir, 'happy3.bmp'))

    def poop():
        global poopPosX, poopPosY
        kona.haspooped = True
        poopPosX = kona.x - 20
        poopPosY = kona.y + 32


kona = Kona
animations = [kona.walkRight, kona.walkleft, kona.happy, kona.bored, kona.eat]
# animations = [kona.sleep]


try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    loadscreen()

    updateScreen()

    # kona.hatch()
    # kona.food = 8
    # updateScreen()
    # time.sleep(1)
    # kona.eat()
    # updateScreen()
    # kona.food = 3
    # kona.walk()
    # time.sleep(1)
    # kona.walk()
    count = 0
    while kona.alive:
        printsStats()
        count += 1
        if count > 10:
            kona.evolve()
        if kona.exhausted >= 30:
            kona.sleep()
        if count % 5 == 0:
            if not kona.haspooped:
                kona.poop()
        random.choice(animations)()
        time.sleep(random.randint(1, 2))
        updateScreen()

    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
