#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import gpiozero
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image, ImageDraw, ImageFont
from signal import pause
import re

class Field:
    """
    Repräsentiert ein Feld mit einem Namen und Positionen (x, y).
    Kann benachbarte Felder in den Richtungen Norden, Osten, Süden und Westen haben.
    """

    def __init__(self, name):
        """
        Initialisiert ein Feld mit dem gegebenen Namen und standardmäßig Nullpositionen.
        
        Parameter:
        name (str): Der Name des Feldes.
        """
        self.x_0 = 0  # Start x-Position
        self.y_0 = 0  # Start y-Position
        self.x_1 = 0  # End x-Position
        self.y_1 = 0  # End y-Position
        self.name = name  # Name des Feldes
        self.north = None  # Nördliches Nachbarfeld
        self.east = None  # Östliches Nachbarfeld
        self.south = None  # Südliches Nachbarfeld
        self.west = None  # Westliches Nachbarfeld
    
    def set_XY_0(self, x, y):
        """
        Setzt die Startposition (x_0, y_0) des Feldes.
        
        Parameter:
        x (int): Die x-Koordinate der Startposition.
        y (int): Die y-Koordinate der Startposition.
        """
        self.x_0 = x
        self.y_0 = y

    def set_XY_1(self, x, y):
        """
        Setzt die Endposition (x_1, y_1) des Feldes.
        
        Parameter:
        x (int): Die x-Koordinate der Endposition.
        y (int): Die y-Koordinate der Endposition.
        """
        self.x_1 = x
        self.y_1 = y

    def set_north(self, north):
        """
        Setzt das nördliche Nachbarfeld.
        
        Parameter:
        north (Field): Das nördliche Nachbarfeld.
        """
        self.north = north

    def set_east(self, east):
        """
        Setzt das östliche Nachbarfeld.
        
        Parameter:
        east (Field): Das östliche Nachbarfeld.
        """
        self.east = east

    def set_south(self, south):
        """
        Setzt das südliche Nachbarfeld.
        
        Parameter:
        south (Field): Das südliche Nachbarfeld.
        """
        self.south = south

    def set_west(self, west):
        """
        Setzt das westliche Nachbarfeld.
        
        Parameter:
        west (Field): Das westliche Nachbarfeld.
        """
        self.west = west

    def set_name(self, name):
        """
        Setzt den Namen des Feldes.
        
        Parameter:
        name (str): Der neue Name des Feldes.
        """
        self.name = name

class Menue:
    """
    Repräsentiert ein Menü, das eine Liste von Feldern und ein aktuelles Feld enthält.
    """

    def __init__(self, name):
        """
        Initialisiert das Menü mit einem Namen
        
        Parameter:
        name (str): Der Name des Menüs.
        """
        self.field_array = []  # Liste der Felder im Menü
        self.name = name  # Name des Menüs

    def set_feldarray(self, field_array):
        """
        Setzt das Array der Felder im Menü.
        
        Parameter:
        field_array (list): Die neue Liste der Felder.
        """
        self.field_array = field_array

    def set_current_field(self, current_field):
        """
        Setzt das aktuelle Feld im Menü.
        
        Parameter:
        current_field (Field): Das neue aktuelle Feld.
        """
        self.current_field = current_field

## Tastaturfelder
field_space = Field(" ")
field_space.set_XY_0(152, 12)
field_space.set_XY_1(97, 4)

field_altGr = Field("Alt Gr")
field_altGr.set_XY_0(83, 12)
field_altGr.set_XY_1(55, 4)

field_shift = Field("Shift")
field_shift.set_XY_0(194, 12)
field_shift.set_XY_1(166, 4)

field_hyphen = Field("-")
field_hyphen.set_XY_0(13, 25)
field_hyphen.set_XY_1(4, 16)

field_dot = Field(".")
field_dot.set_XY_0(37, 25)
field_dot.set_XY_1(27, 16)

field_comma = Field(",")
field_comma.set_XY_0(60, 25)
field_comma.set_XY_1(50, 16)

field_m = Field("m")
field_m.set_XY_0(83, 25)
field_m.set_XY_1(74, 16)

field_n = Field("n")
field_n.set_XY_0(106, 25)
field_n.set_XY_1(97, 16)

field_b = Field("b")
field_b.set_XY_0(129, 25)
field_b.set_XY_1(120, 16)

field_v = Field("v")
field_v.set_XY_0(152, 25)
field_v.set_XY_1(143, 16)

field_c = Field("c")
field_c.set_XY_0(175, 25)
field_c.set_XY_1(166, 16)

field_x = Field("x")
field_x.set_XY_0(199, 25)
field_x.set_XY_1(189, 16)

field_y = Field("y")
field_y.set_XY_0(222, 25)
field_y.set_XY_1(212, 16)

