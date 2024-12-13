import time
import boto3
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit

# Initialize the Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Set up the SNS client (ensure your EC2 instance has necessary IAM permissions)
sns_client = boto3.client('sns', region_name='us-west-1')  # Update to your SNS region

# SNS Topic ARN (replace with your actual SNS topic ARN)
sns_topic_arn = 'arn:aws:sns:us-west-1:867344476207:PlantMonitoringAlerts'

# To store the last time an email was sent
last_email_sent_time = 0  # Timestamp (Unix time) of the last email sent
cooldown_period = 3 * 60 * 60  # 3 hours in seconds (3 * 60 * 60)

# Store the latest sensor data
latest_sensor_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "soil_moisture": 0.0,
    "timestamp": time.time()
}

# Function to send alert to SNS
def send_alert_to_sns(message):
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='Plant Monitoring Alert'
    )
    print("Alert sent to SNS.")

# Route to display the dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route to receive IoT data and trigger email if thresholds are exceeded
@app.route('/data', methods=['GET'])
def receive_data():
    global last_email_sent_time, latest_sensor_data

    # Debugging: Print details about the request
    print("\n[DEBUG] Incoming Request Details:")
    print("Request Method:", request.method)  # Method, e.g., GET
    print("Request URL:", request.url)  # Full URL
    print("Request Args (Query Params):", request.args)  # URL params like ?temp=xx&hum=xx
    print("Request Headers:", request.headers)  # All HTTP headers
    print("Request Data (Raw Body):", request.data)  # Raw data (useful for POST/PUT)

    try:
        # Retrieve sensor data from URL parameters
        temperature = float(request.args.get('temp'))
        humidity = float(request.args.get('hum'))
        soil_moisture = float(request.args.get('soil'))

        # Update the latest sensor data
        latest_sensor_data = {
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture": soil_moisture,
            "timestamp": time.time()
        }

        print("\n[DEBUG] Parsed Sensor Data:")
        print(f"Temperature: {temperature}, Humidity: {humidity}, Soil Moisture: {soil_moisture}")
    except Exception as e:
        print("\n[ERROR] Failed to parse sensor data. Exception:", e)
        return jsonify({'status': 'error', 'message': 'Invalid data format'}), 400

    # Emit the updated data to all connected clients
    socketio.emit('update_data', latest_sensor_data)

    # Print to indicate whether an alert is triggered
    if temperature > 30 or humidity < 40 or soil_moisture < 50:
        print("[DEBUG] Threshold exceeded. Evaluating if alert should be sent...")
        current_time = time.time()
        if current_time - last_email_sent_time >= cooldown_period:
            print("[DEBUG] Cooldown period passed. Sending alert...")
            message = f"Threshold exceeded! Temp: {temperature}, Humidity: {humidity}, Soil Moisture: {soil_moisture}"
            send_alert_to_sns(message)
            last_email_sent_time = current_time
            return jsonify({'status': 'success', 'message': 'Alert sent.'}), 200
        else:
            time_remaining = cooldown_period - (current_time - last_email_sent_time)
            print(f"[DEBUG] Cooldown period not passed. Time remaining: {time_remaining:.2f} seconds.")
            return jsonify({'status': 'wait', 'message': f'Please wait {int(time_remaining)} seconds before the next alert.'}), 200
    else:
        print("[DEBUG] No thresholds exceeded. No alert sent.")
        return jsonify({'status': 'no_alert', 'message': 'No threshold exceeded.'}), 200


# Run the Flask-SocketIO app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
