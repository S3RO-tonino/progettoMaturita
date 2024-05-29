import RPi.GPIO as gp
from datetime import datetime

gp.setmode(gp.BCM)

gp.setup(17, gp.IN)

def leggiDati():
    try:
        eleDict = {}
        if gp.input(17): isIntrusion = True
        else: isIntrusion = False
        ele = ""
    except Exception as e: ele=(f"errore: {e}")

    eleDict = {"ID": 'MSensor', "name": 'Sensore magnetico', "intrusion": {isIntrusion}, "data": f'{ele}', "time": f"{datetime.now().strftime('%H:%M:%S')}"}
    return eleDict