field_smallerAs = Field("<")
field_smallerAs.set_XY_0(245, 25)
field_smallerAs.set_XY_1(236, 16)

field_hashtag = Field("#")
field_hashtag.set_XY_0(27, 37)
field_hashtag.set_XY_1(18, 29)

field_ae = Field("ä")
field_ae.set_XY_0(46,37)
field_ae.set_XY_1(37, 29)

field_oe = Field("ö")
field_oe.set_XY_0(64, 37)
field_oe.set_XY_1(55, 29)

field_l = Field("l")
field_l.set_XY_0(83, 37)
field_l.set_XY_1(74, 29)

field_k = Field("k")
field_k.set_XY_0(101, 37)
field_k.set_XY_1(92, 29)

field_j = Field("j")
field_j.set_XY_0(120, 37)
field_j.set_XY_1(111, 29)

field_h = Field("h")
field_h.set_XY_0(138, 37)
field_h.set_XY_1(129, 29)

field_g = Field("g")
field_g.set_XY_0(157, 37)
field_g.set_XY_1(148, 29)

field_f = Field("f")
field_f.set_XY_0(175, 37)
field_f.set_XY_1(166, 29)

field_d = Field("d")
field_d.set_XY_0(194, 37)
field_d.set_XY_1(185, 29)

field_s = Field("s")
field_s.set_XY_0(212, 37)
field_s.set_XY_1(203, 29)

field_a = Field("a")
field_a.set_XY_0(231, 37)
field_a.set_XY_1(222, 29)

field_plus = Field("+")
field_plus.set_XY_0(27, 50)
field_plus.set_XY_1(18, 42)

field_ue = Field("ü")
field_ue.set_XY_0(46, 50)
field_ue.set_XY_1(37, 42)

field_p = Field("p")
field_p.set_XY_0(64, 50)
field_p.set_XY_1(55, 42)

field_o = Field("o")
field_o.set_XY_0(83, 50)
field_o.set_XY_1(74, 42)

field_i = Field("i")
field_i.set_XY_0(101, 50)
field_i.set_XY_1(92, 42)

field_u = Field("u")
field_u.set_XY_0(120, 50)
field_u.set_XY_1(111, 42)

field_z = Field("z")
field_z.set_XY_0(138, 50)
field_z.set_XY_1(129, 42)

field_t = Field("t")
field_t.set_XY_0(157, 50)
field_t.set_XY_1(148, 42)

field_r = Field("r")
field_r.set_XY_0(175, 50)
field_r.set_XY_1(166, 42)

field_e = Field("e")
field_e.set_XY_0(194, 50)
field_e.set_XY_1(185, 42)

field_w = Field("w")
field_w.set_XY_0(212, 50)
field_w.set_XY_1(203, 42)

field_q = Field("q")
field_q.set_XY_0(231, 50)
field_q.set_XY_1(222, 42)

field_back = Field("back")
field_back.set_XY_0(13, 63)
field_back.set_XY_1(0, 54)

field_apostroph = Field("´")
field_apostroph.set_XY_0(27, 63)
field_apostroph.set_XY_1(18, 54)

field_sz = Field("ß")
field_sz.set_XY_0(46, 63)
field_sz.set_XY_1(37, 54)

field_0 = Field("0")
field_0.set_XY_0(64, 63)
field_0.set_XY_1(55, 54)

field_9 = Field("9")
field_9.set_XY_0(83, 63)
field_9.set_XY_1(74, 54)

field_8 = Field("8")
field_8.set_XY_0(101, 63)
field_8.set_XY_1(92, 54)

field_7 = Field("7")
field_7.set_XY_0(120, 63)
field_7.set_XY_1(111, 54)

field_6 = Field("6")
field_6.set_XY_0(138, 63)
field_6.set_XY_1(129, 54)

field_5 = Field("5")
field_5.set_XY_0(157, 63)
field_5.set_XY_1(148, 54)

field_4 = Field("4")
field_4.set_XY_0(175, 63)
field_4.set_XY_1(166, 54)

field_3 = Field("3")
field_3.set_XY_0(194, 63)
field_3.set_XY_1(185, 54)

field_2 = Field("2")
field_2.set_XY_0(212, 63)
field_2.set_XY_1(203, 54)

field_1 = Field("1")
field_1.set_XY_0(231, 63)
field_1.set_XY_1(222, 54)

field_zirkunflex = Field("^")
field_zirkunflex.set_XY_0(245, 63)
field_zirkunflex.set_XY_1(235, 56)

field_send = Field("send")
field_send.set_XY_0(27, 94)
field_send.set_XY_1(4, 84)

field_exit = Field("exit")
field_exit.set_XY_0(245, 12)
field_exit.set_XY_1(222, 4)


