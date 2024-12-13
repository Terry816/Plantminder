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
    # Log all incoming requests
    print(f"[DEBUG] Incoming Request - {request}")
    temp = request.args.get('temp')
    hum = request.args.get('hum')
    soil = request.args.get('soil')
    print(f"[DEBUG] Raw Query Parameters: {request.args}")

    # Handle the data
    if temp is None or hum is None or soil is None:
        print("[ERROR] Missing one or more parameters")
        return "Missing required parameters", 400
    
    try:
        temp = float(temp)
        hum = float(hum)
        soil = float(soil)
    except ValueError:
        print("[ERROR] Invalid parameter value")
        return "Parameters must be valid numbers", 400

    return render_template('dashboard.html', temp=temp, hum=hum, soil=soil)

if __name__ == '__main__':
    app.run(debug=True)
