import asyncio
import websockets
import json

async def producer_handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)

async def hello():
    uri = "ws://127.0.0.1:8000/nodes/"
    async with websockets.connect(uri) as websocket:
        name = input("token:")
        response = json.dumps({
            'token': name
        })
        await websocket.send(response)
        await producer_handler(websocket)

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()