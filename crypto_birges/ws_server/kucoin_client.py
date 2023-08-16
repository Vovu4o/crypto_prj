import asyncio 
import json 

import requests 



BASE_URL = 'https://api.kucoin.com'
DONOT_TAKE = ['GBP', 'USDC', 'EUR', 'TUSD', 'DAI', 'BRL']
CONNECTIONS = 2 * 7

def prevent_request():
    # base_uri!
    # uri!
    uri = BASE_URL + '/api/v1/bullet-public'

    r = requests.post(uri)
    assert r.status_code == 200
    response = r.json()
    token = response['data']['token']
    ping_interval = float(response['data']['instanceServers'][0]['pingInterval']) / 1000
    ping_timeout = float(response['data']['instanceServers'][0]['pingTimeout']) / 1000 - 1
    endpoint = response['data']['instanceServers'][0]['endpoint']

    return {
        "token": token,
        "ping_interval": ping_interval,
        "ping_timeout": ping_timeout,
        "endpoint": endpoint
    }

def all_currencies():
    with open("currencies.txt", "w") as file:
        uri = '/api/v1/market/allTickers'
        r = requests.get(BASE_URL + uri)
        assert r.status_code == 200
        response = r.json()
        for cur in response['data']['ticker']:
            file.write(cur['symbol'] + '\n')

def make_triangle():
    with open("currencies.txt") as f:
        currencies = [s.strip('\n') for s in f.readlines()]
        no_usdt = []
        cur_triangles = {}
        for cur in currencies:
            if ("USDT" not in cur) and (cur not in DONOT_TAKE):
                if not cur_triangles.get(cur):
                    c0, c1 = cur.split('-')
                    cur_triangles[cur] = [f"{c0}-USDT", f"{c1}-USDT"]
    return cur_triangles


def create_triangle():
    all_triangle = []
    unique_pairs = make_triangle()
    for k, v in unique_pairs.items():
        triangle = [0] * 3
        triangle[0], triangle[2] = v
        triangle[1] = k
        all_triangle += [triangle]
        all_triangle += [reversed(triangle)]
    
    with open("triangles.txt", 'w') as file:
        for tri in all_triangle:
            file.write(":".join(tri) + '\n')

def make_topics():
    triangle = make_triangle()
    all_topics = []
    keys = list(triangle.keys())
    for pair in range(len(keys) // 67):      
        topic = ""
        for t in range(67):
            topic += keys[pair * 7 + t] + ','
        else:
            topic = topic[:-1]
        all_topics += [topic]
    return all_topics


def subscribe(topic):
    subscribe_msg = json.dumps({
        "type": "subscribe",
        "topic": f"/market/ticker:{topic}",
        "privateChannel": False,                      
        "response": True 
    })
    return subscribe_msg

def get_ping_msg(id):
    msg = json.dumps({"id": id, "type": "ping"})
    return msg

        

