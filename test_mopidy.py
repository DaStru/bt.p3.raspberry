import requests
import json

mopidy_url = "http://localhost:6680/mopidy/rpc"

payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "core.describe"
}

response = requests.post(mopidy_url, json=payload).json()

print(response)