## Nachbarfelder setzen
field_zirkunflex.set_east(field_1)

field_1.set_west(field_zirkunflex)
field_1.set_east(field_2)
field_1.set_south(field_q)

field_2.set_west(field_1)
field_2.set_east(field_3)
field_2.set_south(field_w)

field_3.set_west(field_2)
field_3.set_east(field_4)
field_3.set_south(field_e)

field_4.set_east(field_5)
field_4.set_west(field_3)
field_4.set_south(field_r)

field_5.set_east(field_6)
field_5.set_west(field_4)
field_5.set_south(field_t)

field_6.set_east(field_7)
field_6.set_west(field_5)
field_6.set_south(field_z)

field_7.set_east(field_8)
field_7.set_west(field_6)
field_7.set_south(field_u)

field_8.set_east(field_9)
field_8.set_west(field_7)
field_8.set_south(field_i)

field_9.set_east(field_0)
field_9.set_west(field_8)
field_9.set_south(field_o)
field_9.set_north(field_send)

field_0.set_east(field_sz)
field_0.set_west(field_9)
field_0.set_south(field_p)
field_0.set_north(field_send)

field_sz.set_east(field_apostroph)
field_sz.set_west(field_0)
field_sz.set_south(field_ue)
field_sz.set_north(field_send)

field_apostroph.set_east(field_back)
field_apostroph.set_west(field_sz)
field_apostroph.set_south(field_plus)
field_apostroph.set_north(field_send)

field_back.set_west(field_apostroph)
field_back.set_north(field_send)

field_q.set_north(field_1)
field_q.set_east(field_w)
field_q.set_south(field_a)

field_w.set_north(field_2)
field_w.set_east(field_e)
field_w.set_south(field_s)
field_w.set_west(field_q)

field_e.set_north(field_3)
field_e.set_east(field_r)
field_e.set_south(field_d)
field_e.set_west(field_w)

field_r.set_north(field_4)
field_r.set_east(field_t)
field_r.set_south(field_f)
field_r.set_west(field_e)

field_t.set_north(field_5)
field_t.set_east(field_z)
field_t.set_south(field_g)
field_t.set_west(field_r)

field_z.set_north(field_6)
field_z.set_east(field_u)
field_z.set_south(field_h)
field_z.set_west(field_t)

field_u.set_north(field_7)
field_u.set_east(field_i)
field_u.set_south(field_j)
field_u.set_west(field_z)

field_i.set_north(field_8)
field_i.set_east(field_o)
field_i.set_south(field_k)
field_i.set_west(field_u)

field_o.set_north(field_9)
field_o.set_east(field_p)
field_o.set_south(field_l)
field_o.set_west(field_i)

field_p.set_north(field_0)
field_p.set_east(field_ue)
field_p.set_south(field_oe)
field_p.set_west(field_o)

field_ue.set_north(field_sz)
field_ue.set_east(field_plus)
field_ue.set_south(field_ae)
field_ue.set_west(field_p)

field_plus.set_north(field_apostroph)
field_plus.set_south(field_hashtag)
field_plus.set_west(field_ue)

field_hashtag.set_north(field_plus)
field_hashtag.set_south(field_dot)
field_hashtag.set_west(field_ae)

field_ae.set_north(field_ue)
field_ae.set_east(field_hashtag)
field_ae.set_south(field_dot)
field_ae.set_west(field_oe)

field_oe.set_north(field_ue)
field_oe.set_east(field_ae)
field_oe.set_south(field_comma)
field_oe.set_west(field_l)

field_l.set_north(field_o)
field_l.set_east(field_oe)
field_l.set_south(field_m)
field_l.set_west(field_k)

field_k.set_north(field_i)
field_k.set_east(field_l)
field_k.set_south(field_n)
field_k.set_west(field_j)

field_j.set_north(field_u)
field_j.set_east(field_k)
field_j.set_south(field_b)
field_j.set_west(field_h)

field_h.set_north(field_z)
field_h.set_east(field_j)
field_h.set_south(field_b)
field_h.set_west(field_g)

field_g.set_north(field_t)
field_g.set_east(field_h)
field_g.set_south(field_v)
field_v.set_west(field_h)

field_f.set_north(field_r)
field_f.set_east(field_g)
field_f.set_south(field_c)
field_f.set_west(field_d)

field_d.set_north(field_e)
field_d.set_east(field_f)
field_d.set_south(field_x)
field_d.set_west(field_s)

field_s.set_north(field_w)
field_s.set_east(field_d)
field_s.set_south(field_y)
field_s.set_west(field_a)

field_a.set_north(field_q)
field_a.set_east(field_s)
field_a.set_south(field_y)

