import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False) # accendo il sensore
time.sleep(2)

def leggiDati():
    try:
        while(True):
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
            if distance >= 20: ele = "Rilevato qualcosa"
            else: ele = "Nessun rilevamento"
    except Exception as e: ele = (f"Errore durante la lettura: {e}")
    print(ele)
    return ele


