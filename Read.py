
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
while True:
        


        id, text = reader.read()
        if isinstance(id, int):
            print(id)

        #print(text)
#finally:
 #       GPIO.cleanup()