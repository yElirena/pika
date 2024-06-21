#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import adafruit_dht
from PIL import Image, ImageDraw, ImageFont
import board
import matplotlib.pyplot as plt
import pandas as pd
from waveshare_epd import epd2in13_V4
import io
from gpiozero import Button
from signal import pause
import logging
import gpsd

# gps initialisieren
gpsd.connect()

# dht-sensor initialisieren
DHT_SENSOR = adafruit_dht.DHT11(board.D15)

# e-paper-display initialisieren
epd = epd2in13_V4.EPD()
epd.init()

# dateiname für csv
csv_filename = "sensor_data.csv"

# csv-datei laden oder neuen dataframe erstellen
if os.path.exists(csv_filename):
    data = pd.read_csv(csv_filename, parse_dates=["Timestamp"])
else:
    data = pd.DataFrame(columns=["Timestamp", "Temperature", "Humidity"])

# menüoptionen
options = ["Graph anzeigen", "Werte anzeigen", "GPS anzeigen", "Exit"]

# schriftart laden
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)

# definition der field und menue klassen
class Field:
    def __init__(self, name, x_0, y_0, x_1, y_1):
        self.name = name
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = x_1
        self.y_1 = y_1

class Menu:
    def __init__(self):
        self.fields = []
        self.current_field = None

    def set_fields(self, fields):
        self.fields = fields
        self.current_field = fields[0] if fields else None

    def next_field(self):
        index = self.fields.index(self.current_field)
        self.current_field = self.fields[(index + 1) % len(self.fields)]

    def previous_field(self):
        index = self.fields.index(self.current_field)
        self.current_field = self.fields[(index - 1) % len(self.fields)]

# menüfelder initialisieren
fields = [
    Field("Graph anzeigen", 10, 40, 120, 70),
    Field("Werte anzeigen", 10, 80, 120, 110),
    Field("GPS anzeigen", 130, 40, 240, 70),
    Field("Exit", 130, 80, 240, 110)
]

sensor_menu = Menu()
sensor_menu.set_fields(fields)

# aktuelles feld zeichnen
def draw_current_field():
    image = Image.new('1', (epd.height, epd.width), 255)  # epd.height und epd.width sind vertauscht
    draw = ImageDraw.Draw(image)
    
    for field in sensor_menu.fields:
        if field == sensor_menu.current_field:
            draw.rectangle([(field.x_0, field.y_0), (field.x_1, field.y_1)], outline=0, fill=0)
            draw.text((field.x_0 + 10, field.y_0 + 5), field.name, font=font, fill=255)
        else:
            draw.text((field.x_0 + 10, field.y_0 + 5), field.name, font=font, fill=0)
    
    rotated_image = image.rotate(180, expand=True)
    epd.displayPartial(epd.getbuffer(rotated_image))

# option auswählen
def select_option():
    if sensor_menu.current_field.name == "Graph anzeigen":
        display_graph()
    elif sensor_menu.current_field.name == "Werte anzeigen":
        if len(data) > 0:
            last_data = data.iloc[-1]
            display_text(last_data["Temperature"], last_data["Humidity"])
    elif sensor_menu.current_field.name == "GPS anzeigen":
        display_gps()
    elif sensor_menu.current_field.name == "Exit":
        return_to_testmenu()

# text anzeigen (temperatur und luftfeuchtigkeit)
def display_text(temperature, humidity):
    image = Image.new('1', (epd.height, epd.width), 255)  # epd.height und epd.width sind vertauscht
    draw = ImageDraw.Draw(image)
    draw.text((10, 40), f"Temp {temperature:.1f}C", font=font, fill=0)
    draw.text((10, 80), f"Humidity {humidity:.1f}%", font=font, fill=0)
    rotated_image = image.rotate(180, expand=True)
    epd.displayPartial(epd.getbuffer(rotated_image))
    wait_for_exit()

