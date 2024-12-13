from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Example sensor data (replace this with actual sensor data logic)
sensor_data = {
    'temp': 19.14,
    'hum': 57.55,
    'soil': 57.0
}

@app.route('/data', methods=['GET'])
def get_data():
    # You can update sensor_data with real sensor values here
    return jsonify(sensor_data)

@app.route('/', methods=['GET'])
def receive_data():
    # Directly pass initial sensor data into the template
    return render_template('dashboard.html', 
                           temp=sensor_data['temp'], 
                           hum=sensor_data['hum'], 
                           soil=sensor_data['soil'])

if __name__ == '__main__':
    app.run(debug=True)
