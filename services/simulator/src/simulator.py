import paho.mqtt.client as mqtt
import json
import random
import time

BROKER_HOST = "localhost"
BROKER_PORT = 1883

SENSORS = ["sensor-001", "sensor-002", "sensor-003"]

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_start()


def generate_reading(device_id: str) -> dict:
    return {
        "device_id": device_id,
        "temperature": round(random.uniform(20, 80), 1),
        "vibration": round(random.uniform(0, 10), 2),
        "battery": round(random.uniform(20, 100), 1),
    }


def publish_reading(device_id: str):
    reading = generate_reading(device_id)
    topic = f"factory/line1/{device_id}/telemetry"
    payload = json.dumps(reading)
    client.publish(topic, payload, qos=1)
    print(f"Published to {topic}: {payload}")


try:
    while True:
        for device_id in SENSORS:
            publish_reading(device_id)
        time.sleep(5)
except KeyboardInterrupt:
    print("\nStopping simulator...")
    client.loop_stop()
    client.disconnect()