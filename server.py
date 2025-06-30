from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # ✅ Voeg CORS support toe voor alle routes

# Bestand waarin we alles opslaan
DATA_FILE = 'plants_data.json'

# Init bestand als het niet bestaat
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# Helper: lees data uit bestand
def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Helper: schrijf data naar bestand
def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/sensor', methods=['POST'])
def receive_sensor():
    data = request.json

    # Laad huidige data
    all_data = read_data()

    for i in range(1, 7):
        sensor_key = f'sensor{i}'
        history_key = f'history{i}'
        if sensor_key in data:
            raw_value = data[sensor_key]

            # Voeg history toe
            if history_key not in all_data:
                all_data[history_key] = []

            # Voeg nieuwe waarde toe aan history (max 14 dagen = max 14 entries)
            all_data[history_key].append({
                "date": datetime.now().strftime("%d-%m-%Y"),
                "value": raw_value
            })

            # Houd alleen de laatste 14
            all_data[history_key] = all_data[history_key][-14:]

            # Update actuele waarde
            all_data[sensor_key] = raw_value

    # Sla op
    write_data(all_data)
    return jsonify({"message": "✅ Sensor data ontvangen en opgeslagen!"})

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    all_data = read_data()
    return jsonify(all_data)

@app.route('/plants', methods=['GET', 'POST'])
def plants():
    if request.method == 'GET':
        data = read_data()
        return jsonify(data)
    elif request.method == 'POST':
        new_data = request.json
        write_data(new_data)
        return jsonify({"message": "✅ Plant data opgeslagen!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
