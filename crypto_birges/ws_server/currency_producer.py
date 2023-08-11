import asyncio 
import json
import time


import websockets

from kucoin_client import prevent_request, subscribe, get_ping_msg, make_topics


# данные для подключения
creds = prevent_request()



token = creds['token']
endpoint = creds['endpoint']
ping_interval = creds['ping_interval']
ping_timeout = creds['ping_timeout']


async def subscribe_channel(ws, msg):
    await ws.send(msg)

topics =  make_topics()

async def main():
    uri = "ws://localhost:2010"
    async with websockets.connect(uri) as websocket:
        async with websockets.connect(f"{endpoint}/?token={token}") as ws:
            """подключаемся к 7 веб-сокетам и подписываемся на рассылку всех валют"""
            subscribe_msg = [subscribe(topics[conn]) for conn in range(len(topics))]
            tasks = [subscribe_channel(ws, message) for message in subscribe_msg]
            await asyncio.gather(*tasks)
            msg = await ws.recv()
            channel_id = json.loads(str(msg)).get('id')
            if channel_id:
                ping_msg = get_ping_msg(channel_id)
            now = time.time()
            while True:
                async for msg in ws:
                    await websocket.send(json.dumps(msg))
                    await websocket.ping()
                    if time.time() - now + ping_interval >= ping_timeout:
                        pass
                        # await ws.send(ping_msg)
                        # now = time.time()



if __name__ == "__main__":
    asyncio.run(main())