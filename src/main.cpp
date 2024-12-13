#include <Arduino.h>
#include <Wire.h>
#include <DHT20.h>
#include <WiFi.h>
#include <HttpClient.h>

// DHT20 sensor configuration
DHT20 dht;

// Soil moisture sensor configuration (assuming an analog sensor connected to A0)
const int soilMoisturePin = A0; // Replace with your analog pin for the soil moisture sensor

// WiFi credentials
const char* ssid = "TerryK";  // Replace with your WiFi SSID
const char* password = "rosienbuddy";  // Replace with your WiFi password

// Cloud server details
const char* serverIP = "13.52.177.185";  // Replace with your EC2 instance IP address
const int serverPort = 5000;            // Port for Flask server
const char* serverPath = "/update_sensor"; // Path for HTTP request to update the sensor data

void setup() {
    // Initialize Serial Monitor
    Serial.begin(9600);
    delay(1000);

    // Initialize I2C communication
    Wire.begin();

    // Initialize DHT20 sensor
    if (!dht.begin()) {
        Serial.println("Failed to initialize DHT20 sensor!");
        while (1);  // Stop execution if initialization fails
    }

    // Connect to WiFi
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
    // Read data from the DHT20 sensor
    if (dht.read() != DHT20_OK) {
        Serial.println("Failed to read from DHT20 sensor!");
        delay(1000);
        return;
    }

    // Get temperature and humidity values
    float temperature = dht.getTemperature();
    float humidity = dht.getHumidity();
    
    // Read soil moisture value (assuming analog sensor)
    int soilMoistureValue = analogRead(soilMoisturePin);
    Serial.print("Raw soil moisture value: ");
    Serial.println(soilMoistureValue);  // Print raw analog value for debugging

    float soilMoisture = map(soilMoistureValue, 0, 2600, 100, 0);

    // Print values to Serial Monitor
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C, Humidity: ");
    Serial.print(humidity);
    Serial.print(" %, Soil Moisture: ");
    Serial.print(soilMoisture);
    Serial.println(" %");

    // Send data to cloud server
    WiFiClient client;
    HttpClient http(client);
    
    // Prepare the HTTP GET request
    String url = String(serverPath) + "?temp=" + String(temperature) + "&hum=" + String(humidity) + "&soil=" + String(soilMoisture);
    int statusCode = http.get(serverIP, serverPort, url.c_str());
    
    // Check the response status
    if (statusCode == 0) {
        Serial.println("Data sent to cloud successfully.");
    } else {
        Serial.print("Failed to send data to cloud. HTTP Status Code: ");
        Serial.println(statusCode);
    }

    // Wait 10 seconds before the next reading
    delay(3000);
}
