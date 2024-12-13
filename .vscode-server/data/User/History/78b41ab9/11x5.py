from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    # Assuming the data comes from somewhere (e.g., sensors, database, etc.)
    temp = 19.14  # Replace with actual sensor data
    hum = 57.55   # Replace with actual sensor data
    soil = 57.0   # Replace with actual sensor data
    timestamp = 1672500000  # Replace with actual timestamp (UNIX time in seconds)

    # Return the data as JSON
    return jsonify({
        'temp': temp,
        'hum': hum,
        'soil': soil,
        'timestamp': timestamp
    })

@app.route('/', methods=['GET'])
def receive_data():
    print("[DEBUG] Data endpoint hit!")
    
    # Parse query parameters
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

    # Render an HTML page with the data
    return render_template('dashboard.html', temp=temp, hum=hum, soil=soil)

if __name__ == '__main__':
    app.run(debug=True)
