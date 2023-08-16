import asyncio 
import logging
import json
import time
from uuid import uuid4

import websockets

from kucoin_client import prevent_request, subscribe, get_ping_msg, make_topics



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

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
    connect_id = str(uuid4()).replace('-', '')
    last_ping = time.time()
    async with websockets.connect(uri) as websocket:
        try:
            async with websockets.connect(f"{endpoint}/?token={token}&connectId={connect_id}") as ws:
                """подключаемся к 1 веб-сокету и подписываемся на рассылку всех валют"""
                subs_msg = subscribe("all")
                await ws.send(subs_msg)
                msg = await ws.recv()
                channel_id = json.loads(str(msg)).get('id')
                if channel_id:
                    ping_msg = get_ping_msg(channel_id)
                while True:
                    async for msg in ws:
                        if time.time() - last_ping >= ping_interval:
                            await ws.send(ping_msg(str(int(time.time()) * 1000)), timeout=ping_timeout)
                            await websocket.ping()
                        now = time.time()
                        await websocket.send(json.dumps(msg))
        except websockets.exceptions.ConnectionClosedOK:
            print("Error in need ws")
        except websockets.exceptions.ConnectionClosedError:
            print("We didn't close")



if __name__ == "__main__":
    asyncio.run(main())