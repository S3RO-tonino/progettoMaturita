import asyncio
import websockets
import json
from datetime import datetime
from sensoreUltrasuoni import leggiDati as leggiDatiSU

print("Avviando il server...")
async def server(websocket, path):
    try:
        def differenza(i, f):
            diff = int(f.replace(":",""))-int(i.replace(":",""))
            print(f"Differenza: {diff}")
            return diff
        print("Connessione con il client eseguita")
        await websocket.send(json.dumps({"sensorID": 'clientConnected', "data": 'Nessuna intrusione', "time": f"{datetime.now().strftime('%H:%M:%S')}"}))
        oldDatiSU = leggiDatiSU()

        while True:
            # Legge i dati del sensore ultrasuoni
            datiSU = leggiDatiSU()

            # Invia i dati al client tramite WebSocket se sono diversi da ND (no data)
            if(differenza(datiSU["time"], oldDatiSU["time"]) >=5 or datiSU["data"] != "ND"):
                await websocket.send(json.dumps(datiSU))
                oldDatiSU = datiSU
            await asyncio.sleep(1)  # Aggiorna i dati ogni secondo
    except Exception as e: print(f"Errore: {e}")

start_server = websockets.serve(server, '192.168.1.155', 8765)
print("Server avviato")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