# graph anzeigen und live aktualisieren
def display_graph():
    while not btn_b.is_pressed:
        if len(data) < 2:
            # nicht genug daten für einen graphen
            display_text("Nicht genug", "Daten")
            return

        # eine abbildung mit der exakten größe für das e-paper-display erstellen
        fig, ax = plt.subplots(figsize=(2.5, 1.2))  # verkleinerte größe für das display in zoll

        # temperatur- und luftfeuchtigkeitsdaten plotten
        ax.plot(data["Timestamp"], data["Temperature"], label='Temperatur (C)', linestyle='-')  # durchgezogene linie für temperatur
        ax.plot(data["Timestamp"], data["Humidity"], label='Humidity (%)', linestyle='--')  # gestrichelte linie für luftfeuchtigkeit

        ax.set_xlabel('Zeit')
        ax.set_ylabel('Werte')

        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=100)  # die abbildung in den puffer speichern
        buffer.seek(0)
        image = Image.open(buffer).convert('1')
        image = image.resize((250, 122))  # sicherstellen, dass die bildgröße 250x122 pixel beträgt

        rotated_image = image.rotate(180, expand=True)
        epd.displayPartial(epd.getbuffer(rotated_image))
        
        time.sleep(1)
        
        if btn_b.is_pressed:
            draw_current_field()
            break

# gps-daten anzeigen
def display_gps():
    try:
        packet = gpsd.get_current()
        latitude = packet.lat
        longitude = packet.lon
        altitude = packet.alt
        speed = packet.hspeed
        image = Image.new('1', (epd.height, epd.width), 255)  # epd.height und epd.width sind vertauscht
        draw = ImageDraw.Draw(image)
        draw.text((10, 20), f"Latitude {latitude:.6f}", font=font, fill=0)
        draw.text((10, 50), f"Longitude {longitude:.6f}", font=font, fill=0)
        draw.text((10, 80), f"Altitude {altitude:.2f}m", font=font, fill=0)
        draw.text((10, 110), f"Speed {speed:.2f}m/s", font=font, fill=0)
        rotated_image = image.rotate(180, expand=True)
        epd.displayPartial(epd.getbuffer(rotated_image))
        wait_for_exit()
    except Exception as e:
        logging.error(f"GPS error {e}")
        display_no_gps()
        

def display_no_gps():
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    draw.text((10, 40), "No GPS in use", font=font, fill=0)
    rotated_image = image.rotate(180, expand=True)
    epd.displayPartial(epd.getbuffer(rotated_image))
    wait_for_exit()

# logik für tastendruck
def press_logic(num):
    if num in [0, 4]:
        sensor_menu.previous_field()
    elif num in [1, 5]:
        sensor_menu.next_field()
    elif num == 2:
        select_option()
    draw_current_field()

def wait_for_exit():
    while True:
        if btn_b.is_pressed:
            draw_current_field()
            break

def return_to_testmenu():
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    sys.exit()

# buttons initialisieren
btn_oben = Button(16)
btn_unten = Button(20)
btn_a = Button(6)
btn_b = Button(12)
btn_links = Button(19)
btn_rechts = Button(26)

btn_oben.when_pressed = lambda: press_logic(0)
btn_unten.when_pressed = lambda: press_logic(1)
btn_a.when_pressed = lambda: press_logic(2)
btn_b.when_pressed = lambda: wait_for_exit()
btn_links.when_pressed = lambda: press_logic(4)
btn_rechts.when_pressed = lambda: press_logic(5)

# dht-sensor auslesen
def read_dht_sensor(retries=5):
    for _ in range(retries):
        try:
            temperature = DHT_SENSOR.temperature
            humidity = DHT_SENSOR.humidity
            if temperature is not None and humidity is not None:
                timestamp = pd.Timestamp.now()
                # die messwerte zum dataframe hinzufügen
                data.loc[len(data)] = [timestamp, temperature, humidity]
                data.to_csv(csv_filename, index=False)  # daten in csv-datei speichern
                print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
                return
            else:
                print("Fehler beim Abrufen der Daten vom DHT-Sensor")
        except RuntimeError as e:
            # das auslesen funktioniert nicht immer! fehler ausgeben und erneut versuchen
            print("Fehler beim Lesen vom DHT-Sensor: ", e.args)
        except Exception as e:
            # allgemeine ausnahmebehandlung für andere fehler
            print("Unerwarteter Fehler: ", e)
        time.sleep(2)  # warten, bevor erneut versucht wird
    print("Fehler beim Lesen vom DHT-Sensor nach mehreren Versuchen")

try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)
    draw_current_field()
    
    while True:
        read_dht_sensor()
        time.sleep(10)
        
except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    logging.info("Strg + C")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
