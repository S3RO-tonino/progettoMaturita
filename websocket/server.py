import asyncio
import websockets
from sensoreUltrasuoni import leggiDati

async def server(websocket, path):
    while True:
        # Leggi i dati dal sensore utilizzando la funzione da sensor_handler
        dati_sensore = leggiDati()

        # Invia i dati al client tramite WebSocket
        await websocket.send(dati_sensore)

        await asyncio.sleep(1)  # Aggiorna i dati ogni secondo

start_server = websockets.serve(server, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
