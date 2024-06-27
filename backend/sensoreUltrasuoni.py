import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT) #trig
GPIO.setup(24, GPIO.IN) #echo

GPIO.output(23, False) # accendo il sensore
time.sleep(2)

def leggiDati():
    try:
        #ID = "USensor"
        data = {}
        GPIO.output(23, True)
        time.sleep(0.5) # invio del segnale
        GPIO.output(23, False)

        while(GPIO.input(24) == 0):
            pulse_start = time.time()

        while(GPIO.input(24) == 1):
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)
        #riduco la distanza massima di rilevamento a 25cm
        if distance <= 25: isIntrusion = True
        else: isIntrusion = False
        mex = ""
    except Exception as e: mex = (f"Errore durante la lettura: {e}")
    data = {"ID": 'USensor', "name": 'USensor', "intrusion": isIntrusion, "mex": f'{mex}'}
    return data