field_smallerAs.set_east(field_y)
field_smallerAs.set_south(field_exit)

field_y.set_north(field_a)
field_y.set_east(field_x)
field_y.set_west(field_smallerAs)
field_y.set_south(field_exit)

field_x.set_north(field_d)
field_x.set_east(field_c)
field_x.set_south(field_shift)
field_x.set_west(field_y)

field_c.set_north(field_f)
field_c.set_east(field_v)
field_c.set_south(field_shift)
field_c.set_west(field_x)

field_v.set_north(field_g)
field_v.set_east(field_b)
field_v.set_south(field_space)
field_v.set_west(field_c)

field_b.set_north(field_h)
field_b.set_east(field_n)
field_b.set_south(field_space)
field_b.set_west(field_v)

field_n.set_north(field_k)
field_n.set_east(field_m)
field_n.set_south(field_space)
field_n.set_west(field_b)

field_m.set_north(field_l)
field_m.set_east(field_comma)
field_m.set_south(field_altGr)
field_m.set_west(field_n)

field_comma.set_north(field_oe)
field_comma.set_east(field_dot)
field_comma.set_south(field_altGr)
field_comma.set_west(field_m)

field_dot.set_north(field_ae)
field_dot.set_east(field_hyphen)
field_dot.set_west(field_comma)

field_hyphen.set_north(field_hashtag)
field_hyphen.set_west(field_dot)

field_altGr.set_north(field_m)
field_altGr.set_west(field_space)

field_space.set_north(field_b)
field_space.set_east(field_altGr)
field_space.set_west(field_shift)

field_shift.set_north(field_c)
field_shift.set_east(field_space)
field_shift.set_west(field_exit)

field_send.set_south(field_back)

field_exit.set_north(field_smallerAs)
field_exit.set_east(field_shift)

## Passchecker / E-MailChecker Menue
Passchecker_menue = Menue("passchecker menue")

tastatur = [field_space, field_altGr, field_shift, field_hyphen, field_dot, field_comma, field_m, field_n, field_b, field_v,
                  field_c, field_x, field_y, field_z, field_smallerAs, field_hashtag, field_ae, field_oe, field_l, field_k, field_j,
                  field_h, field_g, field_f, field_d, field_s, field_a, field_plus, field_ue, field_p, field_o, field_i, field_u, field_z,
                  field_t, field_r, field_e, field_w, field_q, field_back, field_apostroph, field_sz, field_0, field_9, field_8,
                  field_7, field_6, field_5, field_4, field_3, field_2, field_1, field_zirkunflex, field_send, field_exit]

Passchecker_menue.set_feldarray(tastatur)
Passchecker_menue.set_current_field(field_1)

## menue marv
field_passchecker = Field("passchecker")
field_passchecker.set_XY_0(231, 75)
field_passchecker.set_XY_1(163, 46)

field_emailchecker = Field("baustelle")
field_emailchecker.set_XY_0(106, 75)
field_emailchecker.set_XY_1(37, 46)

field_main_back = Field("exit")
field_main_back.set_XY_0(245, 12)
field_main_back.set_XY_1(222, 4)

field_passchecker.set_east(field_emailchecker)
field_passchecker.set_south(field_main_back)
field_main_back.set_north(field_passchecker)
field_emailchecker.set_west(field_passchecker)

Marv_menue = Menue("marv menue")

felder = [field_passchecker, field_emailchecker, field_main_back]

Marv_menue.set_feldarray(felder)
Marv_menue.set_current_field(field_passchecker)


# Verzeichnisse für Bilder und Bibliotheken festlegen
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

# Schriftart einrichten
# Schriftart für die Texte auf dem Display laden
font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 8)

# GPIO-Buttons initialisieren
# Konfiguration der GPIO-Pins für die Buttons
btn_links = gpiozero.Button(19)
btn_rechts = gpiozero.Button(20)
btn_oben = gpiozero.Button(16)
btn_unten = gpiozero.Button(26)
btn_a = gpiozero.Button(6)
btn_b = gpiozero.Button(12)

# Aktuelles Menü initialisieren
# Setzt das aktuelle Menü auf 'Marv_menue'
current_menue = Marv_menue

# oldRect und Passwort initialisieren
oldRect = None
password = ""

