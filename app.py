from flask import Flask, jsonify
import sys
import requests

app = Flask(__name__)

@app.route('/version', methods=['GET'])
def get_version():
    app_version = "1.0.0"
    return f"Current app version: {app_version}", 200
@app.route('/temperature', methods=['GET'])
def get_temperature():

    api_url = "https://api.opensensemap.org/boxes/5eba5fbad46fb8001b799786" 
    
    # Making the GET request to the API
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()

        for sensor in data["sensors"]:
            if sensor["title"] == "Temperatur":
                temperature = sensor["lastMeasurement"]["value"]
                return jsonify({"temperature": temperature}), 200
        return jsonify({"error": "Temperature sensor not found"}), 404
    else:
        return jsonify({"error": "Failed to fetch data from the API"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)