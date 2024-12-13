# Plant Monitoring and Alert System (Plantminder)

## Motivation
The motivation behind the *Plantminder* project is to create a reliable and efficient system for monitoring the environmental conditions of plants, specifically their temperature, humidity, and soil moisture levels. The goal of this project is to provide real-time monitoring, data analytics, and alerts to ensure that plants receive optimal care even when the user is not physically present, using a combination of IoT sensors, cloud services, and data visualization techniques.

## Project Overview
The *Plantminder* system continuously collects environmental data (temperature, humidity, and soil moisture) from sensors connected to an Arduino device. This data is then sent to a web server built with Flask, where it's displayed on a real-time dashboard. Additionally, an alert system integrated with AWS SNS (Simple Notification Service) sends notifications when certain environmental thresholds are exceeded, helping users take necessary actions to care for their plants.

## Features
- **Real-time Data Collection**: Collects and displays data for temperature, humidity, and soil moisture.
- **Data Visualization**: Uses Flask and JavaScript (Chart.js) to display a real-time updating graph of sensor data on a webpage.
- **AWS SNS Alerts**: Sends automated alerts to a specified email when environmental thresholds (e.g., temperature, humidity, or soil moisture) exceed predefined limits.
- **Cloud Integration**: Data is pushed to an AWS EC2 instance and stored for visualization and alerting purposes.

## Requirements
### Hardware:
- Arduino with sensors (e.g., DHT11 for temperature and humidity, soil moisture sensor)
- Wi-Fi module (e.g., ESP8266) for Arduino to send data to a web server

### Software:
- Python 3.x
- Flask for web server
- AWS SDK (Boto3) for SNS integration
- Chart.js for data visualization on the frontend
- Git for version control

### Services:
- **AWS EC2**: To host the Flask web application and SNS integration.
- **AWS SNS**: For sending notifications when thresholds are exceeded.

## Setup Instructions

### 1. Clone the Repository
First, clone the GitHub repository to your local machine or EC2 instance:

```bash
git clone https://github.com/Terry816/Plantminder.git
cd Plantminder
