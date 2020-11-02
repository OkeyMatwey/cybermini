import asyncio
import websockets
import json
import time
token = 5000

class Session:
    free = True

def create_user():
    pass

async def consumer_handler(websocket):
    async for message in websocket:
        print("data-- ", message)
        try:
            data = json.loads(message)
        except json.JSONDecodeError as jex:
            print("EROR JSON", jex)
            continue
        if "create" in data:
            print(data["create"])
        if "delete" in data:
            print(data["delete"])

async def consume():
    url = "ws://127.0.0.1:8000/nodes/"
    async with websockets.connect(url) as websocket:
        response = json.dumps({
            'token': token
        })
        await websocket.send(response)
        await consumer_handler(websocket)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
    loop.run_forever()