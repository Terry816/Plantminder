from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def receive_data():
    print("[DEBUG] Data endpoint hit!")
    # Parse query parameters
    temp = request.args.get('temp')
    hum = request.args.get('hum')
    soil = request.args.get('soil')

    print(f"[DEBUG] Received Parameters - Temp: {temp}, Hum: {hum}, Soil: {soil}")
    return "Endpoint with parameters reached", 200

