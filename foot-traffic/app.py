from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- Configuration ---
ZONES = [
    "Block A", "Block B", "Block C", "Block D",
    "Canteen", "Dorm-1", "Dorm-2"
]

# --- Data Stores ---
zone_people = {zone: 0 for zone in ZONES}
latest_update = {zone: "N/A" for zone in ZONES}

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_data")
def get_data():
    """Return the latest counts for all zones."""
    result = [
        {
            "zone": zone,
            "total_foot_count": zone_people[zone],
            "last_update": latest_update.get(zone, "N/A")
        }
        for zone in ZONES
    ]
    return jsonify(result)


@app.route("/update_data", methods=["POST"])
def update_data():
    """Receive foot traffic updates (from Azure Logic App or IoT source)."""
    try:
        data = request.get_json(force=True)

        zone = data.get("zone")
        count = data.get("foot_count")
        timestamp = data.get("timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

        if not zone or zone not in zone_people:
            return jsonify({"error": f"Invalid or missing zone: {zone}"}), 400

        if count is None:
            return jsonify({"error": "Missing 'foot_count' value"}), 400

        count = int(count)

        # Update global data
        zone_people[zone] = count
        latest_update[zone] = timestamp

        print(f"✅ Updated {zone}: {count} people at {timestamp}")

        return jsonify({
            "status": "success",
            "zone": zone,
            "new_count": count,
            "timestamp": timestamp
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
