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
    print(f"We are the testing the following \n\n temp :{latest_sensor_data["temperature"]}")
    # Emit the updated data to all connected clients
    socketio.emit('update_data', latest_sensor_data)

    # Print the values for debugging
    print(f"Received data: Temperature={temperature}, Humidity={humidity}, Soil Moisture={soil_moisture}")

    # Check if any of the values exceed the thresholds (example thresholds)
    if temperature > 30 or humidity < 40 or soil_moisture < 50:
        # Check if enough time has passed since the last email was sent
        current_time = time.time()
        if current_time - last_email_sent_time >= cooldown_period:
            # If 3 hours have passed, send an alert and update the last_email_sent_time
            message = f"Threshold exceeded! Temp: {temperature}, Humidity: {humidity}, Soil Moisture: {soil_moisture}"
            send_alert_to_sns(message)
            last_email_sent_time = current_time
            return jsonify({'status': 'success', 'message': 'Alert sent.'}), 200
        else:
            # If it's too soon, don't send another email
            time_remaining = cooldown_period - (current_time - last_email_sent_time)

            return jsonify({'status': 'wait', 'message': f'Please wait {int(time_remaining)} seconds before the next alert.'}), 200
    else:
        return jsonify({'status': 'no_alert', 'message': 'No threshold exceeded.'}), 200

# Run the Flask-SocketIO app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
