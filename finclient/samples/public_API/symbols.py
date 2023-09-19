import json

import requests

endPoint = "https://api.coin.z.com/public"
path = "/v1/symbols"

response = requests.get(endPoint + path)
print(json.dumps(response.json(), indent=2))
