from flask import Flask, render_template, jsonify, request
import time
import boto3

app = Flask(__name__)

# Initialize sensor data storage for real-time plotting
sensor_data = {
    'temp': [],
    'hum': [],
    'soil': []
}

# Set up the SNS client (ensure your EC2 instance has necessary IAM permissions)
sns_client = boto3.client('sns', region_name='us-west-1')  # Update to your SNS region
sns_topic_arn = 'arn:aws:sns:us-west-1:867344476207:PlantMonitoringAlerts'  # Replace with your SNS ARN

# To store the last time an email was sent
last_email_sent_time = 0  # Timestamp (Unix time) of the last email sent
cooldown_period = 3 * 60 * 60  # 3 hours in seconds (3 * 60 * 60)

# Function to send alert to SNS
def send_alert_to_sns(message):
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='Plant Monitoring Alert'
    )
    print("Alert sent to SNS.")

@app.route('/data', methods=['GET'])
def get_data():
    # Return the most recent sensor data
    if len(sensor_data['temp']) > 0:
        latest_data = {
            'temp': sensor_data['temp'][-1],
            'hum': sensor_data['hum'][-1],
            'soil': sensor_data['soil'][-1]
        }
    else:
        latest_data = {'temp': 0.0, 'hum': 0.0, 'soil': 0.0}
    return jsonify(latest_data)

@app.route('/chart_data', methods=['GET'])
def chart_data():
    # Provide all collected sensor data for the graph
    return jsonify(sensor_data)

@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')

@app.route('/update_sensor', methods=['GET'])
def update_sensor():
    global last_email_sent_time

    # Retrieve sensor data from the query parameters sent by the Arduino
    temp = request.args.get('temp', type=float)
    hum = request.args.get('hum', type=float)
    soil = request.args.get('soil', type=float)
    
    # Update the sensor data history
    if temp is not None and hum is not None and soil is not None:
        # Add the new data to the lists (limit to 20 values to avoid excessive memory use)
        if len(sensor_data['temp']) > 20:
            sensor_data['temp'].pop(0)
            sensor_data['hum'].pop(0)
            sensor_data['soil'].pop(0)
        sensor_data['temp'].append(temp)
        sensor_data['hum'].append(hum)
        sensor_data['soil'].append(soil)
        
        # Check if any of the values exceed the thresholds (example thresholds)
        if temp > 30 or hum < 40 or soil < 50:
            current_time = time.time()
            if current_time - last_email_sent_time >= cooldown_period:
                # Send alert if the condition is met and it's been more than the cooldown period
                message = f"Threshold exceeded! Temp: {temp}, Humidity: {hum}, Soil Moisture: {soil}"
                send_alert_to_sns(message)
                last_email_sent_time = current_time
                print("Alert triggered and sent.")
        
        return "Sensor data updated", 200
    else:
        return "Missing parameters", 400

if __name__ == '__main__':
    app.run(debug=True)
