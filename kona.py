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


# setup variables
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

font25 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 25)
font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)

courser = 0
poopPosX = 0
poopPosY = 0
poopSwitch = 0
menuSwitch = False
foodOnScreen = 0
mealLeft = 0


# images
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


# display functions
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
    image.paste(kona.img, (kona.x, kona.y))
    drawFood()
    drawMenuScreen()
    image = image.transpose(Image.ROTATE_180)
    epd.displayPartial(epd.getbuffer(image))


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


# Menu functions
def printsStats():
    print(f'{kona.age}  age')
    print(f'{kona.boredness} bored')
    print(f'{kona.food} food')
    print(f'{kona.exhausted} exhausted')
    print(f'{kona.happyness} happyness')
    print(' '.join(map(str, animations)))
    print(' '.join(map(str, cachedAnimations)))


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


# interact functions
def clean():
    kona.haspooped = False
    cachedAnimations.append(kona.happy)


def meal():
    global foodOnScreen, mealLeft
    if mealLeft > 0:
        foodOnScreen = 3
        mealLeft -= 1


def quiz():
    global mealLeft
    mealLeft += 1
    kona.happyness += 10



btn_a.when_pressed = select
btn_b.when_pressed = menuOnOff
# btn_b.when_pressed = start

btn_links.when_pressed = courserleft
btn_rechts.when_pressed = courserright


class Kona:
    age = 0
    happyness = 50
    boredness = 0
    food = 5
    exhausted = 0
    haspooped = False
    haseaten = False
    alive = True
    evolved = False
    x = 100
    y = 45
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
        kona.move_to_food()
        while foodOnScreen > 0:
            kona.img = eat
            kona.food = kona.food + 1
            updateScreen()
            kona.img = normal
            foodOnScreen -= 1
            updateScreen()
        kona.happyness += 10
        kona.haseaten = True

    def happy():
        kona.img = happy1
        updateScreen()
        kona.img = happy2
        updateScreen()
        if kona.evolved:
            kona.img = happy3
            updateScreen()
        kona.img = normal

    def bored():
        if kona.boredness > 90:
            kona.img = bored1
            updateScreen()
            kona.img = bored2
            updateScreen()
            kona.img = normal

    def sleep():
        global image, sleep
        if kona.exhausted >= 35:
            for i in range(1, 20):
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
        if not kona.evolved and kona.age > 20 and kona.happyness > 80:
            kona.y = 35
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
            kona.evolved = True

    def poop():
        global poopPosX, poopPosY
        kona.haspooped = True
        kona.haseaten = False
        poopPosX = kona.x - 20
        poopPosY = kona.y + 32

    def move_to_food():
        if kona.x < 150:
            kona.img = walk.transpose(Image.FLIP_LEFT_RIGHT)
            while kona.x < 150:
                kona.x += 10
                updateScreen()
        else:
            kona.img = walk
            while kona.x > 150:
                kona.x -= 10
                updateScreen()


kona = Kona
animations = [kona.walkRight, kona.walkleft, kona.bored, kona.evolve, kona.sleep]
cachedAnimations = []


try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    loadscreen()

    updateScreen()

    # kona.hatch()

    while kona.alive:
        printsStats()
        if foodOnScreen > 0:
            animations.append(kona.eat)
        elif foodOnScreen == 0 and kona.eat in animations:
            animations.remove(kona.eat)

        if kona.haseaten and kona.poop not in animations:
            animations.append(kona.poop)
        elif kona.haspooped and kona.poop in animations:
            animations.remove(kona.poop)

        if kona.haspooped and kona.happyness - 1 >= 0:
            kona.happyness -= 1
        if len(cachedAnimations) >= 1:
            for animation in cachedAnimations:
                animation()
            cachedAnimations = []
        if kona.happyness >= 80 and kona.happy not in animations:
            animations.append(kona.happy)
        elif kona.happy in animations and kona.happyness < 80:
            animations.remove(kona.happy)
        random.choice(animations)()
        time.sleep(random.randint(1, 2))
        updateScreen()
        kona.age += 1

    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
