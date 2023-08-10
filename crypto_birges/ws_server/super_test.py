import asyncio 
import json
import time


import websockets

from client import Client
from kucoin_client import prevent_request, subscribe, ping_msg, make_topics


creds = prevent_request()


async def handle():
    async with websockets.connect(f"{creds['endpoint']}/?token={creds['token']}") as ws:
        topic = make_topics()[66]
        now = time.time()
        subs_msg = subscribe(topic)
        msg = await ws.send(subs_msg)
        if msg:
            channel_id = json.loads(str(msg))['channel_id']

        async for msg in ws:
            asyncio.sleep(5.)
            print(msg)
            if (time.time() - now) + creds['ping_timeout'] >= creds['ping_interval']:
                ping = ping_msg(channel_id)
                await ws.send(ping)
                now = time.time()




# async def main():
#     now = time.time()
#     async with websockets.connect(f"{creds['endpoint']}/?token={creds['token']}") as ws:
#         msg = await ws.send(subscribe_msg)
#         if msg:
#             channel_id = json.loads(str(msg))['channel_id']
        
#         async for msg in ws:
#             data = json.loads(str(msg)).get("data")
#             if data:
#                 print(f'Price: {data.get("price")} | Ask: {data.get("bestAsk")} | Bid: {data.get("bestBid")}')
#             await asyncio.sleep(1.5)
#             if (time.time() - now) + creds['ping_timeout'] >= creds['ping_interval']:
#                 await ws.send(json.dumps({"id": channel_id, "type": "ping"}))


asyncio.run(handle())