def keyboard_uppercase():
    """
    Setzt die Namen der Felder auf ihre entsprechenden Zeichen im Großbuchstaben- und
    Symbolmodus der Tastatur.
    """
    field_zirkunflex.set_name("°")
    field_1.set_name("!")
    field_2.set_name("\"\"")
    field_3.set_name("§")
    field_4.set_name("$")
    field_5.set_name("%")
    field_6.set_name("&")
    field_7.set_name("/")
    field_8.set_name("(")
    field_9.set_name(")")
    field_0.set_name("=")
    field_sz.set_name("?")
    field_apostroph.set_name("`")
    field_q.set_name("Q")
    field_w.set_name("W")
    field_e.set_name("E")
    field_r.set_name("R")
    field_t.set_name("T")
    field_z.set_name("Z")
    field_u.set_name("U")
    field_i.set_name("I")
    field_o.set_name("O")
    field_p.set_name("P")
    field_ue.set_name("Ü")
    field_plus.set_name("*")
    field_a.set_name("A")
    field_s.set_name("S")
    field_d.set_name("D")
    field_f.set_name("F")
    field_g.set_name("G")
    field_h.set_name("H")
    field_j.set_name("J")
    field_k.set_name("K")
    field_l.set_name("L")
    field_oe.set_name("Ö")
    field_ae.set_name("Ä")
    field_hashtag.set_name("'")
    field_smallerAs.set_name(">")
    field_y.set_name("Y")
    field_x.set_name("X")
    field_c.set_name("C")
    field_v.set_name("V")
    field_b.set_name("B")
    field_n.set_name("N")
    field_m.set_name("M")
    field_comma.set_name(";")
    field_dot.set_name(":")
    field_hyphen.set_name("_")

def keyboard_lowercase():
    """
    Setzt die Namen der Felder auf ihre entsprechenden Zeichen im Kleinbuchstaben- und
    Symbolmodus der Tastatur.
    """
    field_zirkunflex.set_name("^")
    field_1.set_name("1")
    field_2.set_name("2")
    field_3.set_name("3")
    field_4.set_name("4")
    field_5.set_name("5")
    field_6.set_name("6")
    field_7.set_name("7")
    field_8.set_name("8")
    field_9.set_name("9")
    field_0.set_name("0")
    field_sz.set_name("ß")
    field_apostroph.set_name("´")
    field_q.set_name("q")
    field_w.set_name("w")
    field_e.set_name("e")
    field_r.set_name("r")
    field_t.set_name("t")
    field_z.set_name("z")
    field_u.set_name("u")
    field_i.set_name("i")
    field_o.set_name("o")
    field_p.set_name("p")
    field_ue.set_name("ü")
    field_plus.set_name("+")
    field_a.set_name("a")
    field_s.set_name("s")
    field_d.set_name("d")
    field_f.set_name("f")
    field_g.set_name("g")
    field_h.set_name("h")
    field_j.set_name("j")
    field_k.set_name("k")
    field_l.set_name("l")
    field_oe.set_name("ö")
    field_ae.set_name("ä")
    field_hashtag.set_name("#")
    field_smallerAs.set_name("<")
    field_y.set_name("y")
    field_x.set_name("x")
    field_c.set_name("c")
    field_v.set_name("v")
    field_b.set_name("b")
    field_n.set_name("n")
    field_m.set_name("m")
    field_comma.set_name(",")
    field_dot.set_name(".")
    field_hyphen.set_name("-")

def keyboard_altGr():
    """
    Setzt die Namen der Felder auf ihre entsprechenden Zeichen im AltGr-Modus der Tastatur,
    der zusätzliche Sonderzeichen und Symbole bereitstellt.
    """
    field_1.set_name("¹")
    field_2.set_name("²")
    field_3.set_name("³")
    field_4.set_name("¼")
    field_5.set_name("½")
    field_6.set_name("¬")
    field_7.set_name("{")
    field_8.set_name("[")
    field_9.set_name("]")
    field_0.set_name("}")
    field_sz.set_name("\\")
    field_q.set_name("@")
    field_r.set_name("¶")
    field_o.set_name("ø")
    field_p.set_name("þ")
    field_ue.set_name("¨")
    field_plus.set_name("~")
    field_a.set_name("æ")
    field_d.set_name("ð")
    field_j.set_name(".")
    field_smallerAs.set_name("|")
    field_y.set_name("»")
    field_x.set_name("«")
    field_c.set_name("¢")

def draw_marv_menue():
    """
    Zeichnet das Menü für Marv. Aktualisiert das aktuelle Feld und rotiert das Bild zweimal um 180 Grad.
    Zeichnet Text und Rechtecke auf die Felder.
    """
    global image, draw

    # Zeichne das aktuelle Feld hervor
    draw_currentField(Marv_menue.current_field)

    # Drehe das Bild um 180 Grad und aktualisiere das Zeichenobjekt
    image = image.rotate(180, expand=True)
    draw = ImageDraw.Draw(image)

    # Zeichne den Text für jedes Feld
    for i in felder:
        # Zeiche den Text an die richtige position
        text_x = (250 - i.x_0+1)
        text_y = (122 - i.y_0-1)
        draw.text((text_x, text_y), i.name, font=font15, fill=0)

    # Drehe das Bild erneut um 180 Grad und aktualisiere das Zeichenobjekt
    image = image.rotate(180, expand=True)  # Rotate the image
    draw = ImageDraw.Draw(image)

    # Zeichne die Rechtecke und den Text für jedes Feld
    for i in felder:
        draw.rectangle([(i.x_0, i.y_0), (i.x_1, i.y_1)], outline=0, width=1)

