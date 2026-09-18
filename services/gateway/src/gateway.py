import paho.mqtt.client as mqtt
import json
import time
import requests
from collections import deque

BROKER_HOST = "localhost"
BROKER_PORT = 1883
SUBSCRIBE_TOPIC = "factory/#"
BACKEND_URL = "http://localhost:8000"

buffer = deque()


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
        print("Backend unreachable, will buffer")
        return False


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to broker, reason code: {reason_code}")
    client.subscribe(SUBSCRIBE_TOPIC, qos=1)


def on_message(client, userdata, msg):
    try:
        reading = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print(f"Malformed JSON on {msg.topic}, dropping message")
        return

    success = forward_to_backend(reading)
    if not success:
        buffer.append(reading)
        print(f"Buffered. Queue size: {len(buffer)}")


def retry_buffered_messages():
    while buffer:
        reading = buffer[0]
        if forward_to_backend(reading):
            buffer.popleft()
            print(f"Retry succeeded. Queue size: {len(buffer)}")
        else:
            break 


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="gateway-1", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_start()

try:
    while True:
        retry_buffered_messages()
        time.sleep(5)
except KeyboardInterrupt:
    print("\nStopping gateway...")
    client.loop_stop()
    client.disconnect()