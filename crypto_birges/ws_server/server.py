import asyncio
import json
import random
import websockets 




async def handler(websocket):
    while True:
        incoming_msg = await websocket.recv()
        # print(incoming_msg)
        # incoming_msg = {"msg": str(random.randint(1, 1000))}
        await websocket.send(json.dumps(incoming_msg))


async def server():
    async with websockets.serve(handler, "localhost", '2010') as ws:
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(server())