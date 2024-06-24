#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
from gpiozero import Button
import logging
from waveshare_epd import epd2in13_V4
from PIL import Image, ImageDraw, ImageFont
from signal import pause


# Klassen
class Field:
    def __init__(self, name, field_nr):
        self.x_0 = 0
        self.y_0 = 0
        self.x_1 = 0
        self.y_1 = 0
        self.name = name
        self.field_nr = field_nr

    def set_XY_0(self, x, y):
        self.x_0 = x
        self.y_0 = y

    def set_XY_1(self, x, y):
        self.x_1 = x
        self.y_1 = y


class Menue:
    def __init__(self):
        self.field_array = [[]]
        self.current_field = Field("0", "0")

    def set_feldarray(self, field_array):
        self.field_array = field_array       

    def set_current_field(self, current_field):
        self.current_field = current_field


feld_00 = Field("Thomas", "00")
feld_00.set_XY_0(231, 89)
feld_00.set_XY_1(134, 57)
feld_01 = Field("Marv", "01")
feld_01.set_XY_0(115, 89)
feld_01.set_XY_1(19, 57)
feld_10 = Field("Roman", "10")
feld_10.set_XY_0(231, 40)
feld_10.set_XY_1(134, 8)
feld_11 = Field("Marie", "11")
feld_11.set_XY_0(115, 40)
feld_11.set_XY_1(19, 8)
 
field_array = [[feld_00, feld_01],
               [feld_10, feld_11]]
 
 
main_menue = Menue()
main_menue.set_feldarray(field_array)
main_menue.set_current_field(field_array[0][0])

 
# Main Menü Programm
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
 
 
def draw_current_field():
    global draw1, final_image
    current_field = main_menue.current_field
    field_oben_links = main_menue.field_array[0][0]
    field_oben_rechts = main_menue.field_array[0][1]
    field_unten_links = main_menue.field_array[1][0]
    field_unten_rechts = main_menue.field_array[1][1]
 
    if (current_field.name == "Thomas"):
        draw1.rectangle([(field_oben_links.x_0, field_oben_links.y_0), (field_oben_links.x_1, field_oben_links.y_1)], outline=0, width=3)
        draw1.rectangle([(field_oben_rechts.x_0, field_oben_rechts.y_0), (field_oben_rechts.x_1, field_oben_rechts.y_1)], outline=255, width=3)
        draw1.rectangle([(field_unten_links.x_0, field_unten_links.y_0), (field_unten_links.x_1, field_unten_links.y_1)], outline=255, width=3)
        draw1.rectangle([(field_unten_rechts.x_0, field_unten_rechts.y_0), (field_unten_rechts.x_1, field_unten_rechts.y_1)], outline=255, width=3)
        epd.displayPartial(epd.getbuffer(final_image))
    elif (current_field.name == "Marv"):
        draw1.rectangle([(field_oben_links.x_0, field_oben_links.y_0), (field_oben_links.x_1, field_oben_links.y_1)], outline=255, width=3)
        draw1.rectangle([(field_oben_rechts.x_0, field_oben_rechts.y_0), (field_oben_rechts.x_1, field_oben_rechts.y_1)], outline=0, width=3)
        draw1.rectangle([(field_unten_links.x_0, field_unten_links.y_0), (field_unten_links.x_1, field_unten_links.y_1)], outline=255, width=3)
        draw1.rectangle([(field_unten_rechts.x_0, field_unten_rechts.y_0), (field_unten_rechts.x_1, field_unten_rechts.y_1)], outline=255, width=3)
        epd.displayPartial(epd.getbuffer(final_image))
    elif (current_field.name == "Roman"):
        draw1.rectangle([(field_oben_links.x_0, field_oben_links.y_0), (field_oben_links.x_1, field_oben_links.y_1)], outline=255, width=3)
        draw1.rectangle([(field_oben_rechts.x_0, field_oben_rechts.y_0), (field_oben_rechts.x_1, field_oben_rechts.y_1)], outline=255, width=3)
        draw1.rectangle([(field_unten_links.x_0, field_unten_links.y_0), (field_unten_links.x_1, field_unten_links.y_1)], outline=0, width=3)
        draw1.rectangle([(field_unten_rechts.x_0, field_unten_rechts.y_0), (field_unten_rechts.x_1, field_unten_rechts.y_1)], outline=255, width=3)
        epd.displayPartial(epd.getbuffer(final_image))
    else:
        draw1.rectangle([(field_oben_links.x_0, field_oben_links.y_0), (field_oben_links.x_1, field_oben_links.y_1)], outline=255, width=3)
        draw1.rectangle([(field_oben_rechts.x_0, field_oben_rechts.y_0), (field_oben_rechts.x_1, field_oben_rechts.y_1)], outline=255, width=3)
        draw1.rectangle([(field_unten_links.x_0, field_unten_links.y_0), (field_unten_links.x_1, field_unten_links.y_1)], outline=255, width=3)
        draw1.rectangle([(field_unten_rechts.x_0, field_unten_rechts.y_0), (field_unten_rechts.x_1, field_unten_rechts.y_1)], outline=0, width=3)
        epd.displayPartial(epd.getbuffer(final_image))
 
 
