from threading import Thread
from time import sleep

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
def rfidScaner():
    while True:
        id, text = reader.read()
        print(id)
def testSecondFunction():
    while True:
        for i in range(255):
            print(f"out from test func {i}")
            sleep(0.5)
        
rfidThread = Thread(target=rfidScaner)
backThread = Thread(target=testSecondFunction)
rfidThread.start()
backThread.start()

print("app stop")



            