def draw_currentField(field):
    """
    Zeichnet das aktuelle Feld. Entfernt die Hervorhebung vom vorherigen Feld und zeichnet
    das neue aktuelle Feld hervor.
    
    Parameter:
    field (Field): Das aktuelle Feld, das hervorgehoben werden soll.
    """
    global draw, image, oldRect

    # Entferne die Hervorhebung vom vorherigen Feld, falls vorhanden
    if(oldRect is not None):
        draw.rectangle([(oldRect.x_0, oldRect.y_0), (oldRect.x_1, oldRect.y_1)], outline=0, width=1)
    
    # Aktualisiere oldRect auf das aktuelle Feld
    oldRect = field

    # Zeichne das neue aktuelle Feld
    draw.rectangle([(field.x_0, field.y_0), (field.x_1, field.y_1)], outline=255, width=1)

    # Aktualisiere das Display teilweise, um das neue Feld hervorzuheben
    epd.displayPartial(epd.getbuffer(image))

def draw_password():
    """
    Zeichnet das Passwort auf das Bild. Löscht den Bereich, in dem das Passwort gezeichnet wird,
    und rotiert das Bild zweimal um 180 Grad, um den Text zu zeichnen.
    """
    global password, draw, image

    # Berechne die Textposition für das Passwort
    text_x = (250 - 208 +1)
    text_y = (122 - 96 -1)

    # Lösche den Bereich, in dem das Passwort gezeichnet wird
    draw.rectangle([(207, 95),(42, 85)], fill=255)

    # Drehe das Bild um 180 Grad und aktualisiere das Zeichenobjekt
    image = image.rotate(180, expand=True)
    draw = ImageDraw.Draw(image)

    # Zeichne das Passwort
    draw.text([text_x, text_y], password)

    # Drehe das Bild erneut um 180 Grad und aktualisiere das Zeichenobjekt
    image = image.rotate(180, expand=True)
    draw = ImageDraw.Draw(image)

    # Aktualisiere das Display teilweise, um das gezeichnete Passwort anzuzeigen
    epd.displayPartial(epd.getbuffer(image))

def draw_result(result):
    """
    Zeichnet das result auf das Bild. Löscht den Bereich, in dem das result gezeichnet wird,
    und rotiert das Bild zweimal um 180 Grad, um den Text zu zeichnen.
    """
    global password, draw, image

    # Berechne die Textposition für das Passwort
    text_x = (250 - 208 +1)
    text_y = (140 - 96 -1)

    # Lösche den Bereich, in dem das Ergebnis gezeichnet wird
    draw.rectangle([(207, 83),(10, 64)], fill=255)

    # Drehe das Bild um 180 Grad und aktualisiere das Zeichenobjekt
    image = image.rotate(180, expand=True)
    draw = ImageDraw.Draw(image)

    # Zeichne das Ergebnis
    draw.text([text_x, text_y], result)

    # Drehe das Bild erneut um 180 Grad und aktualisiere das Zeichenobjekt
    image = image.rotate(180, expand=True)
    draw = ImageDraw.Draw(image)

    # Aktualisiere das Display teilweise, um das gezeichnete Passwort anzuzeigen
    epd.displayPartial(epd.getbuffer(image))

