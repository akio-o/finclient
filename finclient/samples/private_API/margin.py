import hashlib
import hmac
import json
import os
import time
from datetime import datetime

import requests

apiKey = os.environ.get("FINCLIENT_API_KEY")
secretKey = os.environ.get("FINCLIENT_SECRET_KEY")

timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
method = "GET"
endPoint = "https://api.coin.z.com/private"
path = "/v1/account/margin"

text = timestamp + method + path
sign = hmac.new(
    bytes(secretKey.encode("ascii")), bytes(text.encode("ascii")), hashlib.sha256
).hexdigest()

headers = {"API-KEY": apiKey, "API-TIMESTAMP": timestamp, "API-SIGN": sign}

res = requests.get(endPoint + path, headers=headers)
print(json.dumps(res.json(), indent=2))
