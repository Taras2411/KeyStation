MagPin1 = 21
MagPin2 = 20
BiperPin = 26
timeToGetKey = 15
rooms_to_pins = {
    '44': 21,
    '45': 20,
    '46': 16
    }
rooms_to_leds = {
    '44':0,
    '45':1,
    '46':2
    }

from threading import Thread
from time import sleep
import mysql.connector 
import os
import time
import board
import neopixel

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
trueStartTime = time.time()
pixel_pin = board.D18
num_pixels = 3
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)



mydb = mysql.connector.connect(
    host="localhost",
    port='3306',
    user="admin",
    password=os.environ['DBPASSWORD'],
    #password= 'ilovetea',
    database="key_station")
    
mycursor = mydb.cursor()



GPIO.setmode(GPIO.BCM)      
GPIO.setup(MagPin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MagPin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for i in rooms_to_pins:
    GPIO.setup(rooms_to_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print(f"{rooms_to_pins[i]} inited!")

GPIO.setup(BiperPin, GPIO.OUT)

GPIO.setwarnings(False)
reader = SimpleMFRC522()
LastCardCode = ''
LastDetectTime = 0
def biper():
    while True:
        GPIO.output(BiperPin, 1)
        sleep(1)
        GPIO.output(BiperPin, 0)
        sleep(1)
def bipOnce():
        GPIO.output(BiperPin, 1)
        sleep(0.5)
        GPIO.output(BiperPin, 0)
def bipTwice():
        for i in range(2):
            GPIO.output(BiperPin, 1)
            sleep(0.5)
            GPIO.output(BiperPin, 0)
            sleep(0.5)
def bipThrice():
        for i in range(3):
            GPIO.output(BiperPin, 1)
            sleep(0.5)
            GPIO.output(BiperPin, 0)
            sleep(0.5)
    

def rfidScaner():
    
    while True:
        
        id, text = reader.read()
        #pixels.fill((0,0,0))
        global LastCardCode
        global LastDetectTime
        LastCardCode = id
        LastDetectTime = TimeFromStart()
        
        print("DETECTED")
        bipOnce()
        #print(id)
        #temp = str(id)
        #roomsAndEnGet = f"SELECT Name,Teachers.en,Cards.en,FIO FROM key_station.Keys JOIN key_station.TeachersToKeys ON key_station.Keys.id = key_station.TeachersToKeys.KeyId JOIN key_station.Teachers ON key_station.Teachers.id = key_station.TeachersToKeys.TeacherId JOIN key_station.Cards ON key_station.Cards.TeacherId = key_station.Teachers.id WHERE Card IN ('{temp}')"
        #mycursor.execute(roomsAndEnGet)
        #restuple = mycursor.fetchall()
        #for i in restuple:
        #   roomnum = i[0]
        #    rooms_to_leds[roomnum]
        #    pixels[rooms_to_leds[roomnum]]=((0, 255, 0))
        #sleep(timeToGetKey)
        #pixels.fill((0,0,0))
        #bipTwice()
        
        
def testSecondFunction():
        print(readMagState(rooms_to_pins))
        print(readMagState(rooms_to_pins)["44"])

        
def readMagState(names_to_pins):
    names_to_status = {}
    for name in names_to_pins:
        names_to_status[name] = GPIO.input(names_to_pins[name])
    return names_to_status

rfidThread = Thread(target=rfidScaner)
bipThread = Thread(target=biper)


def WinDef():
    prevPinState =  readMagState(rooms_to_pins)
    while True:
        
        ###LED IND START
        
        pixels.fill((0,0,0))
        if TimeFromStart()- LastDetectTime < timeToGetKey:
            
            temp = str(LastCardCode)
            roomsAndEnGet = f"SELECT Name,Teachers.en,Cards.en,FIO FROM key_station.Keys JOIN key_station.TeachersToKeys ON key_station.Keys.id = key_station.TeachersToKeys.KeyId JOIN key_station.Teachers ON key_station.Teachers.id = key_station.TeachersToKeys.TeacherId JOIN key_station.Cards ON key_station.Cards.TeacherId = key_station.Teachers.id WHERE Card IN ('{temp}')"
            mycursor.execute(roomsAndEnGet)
            restuple = mycursor.fetchall()
            for i in rooms_to_leds:
               for z in restuple:
                   if i in z:
                       pixels[rooms_to_leds[i]]=((0, 255, 0))
                   #else:
                       #pixels[rooms_to_leds[i]]=((0, 0, 0))
            
            num = 0

        else:
            pixels.fill((0,0,0))
            pixels.show()
        
        
    ###LED IND END
        sleep(0.1)
        lastPinState = readMagState(rooms_to_pins)
        print(readMagState(rooms_to_pins))
        if readMagState(rooms_to_pins) != prevPinState:
            print(f"ALARM! DIF DETECT last: {readMagState(rooms_to_pins)} prev: {prevPinState}")
            
            if TimeFromStart()- LastDetectTime < timeToGetKey:
                print(TimeFromStart()- LastDetectTime)
                print("You have some time!")
                print("is dif:")
                ErrFlag = 0
                ErrList = []
                for i in lastPinState:
                    if lastPinState[i] != prevPinState[i]:
                        print(f'key {i} with value {lastPinState[i]} != {prevPinState[i]} from cycle begin')
                        ErrFlag += 1
                        ErrList.append(i)
                print(f'number of errs:{ErrFlag}')
                print(f'list or errs:{ErrList}')
                temp = str(LastCardCode)
                roomsAndEnGet = f"SELECT Name,Teachers.en,Cards.en,FIO FROM key_station.Keys JOIN key_station.TeachersToKeys ON key_station.Keys.id = key_station.TeachersToKeys.KeyId JOIN key_station.Teachers ON key_station.Teachers.id = key_station.TeachersToKeys.TeacherId JOIN key_station.Cards ON key_station.Cards.TeacherId = key_station.Teachers.id WHERE Card IN ('{temp}')"
                mycursor.execute(roomsAndEnGet)
                response = mycursor.fetchall()
                for y in ErrList:
                    for z in response:
                        if y == z[0]:
                            print("permision is ok!")
                            ErrFlag -= 1
                            ErrList.remove(y)
                print(f'final err count is {ErrList}')
                for i in ErrList:
                    pixels[rooms_to_leds[i]] = ((255,0,0))

                
                if len(ErrList) == 0 :
                    print("ALL IS GOOD")
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    print(prevPinState)
                    prevPinState =  readMagState(rooms_to_pins)
                    print(prevPinState)
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    
                    
                    
                    
                else:
                    pixels.show()
                    bipThrice()
                    print(f'final err count is {ErrList}')
                    
            else:
                print('time is out ')
                pixels.show()
                bipThrice()
        pixels.show()
    print("FUNC STOP")
    
    
def LedIndication():
    pixels.fill((0,0,0))
    pixels.show()
    while True:
        pixels.fill((0,0,0))
        if TimeFromStart()- LastDetectTime < timeToGetKey:
            
            temp = str(LastCardCode)
            roomsAndEnGet = f"SELECT Name,Teachers.en,Cards.en,FIO FROM key_station.Keys JOIN key_station.TeachersToKeys ON key_station.Keys.id = key_station.TeachersToKeys.KeyId JOIN key_station.Teachers ON key_station.Teachers.id = key_station.TeachersToKeys.TeacherId JOIN key_station.Cards ON key_station.Cards.TeacherId = key_station.Teachers.id WHERE Card IN ('{temp}')"
            mycursor.execute(roomsAndEnGet)
            restuple = mycursor.fetchall()
            for i in rooms_to_leds:
               for z in restuple:
                   if i in z:
                       pixels[rooms_to_leds[i]]=((0, 255, 0))
                   #else:
                       #pixels[rooms_to_leds[i]]=((0, 0, 0))
            pixels.show()
            num = 0

        else:
            pixels.fill((0,0,0))
            pixels.show()
    
    
    
def TimeFromStart():
    ret = time.time()- trueStartTime
    return ret


#backThread = Thread(target=testSecondFunction)
WinDefThread = Thread(target=WinDef)
WinDefThread.start()
rfidThread.start()
LedIndicationThread = Thread(target=LedIndication)
#LedIndicationThread.start()
#bipThread.start()
#backThread.start()