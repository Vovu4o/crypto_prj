import asyncio
import json
import websockets 




async def handler(websocket):
    async for msg in websocket:
        await websocket.send(json.loads(msg))


async def server():
    async with websockets.serve(handler, "localhost", '2010') as ws:
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(server())