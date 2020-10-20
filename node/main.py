import asyncio
import websockets

async def hello():
    uri = "ws://127.0.0.1:8000/chat/"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)

        greeting = await websocket.recv()

asyncio.get_event_loop().run_until_complete(hello())