import paho.mqtt.client as mqtt
import json

BROKER_HOST = "localhost"
BROKER_PORT = 1883
SUBSCRIBE_TOPIC = "factory/#"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to broker, reason code: {reason_code}")
    client.subscribe(SUBSCRIBE_TOPIC)


def on_message(client, userdata, msg):
    try:
        reading = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print(f"Malformed JSON on {msg.topic}, dropping message")
        return

    print(f"Received from {msg.topic}: {reading}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

client.loop_forever()