def press_logic(num):
    """
    Verarbeitet die Logik, wenn ein Button gedrückt wird.
    
    Parameter:
    num (int): Die Nummer des gedrückten Buttons.
    """
    global password, current_menue, oldRect

    # Überprüfe, ob das aktuelle Menü das "marv menue" ist
    if(current_menue.name == "marv menue"):
        # Bewegung nach Norden
        if num == 0:
            if(Marv_menue.current_field.north is not None):
                Marv_menue.current_field = Marv_menue.current_field.north
                draw_currentField(Marv_menue.current_field)
        # Bewegung nach Osten
        elif num == 1:
            if(Marv_menue.current_field.east is not None):
                Marv_menue.current_field = Marv_menue.current_field.east
                draw_currentField(Marv_menue.current_field)
        # Bewegung nach Süden
        elif num == 2:
            if(Marv_menue.current_field.south is not None):
                Marv_menue.current_field = Marv_menue.current_field.south
                draw_currentField(Marv_menue.current_field)
        # Bewegung nach Westen
        elif num == 3:
            if(Marv_menue.current_field.west is not None):
                Marv_menue.current_field = Marv_menue.current_field.west
                draw_currentField(Marv_menue.current_field)

        # Auswahl bestätigen
        elif num == 4:
            if(Marv_menue.current_field.name == "passchecker"):
                draw.rectangle([(250, 122), (0, 0)], outline=255, fill=255)
                draw.rectangle([(208, 96), 41, 84], outline=0, width=1)
                draw_keyboard()
                oldRect = None
                current_menue = Passchecker_menue

            elif(Marv_menue.current_field.name == "baustelle"):
                ## TODO: Emailchecker mit HaveIbeenPwned API (4Euro monatlich bruh)
                pass

            elif(Marv_menue.current_field.name == "exit"):
                sys.exit()
        elif num == 5:
            ## Zurück ins Hauptmenü
            sys.exit()
    
    # Überprüfe, ob das aktuelle Menü das "passchecker menue" ist
    elif(current_menue.name == "passchecker menue"):
        # Bewegung nach Norden
        if num == 0:
            if(Passchecker_menue.current_field.north is not None):
                Passchecker_menue.current_field = Passchecker_menue.current_field.north
                draw_currentField(Passchecker_menue.current_field)
        # Bewegung nach Osten
        elif num == 1:
            if(Passchecker_menue.current_field.east is not None):
                Passchecker_menue.current_field = Passchecker_menue.current_field.east
                draw_currentField(Passchecker_menue.current_field)
        # Bewegung nach Süden
        elif num == 2:
            if(Passchecker_menue.current_field.south is not None):
                Passchecker_menue.current_field = Passchecker_menue.current_field.south
                draw_currentField(Passchecker_menue.current_field)
        # Bewegung nach Westen
        elif num == 3:
            if(Passchecker_menue.current_field.west is not None):
                Passchecker_menue.current_field = Passchecker_menue.current_field.west
                draw_currentField(Passchecker_menue.current_field)
        # Auswahl bestätigen oder spezielle Tasten verarbeiten
        elif num == 4:
            if(Passchecker_menue.current_field.name == "Shift"):
                if(Passchecker_menue.field_array[3].name == "-"):
                    keyboard_uppercase()
                    draw_keyboard()
                    draw_currentField(Passchecker_menue.current_field)
                    draw_password()
                else:
                    keyboard_lowercase()
                    draw_keyboard()
                    draw_password()
            elif(Passchecker_menue.current_field.name == "Alt Gr"):
                if(Passchecker_menue.field_array[38].name == "@"):
                    keyboard_lowercase()
                    draw_keyboard()
                    draw_currentField(Passchecker_menue.current_field)
                    draw_password()
                else:
                    keyboard_altGr()
                    draw_keyboard()
                    draw_currentField(Passchecker_menue.current_field)
                    draw_password()
            elif(Passchecker_menue.current_field.name == "back"):
                if(len(password) > 0):
                    password = password[0:-1]
                    draw_password()
            elif(Passchecker_menue.current_field.name == "exit"):
                current_menue = Marv_menue
                password = ""
                draw.rectangle([(250, 122), (0, 0)], outline=255, fill=255)
                draw_marv_menue()
                oldRect = None
                Marv_menue.current_field = field_passchecker
                draw_currentField(Marv_menue.current_field)
            elif(Passchecker_menue.current_field.name == "send"):
                ergebnis = check_password(password)
                draw_result(ergebnis)
                print(ergebnis)
            else:
                password += Passchecker_menue.current_field.name
                draw_password()
        # Rücktaste drücken
        elif num == 5:
            if(len(password) > 0):
                    password = password[0:-1]
                    draw_password()
                    

def draw_keyboard():
    """
    Zeichnet die aktuelle Tastatur. Löscht den Bereich, in dem die Tastatur gezeichnet wird,
    und rotiert das Bild zweimal um 180 Grad, um den Text und die Rechtecke zu zeichnen.
    """
    global draw, image
    # Lösche den Bereich, in dem die Tastatur gezeichnet wird
    draw.rectangle([(250, 65),(0, 0)], outline=255, fill=255)

    # Drehe das Bild um 180 Grad und aktualisiere das Zeichenobjekt
    image = image.rotate(180, expand=True)
    draw = ImageDraw.Draw(image)

    # Zeichne den Text für jede Taste in der Tastatur
    for i in Passchecker_menue.field_array:
        # Berechne die Textposition
        text_x = (250 - i.x_0+1)
        text_y = (122 - i.y_0-1)
        draw.text((text_x, text_y), i.name, font=font15, fill=0)

    # Drehe das Bild erneut um 180 Grad und aktualisiere das Zeichenobjekt
    image = image.rotate(180, expand=True)
    draw = ImageDraw.Draw(image)

    # Zeichne die Rechtecke für jede Taste in der kleinen Tastatur
    for i in Passchecker_menue.field_array:
        draw.rectangle([(i.x_0, i.y_0), (i.x_1, i.y_1)], outline=0, width=1)

    # Aktualisiere das Display teilweise, um die gezeichnete Tastatur anzuzeigen
    epd.displayPartial(epd.getbuffer(image))

