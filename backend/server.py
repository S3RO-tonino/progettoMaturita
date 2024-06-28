import asyncio
import websockets
import json
from datetime import datetime
from sensoreUltrasuoni import leggiDati as leggiDatiSU
from sensoreMagnetico import leggiDati as leggiDatiSM

print("Avviando il server...")
async def server(websocket, path):
    try:
        def differenza(f, i):
            diff = int(f.replace(":",""))-int(i.replace(":",""))
            return int(diff)

        def timeNow():
            return datetime.now().strftime('%H:%M:%S')

        print("Connessione con il client eseguita")

        startMessage = {"ID": 'start'}
        print(f"SENDING: {startMessage}")
        await websocket.send(json.dumps(startMessage))
        #end = timeNow()
        datiSUTime = ''
        datiSMTime = ''
        while True:
            # Legge i dati dei sensori
            datiSU = leggiDatiSU()
            datiSM = leggiDatiSM()
            #start = timeNow()
            if datiSUTime == '':
                datiSUTime = timeNow()
                datiSMTime = timeNow()
                await websocket.send(json.dumps(datiSU))
                await websocket.send(json.dumps(datiSM))

            # Invia i dati al client tramite WebSocket
            if(datiSU['intrusion']==True and differenza(datiSU['mex'], datiSUTime) < 5):
                datiSUTime = timeNow()
                await websocket.send(json.dumps(datiSU))
            elif(datiSM['intrusion']==True and differenza(datiSU['mex'], datiSUTime) < 5):
                datiSMTime = timeNow()
                await websocket.send(json.dumps(datiSM))
            else:
                await websocket.send(json.dumps(datiSU))
                await websocket.send(json.dumps(datiSM))
            await asyncio.sleep(1)
            #end = timeNow()
            print(f"{datiSU} {datiSUTime} {differenza(datiSU['mex'], datiSUTime)}")

            await asyncio.sleep(1)  # Aggiorna i dati ogni secondo
    except Exception as e: print(f"Errore: {e}")

start_server = websockets.serve(server, '192.168.1.155', 8765)
print("Server avviato")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
