MagPin1 = 21
MagPin2 = 20
rooms_to_pins = {
    '44': 21,
    '45': 20
    }
from threading import Thread
from time import sleep
import mysql.connector 
import os

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

mydb = mysql.connector.connect(
    host="localhost",
    port='3306',
    user="admin",
    password=os.environ['DBPASSWORD'],
    database="key_station")
    
mycursor = mydb.cursor()



GPIO.setmode(GPIO.BCM)      
GPIO.setup(MagPin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MagPin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
reader = SimpleMFRC522()


def rfidScaner():
    while True:
        id, text = reader.read()
        #print(id)
        temp = str(id)
        roomsAndEnGet = f"SELECT Name,Teachers.en,Cards.en,FIO FROM key_station.Keys JOIN key_station.TeachersToKeys ON key_station.Keys.id = key_station.TeachersToKeys.KeyId JOIN key_station.Teachers ON key_station.Teachers.id = key_station.TeachersToKeys.TeacherId JOIN key_station.Cards ON key_station.Cards.TeacherId = key_station.Teachers.id WHERE Card IN ('{temp}')"
        mycursor.execute(roomsAndEnGet)
        restuple = mycursor.fetchall()
        print(restuple)
        
        
def testSecondFunction():
        print(readMagState(rooms_to_pins))
        print(readMagState(rooms_to_pins)["44"])

        
def readMagState(names_to_pins):
    names_to_status = {}
    for name in names_to_pins:
        names_to_status[name] = GPIO.input(names_to_pins[name])
    return names_to_status

rfidThread = Thread(target=rfidScaner)
#backThread = Thread(target=testSecondFunction)
rfidThread.start()
#backThread.start()