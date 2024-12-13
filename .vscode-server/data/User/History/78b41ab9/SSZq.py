from flask import Flask, request, render_template

app = Flask(__name__)

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

    # Debug message before rendering template
    print("[DEBUG] Rendering dashboard.html with data...")

    # Render an HTML page with the data
    return render_template('dashboard.html', temp=temp, hum=hum, soil=soil)

if __name__ == '__main__':
    app.run(debug=True)
