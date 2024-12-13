from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Example sensor data (you can replace this with actual sensor data logic)
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
    # Parse query parameters (this is for the first time the data is received)
    temp = request.args.get('temp')
    hum = request.args.get('hum')
    soil = request.args.get('soil')

    print(f"[DEBUG] Raw Query Parameters: {request.args}")

    # Validate the presence of all parameters
    if temp is None or hum is None or soil is None:
        print("[ERROR] Missing one or more parameters")
        return "Missing required parameters", 400
    
    # Convert the values to float
    try:
        temp = float(temp)
        hum = float(hum)
        soil = float(soil)
    except ValueError:
        print("[ERROR] Invalid value for one or more parameters")
        return "Parameters must be valid numbers", 400
    
    print(f"[DEBUG] Received Parameters - Temp: {temp}, Hum: {hum}, Soil: {soil}")

    # Render the HTML page with the data
    return render_template('dashboard.html', temp=temp, hum=hum, soil=soil)

if __name__ == '__main__':
    app.run(debug=True)
