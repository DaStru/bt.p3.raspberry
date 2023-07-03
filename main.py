import paho.mqtt.client as mqtt
import time
import ast
import requests
from PIL import Image, ImageDraw
from ST7789 import ST7789

#setup display
SPI_SPEED_MHZ = 80
sleeping_gif_file = "./assets/images/sleeping_dog.gif"
harmony_screen_file = "./assets/images/harmony_screen.png"

disp = ST7789(
    height=240,
    width=240,
    rotation=90,  # Needed to display the right way up on Pirate Audio
    port=0,       # SPI port
    cs=1,         # SPI port Chip-select channel
    dc=9,         # BCM pin used for data/command
    backlight=13,
    spi_speed_hz=SPI_SPEED_MHZ * 1000 * 1000
)
disp.begin()
sleeping_gif = Image.open(sleeping_gif_file)
harmony_screen = Image.open(harmony_screen_file)

gif_frame = 0

#mopidy settings
mopidy_url = "http://localhost:6680/mopidy/rpc"

#gemeral settings
currently_playing = False

def start_playback(sound):
    global gif_frame, currently_playing
    currently_playing = True
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
                "uris": [f'local:track:{sound}']
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

    sleeping_gif.seek(gif_frame)
    disp.display(sleeping_gif.resize((disp.width, disp.height)))
    gif_frame += 1
    time.sleep(0.05)

    print("Started playing")

def pause_playback():
    global gif_frame, currently_playing
    currently_playing = False
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "core.playback.pause"
    }
    response = requests.post(mopidy_url, json=payload).json()

    disp.display(harmony_screen.resize((disp.width, disp.height)))
    gif_frame = 0
    print("Stopped playing")

def stop_playback():
    global gif_frame, currently_playing
    currently_playing = False
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "core.playback.stop"
    }
    response = requests.post(mopidy_url, json=payload).json()

    disp.display(harmony_screen.resize((disp.width, disp.height)))
    gif_frame = 0
    print("Stopped playing")


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("raspberry/topic")

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    
    message_payload = ast.literal_eval(msg.payload.decode("utf-8"))
    action = message_payload["action"]
    if action == "play":
        start_playback(message_payload["payload"]["sound_name"])
    elif action == "pause":
        pause_playback()
    elif action == "stop":
        stop_playback()


#connect to mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("raspberrypi", "changemepls")
client.connect("3.78.96.233", 1883, 60)

client.loop_start()

#display logo
disp.display(harmony_screen.resize((disp.width, disp.height)))

#start loop
while True:
    if currently_playing == True:
        try:
            sleeping_gif.seek(gif_frame)
            disp.display(sleeping_gif.resize((disp.width, disp.height)))
            gif_frame += 1
            time.sleep(0.05)

        except EOFError:
            gif_frame = 0
    else:
        print("Waiting for messages")
        time.sleep(1)