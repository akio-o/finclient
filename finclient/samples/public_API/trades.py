import json

import requests

endPoint = "https://api.coin.z.com/public"
path = "/v1/trades?symbol=BTC&page=1&count=10"

response = requests.get(endPoint + path)
print(json.dumps(response.json(), indent=2))
