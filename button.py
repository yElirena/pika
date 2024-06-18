from gpiozero import Button
from signal import pause
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

tb = TonalBuzzer(5)

def sb1():
    print("Goodbye 16 oben!")
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


button1 = Button(16)
button2 = Button(19)
button3 = Button(20)
button4 = Button(26)
button5 = Button(6)
button6 = Button(12)

button1.when_pressed = sb1

button2.when_pressed = sb2
button3.when_pressed = sb3
button4.when_pressed = sb4
button5.when_pressed = sb5
button6.when_pressed = sb6
pause()
