import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN)
print(GPIO.input(14))
GPIO.cleanup()