from flask import Flask, render_template_string
import paho.mqtt.client as mqtt
import json
import threading
import time

app = Flask(__name__)

# Data storage
data_store = {}

# Konfigurasi Failover
BROKER_LIST = ["broker-primary", "broker-secondary"]
current_broker_idx = 0
client = mqtt.Client()

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        sensor = payload.get("sensor") or payload.get("type") or msg.topic
        value = payload.get("value") or payload.get("val") or payload.get("data") or payload
        broker_used = payload.get("broker_used", "unknown")
        data_store[sensor] = {"value": value, "broker_used": broker_used}
        print(f"[DASHBOARD] Reveiced from {msg.topic}: sensor={sensor}, value={value}")
    except Exception as e:
        print(f"[DASHBOARD] Error processing message: {e}")

def mqtt_worker():
    global current_broker_idx
    client.on_message = on_message
    
    while True:
        target = BROKER_LIST[current_broker_idx]
        try:
            print(f"[DASHBOARD] Connecting to {target}...")
            client.connect(target, 1883, 5)
            client.subscribe("sensor/#")
            print(f"[DASHBOARD] Connected to {target}")
            
            # Loop forever akan block di sini sampai disconnect/error
            client.loop_forever() 
            
        except Exception:
            print(f"[DASHBOARD] Connection lost/failed to {target}")
        
        # Jika loop_forever tembus (artinya disconnect), pindah broker
        print("[DASHBOARD] Switching Broker...")
        current_broker_idx = (current_broker_idx + 1) % len(BROKER_LIST)
        time.sleep(2)

# Start Background Thread
t = threading.Thread(target=mqtt_worker)
t.daemon = True
t.start()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="2">
    <title>HA Dashboard</title>
    <style>
        body { font-family: monospace; padding: 20px; background: #222; color: #fff; }
        .card { border: 1px solid #444; padding: 15px; margin: 10px; display: inline-block; width: 200px; }
        h1 { color: #00ff00; }
        .src { font-size: 10px; color: #aaa; }
    </style>
</head>
<body>
    <h1>High Availability IoT Monitor</h1>
    {% for sensor, data in store.items() %}
    <div class="card">
        <h3>{{ sensor.upper() }}</h3>
        <h2>{{ data.value }}</h2>
        <div class="src">Via: {{ data.broker_used }}</div>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, store=data_store)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)