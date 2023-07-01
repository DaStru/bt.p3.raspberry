import requests
import json
import sys

mopidy_url = "http://localhost:6680/mopidy/rpc"

payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": sys.argv[1],
        "params": sys.argv[2] if sys.argv[1] else []
}

response = requests.post(mopidy_url, json=payload).json()

print(response)