import asyncio 
import logging
import sys 
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


async def create_connection(uri, timeout=60, *args, **kwargs):
    connection = await asyncio.wait_for(websockets.connect(uri), timeout)
    return connection




async def handler(websocket):
    kucoin_connect_id = str(uuid4()).replace('-', '')
    kucoin_msg = subscribe('all')
    kucoin_uri = f"{endpoint}/?token={token}&connectId={kucoin_connect_id}"
    kucoin_websocket = await create_connection(kucoin_uri)
    ping_time = time.time()

    await kucoin_websocket.send(kucoin_msg)
    async for message in kucoin_websocket:
        try:
            if time.time() - ping_time > ping_interval:
                await kucoin_websocket.send(get_ping_msg(str(int(time.time()) * 1000)), timeout=ping_timeout)
                ping_time = time.time()
                        # data = await kucoin_websocket.recv()
            await websocket.send(message)

        except websockets.exceptions.ConnectionClosedOK:
            print("Error in need ws")
            sys.exit(0)
        except websockets.exceptions.ConnectionClosedError:
            print("We didn't close")
            sys.exit(0)
        except websocket.ConnectionClosed:


            kucoin_connect_id = str(uuid4()).replace('-', '')
            kucoin_msg = subscribe('all')
            kucoin_uri = f"{endpoint}/?token={token}&connectId={kucoin_connect_id}"
            kucoin_websocket = await create_connection(kucoin_uri)
            ping_time = time.time()

            await kucoin_websocket.send(kucoin_msg)
            async for message in kucoin_websocket:
                    if time.time() - ping_time > ping_interval:
                        await kucoin_websocket.send(get_ping_msg(str(int(time.time()) * 1000)), timeout=ping_timeout)
                        ping_time = time.time()
                                # data = await kucoin_websocket.recv()
                    await websocket.send(message)
        
async def create_server():
    async with websockets.serve(handler, "localhost", '2010') as ws:
        await asyncio.Future()





if __name__ == "__main__":
    asyncio.run(create_server())