import paho.mqtt.client as mqtt
import json
import requests

BROKER_HOST = "localhost"
BROKER_PORT = 1883
SUBSCRIBE_TOPIC = "factory/#"
BACKEND_URL = "http://localhost:8000"


def forward_to_backend(reading: dict) -> bool:
    try:
        response = requests.post(f"{BACKEND_URL}/telemetry", json=reading, timeout=3)
        if response.status_code == 201:
            print(f"Forwarded: {reading['device_id']}")
            return True
        else:
            print(f"Backend rejected ({response.status_code}): {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Backend unreachable")
        return False


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to broker, reason code: {reason_code}")
    client.subscribe(SUBSCRIBE_TOPIC)


def on_message(client, userdata, msg):
    try:
        reading = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print(f"Malformed JSON on {msg.topic}, dropping message")
        return

    forward_to_backend(reading)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

client.loop_forever()