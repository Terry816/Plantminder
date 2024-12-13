from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Example sensor data (replace this with actual sensor data logic)
sensor_data = {
    'temp': 19.14,
    'hum': 57.55,
    'soil': 57.0
}

@app.route('/', methods=['GET'])
def receive_data():
    # Directly return the sensor data in JSON format
    return jsonify({
        'temp': sensor_data['temp'],
        'hum': sensor_data['hum'],
        'soil': sensor_data['soil']
    })

if __name__ == '__main__':
    app.run(debug=True)
