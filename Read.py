MagPin1 = 21
MagPin2 = 20
rooms_to_pins = {
    '44': 21,
    '45': 20
    }
from threading import Thread
from time import sleep

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
GPIO.setmode(GPIO.BCM)      
GPIO.setup(MagPin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MagPin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
reader = SimpleMFRC522()
def rfidScaner():
    while True:
        id, text = reader.read()
        print(id)
def testSecondFunction():
        print(readMagState(rooms_to_pins))
        print(readMagState(rooms_to_pins)["44"])

        
def readMagState(names_to_pins):
    names_to_status = {}
    for name in names_to_pins:
        names_to_status[name] = GPIO.input(names_to_pins[name])
    return names_to_status

rfidThread = Thread(target=rfidScaner)
backThread = Thread(target=testSecondFunction)
rfidThread.start()
backThread.start()





            

