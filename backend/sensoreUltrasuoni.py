import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False) # accendo il sensore
time.sleep(2)

def leggiDati():
    try:
        ID = "sensoreUltrasuoni"
        eleDict = {}
        GPIO.output(TRIG, True)
        time.sleep(0.5) # invio del segnale
        GPIO.output(TRIG, False)

        while(GPIO.input(ECHO) == 0):
            pulse_start = time.time()

        while(GPIO.input(ECHO) == 1):
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)
        #riduco la distanza massima di rilevamento a 25cm
        if distance <= 25: ele = f"Rilevato qualcosa {datetime.now().strftime('%H:%M:%S')}."
        else: ele = "ND"
    except Exception as e: ele = (f"Errore durante la lettura: {e}")
    eleDict = {"sensorID": f'{ID}', "data": f'{ele}'}
    return eleDict
