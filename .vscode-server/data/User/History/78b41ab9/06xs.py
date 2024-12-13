from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Example sensor data (replace this with actual sensor data logic)
sensor_data = {
    'temp': 19.14,
    'hum': 57.55,
    'soil': 57.0
}

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({
        'temp': sensor_data['temp'],
        'hum': sensor_data['hum'],
        'soil': sensor_data['soil']
    })

@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
