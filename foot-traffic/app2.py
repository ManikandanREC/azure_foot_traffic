from flask import Flask, jsonify, render_template 
from flask_cors import CORS
import threading
import random
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- Configuration ---
TOTAL_PEOPLE = 1000  # fixed total campus population
UPDATE_INTERVAL = 5  # seconds

ZONES = {
    "Block A": [f"Classroom-{i}" for i in range(1, 16)],
    "Block B": [f"Classroom-{i}" for i in range(1, 16)],
    "Block C": [f"Classroom-{i}" for i in range(1, 16)],
    "Block D": [f"Classroom-{i}" for i in range(1, 16)],
    "Canteen": [f"Canteen-{i}" for i in range(1, 6)],
    "Dorm-1": [f"Dorm1-WiFi-{i}" for i in range(1, 11)],
    "Dorm-2": [f"Dorm2-WiFi-{i}" for i in range(1, 16)],
}

# Store current distribution per zone
zone_people = {zone: TOTAL_PEOPLE // len(ZONES) for zone in ZONES}  # equal at start
device_data = {}  # {device_id: {zone, foot_count, timestamp}}

# --- Simulation logic ---
def simulate_data():
    global zone_people
    while True:
        zones = list(ZONES.keys())

        # Randomly select a "hot zone" (attracts more people)
        hot_zone = random.choice(zones)
        for _ in range(random.randint(20, 50)):  # more movement events
            from_zone = random.choice(zones)
            to_zone = random.choice(zones)

            # Bias toward hot zone (people move there more often)
            if random.random() < 0.3:
                to_zone = hot_zone

            if from_zone != to_zone and zone_people[from_zone] > 10:
                move = random.randint(5, 50)
                move = min(move, zone_people[from_zone])
                zone_people[from_zone] -= move
                zone_people[to_zone] += move

        # Update devices per zone with small random variation
        for zone, devices in ZONES.items():
            base = zone_people[zone] // len(devices)
            for device in devices:
                device_data[device] = {
                    "zone": zone,
                    "foot_count": max(0, base + random.randint(-5, 5)),
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }

        total_now = sum(zone_people.values())
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Total: {total_now} | Hot Zone: {hot_zone}")

        time.sleep(5)


# Start background simulation
threading.Thread(target=simulate_data, daemon=True).start()

# --- Flask routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data")
def get_data():
    result = [{"zone": zone, "total_foot_count": zone_people[zone]} for zone in ZONES]
    return jsonify(result)

@app.route("/update_data", methods=["POST"])
def update_data():
    data = request.get_json()
    zone = data.get("zone")
    count = data.get("foot_count")

    if zone in zone_people:
        zone_people[zone] += count  # or replace with your logic
        return jsonify({"status": "success", "zone": zone, "new_count": zone_people[zone]})
    return jsonify({"error": "Invalid zone"}), 400


# --- Run ---
if __name__ == "__main__":
    app.run(debug=True)
