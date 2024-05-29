import asyncio
import websockets
import json
from datetime import datetime
from sensoreUltrasuoni import leggiDati as leggiDatiSU
from sensoreMagnetico import leggiDati as leggiDatiSM


jsonFilePath = "config.json"
print("Avviando il server...")
async def server(websocket, path):
    try:
        def readJson():
            with open(jsonFilePath, "r", encoding='utf-8') as f: config = json.load(f)
            return config

        def dumpJson(obj):
            with open(jsonFilePath, 'w', encoding='utf-8') as f: json.dump(obj, f, ensure_ascii=False) 

        def differenza(i, f):
            diff = int(f.replace(":",""))-int(i.replace(":",""))
            print(f"Differenza: {diff}")
            return diff

        def timeNow():
            return datetime.now().strftime('%H:%M:%S')

        print("Connessione con il client eseguita")
        status = readJson()["status"]
        startMessage = {"ID": 'start', "allarmStatus": f'{status}'}
        print(f"SENDING: {startMessage}")
        #print(f"allarm: {allarm}, type: {type(allarm)}")
        await websocket.send(json.dumps(startMessage))
        #await websocket.send(json.dumps({"sensorID": 'clientConnected', "data": 'Nessuna intrusione', "time": f"{datetime.now().strftime('%H:%M:%S')}"}))
        end = timeNow()

        while True:
            # Legge i dati del sensore ultrasuoni
            datiSU = leggiDatiSU()
            datiSM = leggiDatiSM()
            start = timeNow()

            # Invia i dati al client tramite WebSocket se sono diversi da ND (no data)
            if(status):
                toSend = {}
                if(datiSU['intrusion']==True or datiSM['intrusion']==True):
                    if datiSU['intrusion']==True: toSend.append(datiSU['name'])
                    if datiSM['intrusion']==True: toSend.append(datiSM['name'])
                if(differenza(end, start)>=5):
                    toSend.append("noIntrusion")
                print(f"[DEBUG] - DIFFERENZA: {differenza(end, start)} - INIZIO FINE: {start} {end} - SU: {datiSU['intrusion']} - SM:{datiSM['intrusion']} - STATUS {status}")
                await websocket.send(json.dumps(toSend))
                end = timeNow()
                #print(f"SENDING: {datiSU}")
                #print(f"SENDING: {datiSM}")
            await asyncio.sleep(1)  # Aggiorna i dati ogni secondo
    except Exception as e: print(f"Errore: {e}")

start_server = websockets.serve(server, '192.168.1.155', 8765)
print("Server avviato")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
