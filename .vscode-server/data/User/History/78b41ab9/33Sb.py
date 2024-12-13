from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initialize sensor data (will be updated with incoming data from the Arduino)
sensor_data = {
    'temp': 0.0,
    'hum': 0.0,
    'soil': 0.0
}

@app.route('/data', methods=['GET'])
def get_data():
    # Return the most recent sensor data
    return jsonify(sensor_data)

@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')

@app.route('/update_sensor', methods=['GET'])
def update_sensor():
    # Retrieve sensor data from the query parameters sent by the Arduino
    temp = request.args.get('temp', type=float)
    hum = request.args.get('hum', type=float)
    soil = request.args.get('soil', type=float)
    
    # Update the global sensor data
    if temp is not None and hum is not None and soil is not None:
        sensor_data['temp'] = temp
        sensor_data['hum'] = hum
        sensor_data['soil'] = soil
        return "Sensor data updated", 200
    else:
        return "Missing parameters", 400

if __name__ == '__main__':
    app.run(debug=True)
