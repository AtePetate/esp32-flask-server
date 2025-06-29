from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_data = {}

@app.route('/sensor', methods=['POST'])
def receive_sensor():
    global latest_data
    data = request.get_json()
    if data:
        latest_data = data
        print(f"✅ Ontvangen data opgeslagen: {latest_data}")
        return 'OK', 200
    return 'Geen data ontvangen', 400

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    if latest_data:
        return jsonify(latest_data), 200
    else:
        return jsonify({"message": "Nog geen data"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
