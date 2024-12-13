from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def receive_data():
    print("[DEBUG] Data endpoint hit!")
    return "Endpoint reached", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
