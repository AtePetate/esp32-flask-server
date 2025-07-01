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

            all_data[history_key].append({
                "date": datetime.now().strftime("%d-%m-%Y"),
                "value": raw_value
            })

            # Houd alleen de laatste 14
            all_data[history_key] = all_data[history_key][-14:]

            # Update actuele waarde
            all_data[sensor_key] = raw_value

    write_data(all_data)
    return jsonify({"message": "✅ Sensor data ontvangen en opgeslagen!"})

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    all_data = read_data()
    return jsonify(all_data)

@app.route('/log', methods=['POST'])
def receive_log():
    data = request.json
    plant_name = data.get('plant_name')
    log_entry = data.get('log')

    if not plant_name or not log_entry:
        return jsonify({"error": "Missing plant_name or log"}), 400

    all_data = read_data()

    log_key = f'log_{plant_name}'
    if log_key not in all_data:
        all_data[log_key] = []

    all_data[log_key].append({
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "entry": log_entry
    })

    write_data(all_data)
    return jsonify({"message": "✅ Logregel opgeslagen!"})

@app.route('/logs/<plant_name>', methods=['GET'])
def get_logs(plant_name):
    all_data = read_data()
    log_key = f'log_{plant_name}'
    logs = all_data.get(log_key, [])
    return jsonify(logs)

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
