import asyncio
import websockets
import json
from sensoreUltrasuoni import leggiDati as datiSU

async def server(websocket, path):
    while True:
        # Legge i dati del sensore ultrasuoni
        datiSU = leggiSU()

        # Invia i dati al client tramite WebSocket se sono diversi da ND (no data)
        if datiSU["data"] != "ND":
            await websocket.send(json.dumps(datiSU))

        await asyncio.sleep(1)  # Aggiorna i dati ogni secondo

start_server = websockets.serve(server, '192.168.1.155', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