def password_strength(password):
    """
    Bewertet die Stärke eines Passworts basierend auf verschiedenen Kriterien:
    Länge, Großbuchstaben, Kleinbuchstaben, Zahlen und Sonderzeichen.
    
    Parameter:
    password (str): Das zu bewertende Passwort.
    
    Rückgabe:
    int: Punktzahl, die die Stärke des Passworts repräsentiert.
    """
    points = 0

    # Länge des Passworts
    if len(password) >= 8:
        points += 1
    if len(password) >= 12:
        points += 1

    # Enthält Großbuchstaben
    if re.search(r'[A-Z]', password):
        points += 1

    # Enthält Kleinbuchstaben
    if re.search(r'[a-z]', password):
        points += 1

    # Enthält Zahlen
    if re.search(r'[0-9]', password):
        points += 1

    # Enthält Sonderzeichen
    if re.search(r'[\W_]', password):
        points += 1

    return points

def check_rockyou(password, rockyou_path="rockyou.txt"):
    try:
        with open(rockyou_path, 'r', encoding='latin-1') as file:
            for line in file:
                if line.strip() == password:
                    return True
        return False
    except FileNotFoundError:
        print(f"Die Datei {rockyou_path} wurde nicht gefunden.")
        return False

def add_to_list(password, pwdPath="pwd.txt"):
    """
    Fügt ein Passwort zur RockYou-Liste hinzu, falls es nicht bereits vorhanden ist.
    
    Parameter:
    password (str): Das hinzuzufügende Passwort.
    rockyou_path (str): Pfad zur RockYou-Datei.
    """
    try:
        with open(pwdPath, 'a', encoding='latin-1') as file:
            file.write(password + '\n')
    except Exception as e:
        print(f"Fehler beim Schreiben in die Datei {pwdPath}: {e}")

def check_password(password, rockyou_path="rockyou.txt"):
    """
    Überprüft ein Passwort auf seine Stärke und ob es in der RockYou-Liste enthalten ist.
    Falls das Passwort nicht in der RockYou-Liste enthalten ist, wird es hinzugefügt.
    
    Parameter:
    password (str): Das zu überprüfende Passwort.
    rockyou_path (str): Pfad zur RockYou-Datei.
    
    Rückgabe:
    str: Bewertung des Passworts ('Schwach', 'Mittel', 'Stark' oder 'Schwach (in der RockYou-Liste)').
    """
    if check_rockyou(password, rockyou_path):
        return "Schwach (in der RockYou-Liste)"

    add_to_list(password)
    strength = password_strength(password)
    if strength <= 2:
        return "Schwach"
    elif strength == 3 or 4:
        return "Mittel"
    else:
        return "Stark"


# Ereignisbehandlung für die GPIO-Buttons einrichten
# Wenn die Buttons gedrückt werden, wird die entsprechende Funktion mit einem Parameter aufgerufen
btn_links.when_pressed = lambda: press_logic(3)
btn_rechts.when_pressed = lambda: press_logic(1)
btn_unten.when_pressed = lambda: press_logic(2)
btn_oben.when_pressed = lambda: press_logic(0)
btn_a.when_pressed = lambda: press_logic(4)
btn_b.when_pressed = lambda: press_logic(5)


# Display setup
try:
    # Initialisiere das E-Paper-Display
    epd = epd2in13_V4.EPD()
    epd.init_fast()  # Schnelle Initialisierung des Displays
    epd.Clear(0xFF)  # Bildschirm löschen (mit weißem Hintergrund)

    # Bildsetup
    # Erstelle ein neues Bild mit den Dimensionen des Displays und einem weißen Hintergrund
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)  # Zeichnen-Objekt initialisieren
    draw_currentField(Marv_menue.current_field)  # Zeichne das aktuelle Feld

    draw_marv_menue()  # Zeichne das Marv-Menü

    # Zeichne das Bild auf dem Bildschirm
    epd.displayPartBaseImage(epd.getbuffer(image))
    pause()  # Halte den Prozess an
    epd.sleep()  # Versetze das Display in den Schlafmodus

except IOError as e:
    # Fehlerbehandlung bei Ein-/Ausgabefehlern
    logging.info(e)

except KeyboardInterrupt:
    # Fehlerbehandlung bei manueller Unterbrechung (Ctrl + C)
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)  # Modul-Exit aufrufen und aufräumen
    exit()  # Programm beenden