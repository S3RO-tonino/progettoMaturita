import asyncio
import websockets
import json
from datetime import datetime
from sensoreUltrasuoni import leggiDati as leggiDatiSU
from sensoreMagnetico import leggiDati as leggiDatiSM


print("Avviando il server...")
async def server(websocket, path):
    try:
        def differenza(i, f):
            diff = int(f.replace(":",""))-int(i.replace(":",""))
            return diff

        def timeNow():
            return datetime.now().strftime('%H:%M:%S')

        print("Connessione con il client eseguita")

        startMessage = {"ID": 'start'}
        print(f"SENDING: {startMessage}")
        await websocket.send(json.dumps(startMessage))
        end = timeNow()

        while True:
            # Legge i dati del sensore ultrasuoni
            datiSU = leggiDatiSU()
            datiSM = leggiDatiSM()
            start = timeNow()

            # Invia i dati al client tramite WebSocket se sono diversi da ND (no data)
            if(datiSU['intrusion']==True or datiSM['intrusion']==True):
                if(datiSU['intrusion']==True):
                    await websocket.send(json.dumps(datiSU))
                if(datiSM['intrusion']==True):
                    await websocket.send(json.dumps(datiSM))
            elif(differenza(end, start)>=5):
                await websocket.send(json.dumps(datiSU))
                await websocket.send(json.dumps(datiSM))
            end = timeNow()

            await asyncio.sleep(1)  # Aggiorna i dati ogni secondo
    except Exception as e: print(f"Errore: {e}")

start_server = websockets.serve(server, '192.168.1.155', 8765)
print("Server avviato")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
