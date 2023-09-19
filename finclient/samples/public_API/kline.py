import json

import requests

endPoint = "https://api.coin.z.com/public"
path = "/v1/klines?symbol=BTC&interval=1min&date=20210417"

response = requests.get(endPoint + path)
print(json.dumps(response.json(), indent=2))
