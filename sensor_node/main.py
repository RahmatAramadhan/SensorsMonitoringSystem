import time
import random
import os
import json
import paho.mqtt.client as mqtt
from threading import Thread

SENSOR_TYPE = os.getenv('SENSOR_TYPE', 'temperature')
TOPIC = f"sensor/{SENSOR_TYPE}"

BROKER_LIST = ["broker-primary", "broker-secondary"]
CURRENT_BROKER_INDEX = 0

client = mqtt.Client()

def get_data():
    if SENSOR_TYPE == 'temperature':
        return round(random.uniform(25.0, 40.0), 1)
    if SENSOR_TYPE == 'humidity':
        return int(random.uniform(30, 70))
    if SENSOR_TYPE == 'voltage':
        return int(random.uniform(110, 240))
    if SENSOR_TYPE == 'air_quality':
        return int(random.uniform(50, 150))
    return 0

def connect_to_broker():
    global CURRENT_BROKER_INDEX

    while True:
        target_broker = BROKER_LIST[CURRENT_BROKER_INDEX]
        print(f"[{SENSOR_TYPE}] Connecting to broker: {target_broker}...")

        try:
            client.connect(target_broker, 1883, 5)
            client.loop_start()
            print(f"[{SENSOR_TYPE}] Connected to broker: {target_broker}")
            return
        except Exception as e:
            print(f"[{SENSOR_TYPE}] Connection to broker {target_broker} error: {e}")
            CURRENT_BROKER_INDEX = (CURRENT_BROKER_INDEX + 1) % len(BROKER_LIST)
            print(f"[{SENSOR_TYPE}] Switching to next broker...")
            time.sleep(5)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"[{SENSOR_TYPE}] Disconnected from broker with result code ! , reconnecting...")
        connect_to_broker()
client.on_disconnect = on_disconnect

connect_to_broker()
while True:
    try:
        val = get_data()
        payload = json.dumps({
            "sensor": SENSOR_TYPE,
            "value": val,
            "broker_used": BROKER_LIST[CURRENT_BROKER_INDEX]
        })

        info = client.publish(TOPIC, payload)

        info.wait_for_publish(timeout=2)
        
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            raise Exception("Publish failed")

        print(f"[{SENSOR_TYPE}] Sent data: {val} via {BROKER_LIST[CURRENT_BROKER_INDEX]}")

    except Exception as e:
        print(f"[{SENSOR_TYPE}] Error publishing data. Reconnecting... logic activated")
        connect_to_broker()
    
    time.sleep(2)