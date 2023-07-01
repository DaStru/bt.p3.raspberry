import requests
import json
import sys
import ast
import time

mopidy_url = "http://localhost:6680/mopidy/rpc"

payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "core.tracklist.clear"
}
response = requests.post(mopidy_url, json=payload).json()
print("Cleared tracklist")

payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "core.tracklist.add",
        "params": {
                "uris": ['local:track:testsound1.mp3']
        }
}
response = requests.post(mopidy_url, json=payload).json()
print("Added track to tracklist")

payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "core.mixer.set_volume",
        "params": {
                "volume": 100
        }
}
response = requests.post(mopidy_url, json=payload).json()
print("Set volume")

payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "core.playback.play"
}
response = requests.post(mopidy_url, json=payload).json()
print("Started playing")

time.sleep(15)

payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "core.playback.stop"
}
response = requests.post(mopidy_url, json=payload).json()
print("Stopped playing")