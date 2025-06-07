#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <cstring>

const char* ssid = "<ssid>"; // Replace with your Wi-Fi SSID
const char* password = "<password>"; // Replace with your Wi-Fi password

const char* postURL = "http://192.168.15.9:8000/humidity/";
const char* plantBaseURL = "http://192.168.15.9:8000/plant/"; // plant ID registered in the plant table

const int moistureSensorPin = 34;
const int relayPin = 26;

int dryValue = 3200;      // Sensor value when soil is dry
int wetValue = 1000;      // Sensor value when soil is wet

struct Plant {
  int moisture_threshold;
  int check_interval;
};

int check_interval = 60;

Plant fetchPlant(int id) {
  HTTPClient http;
  String plantURL = String(plantBaseURL) + String(id);
  http.begin(plantURL);
  int httpCode = http.GET();

  Plant plant = {50, 50};
  
  if (httpCode == HTTP_CODE_OK) {
    String payload = http.getString();
    Serial.println("Plant response: " + payload);

    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, payload);

    if (error) {
      Serial.println("Failed to parse JSON");
      return plant; // fallback
    }

    plant.moisture_threshold = doc["moisture_threshold"].as<int>();
    plant.check_interval = doc["check_interval"].as<int>();

    http.end();
  } else {
    Serial.println("Failed to fetch plant, using default 50");
    http.end();
  }
  return plant;
}

void setup() {
  Serial.begin(115200);
  delay(100);

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(" connected!");

    Plant plant = fetchPlant(<id>); // Replace <id> with the actual plant ID

    int moistureThreshold = plant.moisture_threshold;
    check_interval = plant.check_interval;

    int rawReading = analogRead(moistureSensorPin);
    int moisturePercent = map(rawReading, dryValue, wetValue, 0, 100);
    moisturePercent = constrain(moisturePercent, 0, 100);

    Serial.print("Raw reading: ");
    Serial.print(rawReading);
    Serial.print(" | Moisture: ");
    Serial.print(moisturePercent);
    Serial.println("%");

    HTTPClient http;
    http.begin(postURL);
    http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"value\": " + String(moisturePercent) + "}";
    int httpResponseCode = http.POST(jsonData);

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    Serial.println("Payload sent: " + jsonData);

    http.end();

    if (moisturePercent < moistureThreshold) {
      Serial.println("Soil is dry! Starting irrigation...");
      digitalWrite(relayPin, HIGH);

      while (true) {
        delay(5000);
        rawReading = analogRead(moistureSensorPin);
        moisturePercent = map(rawReading, dryValue, wetValue, 0, 100);
        moisturePercent = constrain(moisturePercent, 0, 100);

        Serial.print("Moisture now: ");
        Serial.print(moisturePercent);
        Serial.println("%");

        if (moisturePercent >= moistureThreshold) {
          Serial.println("Soil is sufficiently moist. Stopping irrigation.");
          break;
        }
      }

      digitalWrite(relayPin, LOW);
    }

    WiFi.disconnect(true);
  } else {
    Serial.println("Failed to connect to Wi-Fi");
  }

  Serial.println("Entering Deep Sleep for 1 hour...");
  if (check_interval > 0) { 
    esp_sleep_enable_timer_wakeup(check_interval * 60 * 1000000LL); 
  } else {
    esp_sleep_enable_timer_wakeup(60 * 60 * 1000000LL);
  }
  esp_deep_sleep_start();
}

void loop() {
  // Not used
}

