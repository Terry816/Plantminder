@app.route('/data', methods=['GET'])
def receive_data():
    print("[DEBUG] Data endpoint hit!")
    try:
        temp = float(request.args.get('temp'))
        hum = float(request.args.get('hum'))
        soil = float(request.args.get('soil'))
        print(f"[DEBUG] Parsed Parameters - Temp: {temp}, Hum: {hum}, Soil: {soil}")
        return "Parameters successfully parsed", 200
    except Exception as e:
        print(f"[ERROR] Failed to parse parameters: {e}")
        return "Error parsing parameters", 400
