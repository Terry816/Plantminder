from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

# Initialize sensor data storage for real-time plotting
sensor_data = {
    'temp': [],
    'hum': [],
    'soil': []
}

@app.route('/data', methods=['GET'])
def get_data():
    # Return the most recent sensor data
    if len(sensor_data['temp']) > 0:
        latest_data = {
            'temp': sensor_data['temp'][-1],
            'hum': sensor_data['hum'][-1],
            'soil': sensor_data['soil'][-1]
        }
    else:
        latest_data = {'temp': 0.0, 'hum': 0.0, 'soil': 0.0}
    return jsonify(latest_data)

@app.route('/chart_data', methods=['GET'])
def chart_data():
    # Provide all collected sensor data for the graph
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
    
    # Update the sensor data history
    if temp is not None and hum is not None and soil is not None:
        # Add the new data to the lists (limit to 20 values to avoid excessive memory use)
        if len(sensor_data['temp']) > 20:
            sensor_data['temp'].pop(0)
            sensor_data['hum'].pop(0)
            sensor_data['soil'].pop(0)
        sensor_data['temp'].append(temp)
        sensor_data['hum'].append(hum)
        sensor_data['soil'].append(soil)
        return "Sensor data updated", 200
    else:
        return "Missing parameters", 400

if __name__ == '__main__':
    app.run(debug=True)
