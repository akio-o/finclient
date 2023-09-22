import json
import time
from pprint import pprint

import websocket

websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://api.coin.z.com/ws/public/v1")
symbols = ["BTC", "ETH", "XRP"]


def on_open(self):
    for symbol in symbols:
        message = {"command": "subscribe", "channel": "ticker", "symbol": symbol}
        ws.send(json.dumps(message))
        time.sleep(0.5)


def on_message(self, message):
    try:
        msg = json.loads(message)
        pprint(msg)
    except Exception as e:
        print(e)


ws.on_open = on_open
ws.on_message = on_message

ws.run_forever()