def press_logic(num):
    if num == 0:
        if (main_menue.current_field.name == "Marv"):
            main_menue.set_current_field(main_menue.field_array[0][0])
            draw_current_field()
        elif (main_menue.current_field.name == "Marie"):
            main_menue.set_current_field(main_menue.field_array[1][0])
            draw_current_field()
    elif num == 1:
        if (main_menue.current_field.name == "Thomas"):
            main_menue.set_current_field(main_menue.field_array[0][1])
            draw_current_field()
        elif (main_menue.current_field.name == "Roman"):
            main_menue.set_current_field(main_menue.field_array[1][1])
            draw_current_field()
    elif num == 2:
        if (main_menue.current_field.name == "Roman"):
            main_menue.set_current_field(main_menue.field_array[0][0])
            draw_current_field()
        elif (main_menue.current_field.name == "Marie"):
            main_menue.set_current_field(main_menue.field_array[0][1])
            draw_current_field()
    elif num == 3:
        if (main_menue.current_field.name == "Thomas"):
            main_menue.set_current_field(main_menue.field_array[1][0])
            draw_current_field()
        elif (main_menue.current_field.name == "Marv"):
            main_menue.set_current_field(main_menue.field_array[1][1])
            draw_current_field()
    elif num == 4:
        if(main_menue.current_field.name == "Thomas"):
            os.system("/home/pi/pika/sensor.py")
            exit()
        elif(main_menue.current_field.name == "Marv"):
            os.system("/home/pi/pika/marv.py")
            exit()
        elif(main_menue.current_field.name == "Roman"):
            os.system("/home/pi/pika/kona.py")
            exit()
        elif(main_menue.current_field.name == "Marie"):
            pass
 
 
# gpio button
btn_links = Button(19)
btn_rechts = Button(20)
btn_oben = Button(16)
btn_unten = Button(26)
btn_a = Button(6)
btn_b = Button(12)

btn_links.when_pressed = lambda: press_logic(0)
btn_rechts.when_pressed = lambda: press_logic(1)
btn_oben.when_pressed = lambda: press_logic(2)
btn_unten.when_pressed = lambda: press_logic(3)
btn_a.when_pressed = lambda: press_logic(4)


font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)

try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)
 
    image = Image.new('1', (epd.height, epd.width), 255)
 
    draw = ImageDraw.Draw(image)
 
    bmp = Image.open(os.path.join(picdir, 'temp.bmp'))
    bmp1 = Image.open(os.path.join(picdir, 'checker.bmp'))
    bmp2 = Image.open(os.path.join(picdir, 'kona.bmp'))
    bmp3 = Image.open(os.path.join(picdir, 'breakout.bmp'))
 
    draw.text((115, 8), 'Pika:', font=font15, fill=0)
 
    image.paste(bmp, (19, 32))
    image.paste(bmp1, (135, 32))
    image.paste(bmp2, (19, 82))
    image.paste(bmp3, (135, 82))
 
    rotated_image = image.rotate(180, expand=True)  # rotate
 
    epd.displayPartBaseImage(epd.getbuffer(rotated_image))
 
    original_width, original_height = image.size
    rotated_width, rotated_height = rotated_image.size
 
    offset_x = (rotated_width - original_width) // 2
    offset_y = (rotated_height - original_height) // 2
 
    final_image = Image.new('1', (rotated_width, rotated_height), 255)
 
    # final_image = final_image.rotate(180)
    final_image.paste(rotated_image)
    draw1 = ImageDraw.Draw(final_image)
    draw_current_field()
    epd.displayPartial(epd.getbuffer(final_image))
 
    pause()
 
    epd.sleep()
 
 
except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
