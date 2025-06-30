from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_data = {}

@app.route('/sensor', methods=['POST'])
def receive_sensor():
    """Ontvangt sensor data via POST en slaat deze op."""
    global latest_data
    data = request.get_json(force=True, silent=True)
    if not data:
        return 'Geen geldige JSON ontvangen', 400

    latest_data = data
    app.logger.info("Ontvangen data opgeslagen: %s", latest_data)
    return 'OK', 200

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    if latest_data:
        return jsonify(latest_data), 200
    else:
        return jsonify({"message": "Nog geen data"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
