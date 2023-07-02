import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("raspberrypi", "changemepls")
client.connect("3.78.96.233", 1883, 60)

client.loop_start()

test_payloads=[
    {
        "action": "play",
        "payload": {
            "sound_name": "testsound1.mp3"
        }
    },
    {
        "action": "stop",
        "payload": {}
    }
]
cnt = 0
while cnt < len(test_payloads):
    client.publish('raspberry/topic', payload=str(test_payloads[cnt]), qos=0, retain=False)
    print(f"send {cnt} to raspberry/topic")
    cnt+=1
    time.sleep(15)