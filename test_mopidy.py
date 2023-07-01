import requests
import json
import sys
import ast

mopidy_url = "http://localhost:6680/mopidy/rpc"

payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": sys.argv[1],
        "params": ast.literal_eval(sys.argv[2])
}

response = requests.post(mopidy_url, json=payload).json()

print(response)