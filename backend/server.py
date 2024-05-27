import asyncio
import websockets
import json
<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> d5330f74f009581301ffceab902dc48b95c473dc
from sensoreUltrasuoni import leggiDati as leggiDatiSU

print("Avviando il server...")
async def server(websocket, path):
<<<<<<< HEAD
    try:
        def differenza(i, f):
            return int(f.replace(":",""))-int(i.replace(":",""))
        print("Connessione con il client eseguita")
        oldDatiSU = leggiDatiSU()
        while True:
            # Legge i dati del sensore ultrasuoni
            datiSU = leggiDatiSU()
=======
    while True:
        # Legge i dati del sensore ultrasuoni
        datiSU = leggiDatiSU()
>>>>>>> d5330f74f009581301ffceab902dc48b95c473dc

            # Invia i dati al client tramite WebSocket se sono diversi da ND (no data)
            if(differenza(datiSU["time"], oldDatiSU["time"]) >=5 or datiSU["data"] != "ND"): await websocket.send(json.dumps(datiSU))
            await asyncio.sleep(1)  # Aggiorna i dati ogni secondo
            oldDatiSU = datiSU
    except Exception as e: print(f"Errore: {e}")

start_server = websockets.serve(server, '192.168.1.155', 8765)
print("Server avviato")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
