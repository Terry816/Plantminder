import boto3
import time

sns_client = boto3.client('sns', region_name='us-west-1')
sns_topic_arn = 'arn:aws:sns:us-west-1:867344476207:PlantMonitoringAlerts'

last_email_sent_time = 0
cooldown_period = 3 * 60 * 60  # 3 hours

def send_alert_to_sns(message):
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='Plant Monitoring Alert'
    )
    print("[DEBUG] Alert sent to SNS.")

@app.route('/', methods=['GET'])
def receive_data():
    global last_email_sent_time
    print("[DEBUG] Data endpoint hit!")
    try:
        temp = float(request.args.get('temp'))
        hum = float(request.args.get('hum'))
        soil = float(request.args.get('soil'))
        print(f"[DEBUG] Parsed Parameters - Temp: {temp}, Hum: {hum}, Soil: {soil}")

        # Check thresholds and send alert if necessary
        if temp > 30 or hum < 40 or soil < 50:
            current_time = time.time()
            if current_time - last_email_sent_time >= cooldown_period:
                message = f"Threshold exceeded! Temp: {temp}, Hum: {hum}, Soil: {soil}"
                send_alert_to_sns(message)
                last_email_sent_time = current_time
                return "Alert sent", 200
            else:
                print("[DEBUG] Cooldown period active.")
                return "Cooldown active", 200
        else:
            print("[DEBUG] No thresholds exceeded.")
            return "No thresholds exceeded", 200
    except Exception as e:
        print(f"[ERROR] Failed to parse parameters: {e}")
        return "Error parsing parameters", 400
