import asyncio
import websockets
import json
import time
token = 5000

async def producer_handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)

async def hello():
    uri = "ws://127.0.0.1:8000/nodes/"
    async with websockets.connect(uri) as websocket:
        response = json.dumps({
            'token': token
        })
        await websocket.send(response)
        await producer_handler(websocket)

if __name__ == '__main__':
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(hello())
            asyncio.get_event_loop().run_forever()
        except:
            time.sleep(1)