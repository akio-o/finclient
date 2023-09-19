import json

import requests

endPoint = "https://api.coin.z.com/public"
path = "/v1/status"

response = requests.get(endPoint + path)
print(response.json())
