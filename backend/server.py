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
        end = timeNow()

        while True:
            # Legge i dati dei sensori
            datiSU = leggiDatiSU()
            datiSM = leggiDatiSM()
            start = timeNow()
            if datiSU['mex'] == '': datiSU['mex'] = timeNow()
            if datiSM['mex'] == '': datiSM['mex'] = timeNow()

            # Invia i dati al client tramite WebSocket
            if(datiSU['intrusion']==True):
                datiSU['mex'] = timeNow()
                await websocket.send(json.dumps(datiSU))
            if(datiSM['intrusion']==True):
                datiSM['mex'] = timeNow()
                await websocket.send(json.dumps(datiSM))
            elif(differenza(datiSU['mex'], start)>=5 or differenza(datiSM['mex'], start)>=5):
                await websocket.send(json.dumps(datiSU))
                await websocket.send(json.dumps(datiSM))
            await asyncio.sleep(1)
            end = timeNow()
            print(f"{start}, {end} - {differenza(end, start)} - {datiSU} {datiSM}")

            await asyncio.sleep(1)  # Aggiorna i dati ogni secondo
    except Exception as e: print(f"Errore: {e}")

start_server = websockets.serve(server, '192.168.1.155', 8765)
print("Server avviato")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
