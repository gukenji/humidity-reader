# 💧 Automatic Watering System with ESP32, FastAPI, and Vue

This project is an **automatic irrigation system** controlled via Wi-Fi, ideal for watering plants based on soil moisture. It uses an **ESP32**, sensors, and a web-based frontend and backend to visualize and manage the data.

## 🔧 Components Used

- ✅ ESP32 (Wi-Fi enabled)
- ✅ Capacitive soil moisture sensor
- ✅ 10kΩ resistor
- ✅ Transistor (to switch the pump)
- ✅ 5V relay module
- ✅ 5V water pump
- ✅ **MT3608** step-up module – used to boost battery voltage to 5V
- ✅ Power supply (batteries or power bank)
- ✅ Backend built with **FastAPI**
- ✅ Frontend built with **Vue + Vite**

## 🧠 Project Overview

- The **ESP32** reads soil moisture data and sends it to the FastAPI backend via HTTP.
- The backend (FastAPI + PostgreSQL) stores the data and exposes an API.
- The frontend (Vue + Vite) displays the latest moisture readings and auto-refreshes.
- The system activates the **water pump** if the moisture is below a certain threshold.
- After irrigation, the ESP32 goes into **deep sleep mode** for a configurable period to save power.

## 💧 Plant-Specific Configuration

- In the **frontend**, each plant's **moisture threshold** (the minimum moisture level required to activate the relay) and the **check interval** (how often the system checks moisture levels) can be set individually.
- The settings are saved for each plant, and the system will automatically adjust its watering actions based on those settings.
- The **check interval** can now be dynamically set through the web interface, so the time the system waits before checking the moisture level again is customizable per plant.
- Similarly, each plant's **moisture threshold** can be set individually to determine when irrigation should begin.

## 🔌 Arduino Code Summary

The ESP32 firmware does the following:

1. Connects to a Wi-Fi network.
2. Reads the soil moisture sensor value.
3. Converts the raw sensor value to a percentage using calibration values:
   - Dry soil = 3200
   - Wet soil = 1000
4. Sends the moisture value via HTTP POST to the FastAPI server:
   ```
   POST http://<server-ip>:8000/humidity/
   Body: { "value": moisturePercent, "plant_id": plant_id }
   ```
5. If the soil is too dry, it activates the water pump using a relay.
6. The pump runs until the soil reaches sufficient moisture.
7. Disconnects from Wi-Fi and enters **deep sleep for a configurable period**.

## ⚙️ How to Run the Project

Requirements:

- Docker and Docker Compose
- Git

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
docker-compose up --build
```

- Access the **frontend locally**:  
  👉 http://localhost:5173

## 🌐 Access from Another Device on the Network

To access the web dashboard from another device on the same network:

1. Get your local IP address (e.g., `192.168.0.10`)
2. On your phone or another computer, open:  
   👉 `http://<your-ip>:5173`

✅ The frontend will automatically detect and communicate with the backend server on the correct IP.

> ℹ️ Note: This system is only accessible inside your local network by default.

## 📂 Arduino Script

Here is the script running on the ESP32:

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <cstring>

const char* ssid = "<ssid>"; // Replace with your Wi-Fi SSID
const char* password = "<password>"; // Replace with your Wi-Fi password

const char* postURL = "http://<server-ip>:8000/humidity/";
const char* plantBaseURL = "http://<server-ip>:8000/plant/"; // plant ID registered in the plant table

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
    int plant_id = <id>; // Replace <id> with the actual plant ID
    Plant plant = fetchPlant(plant_id); // Replace <id> with the actual plant ID

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

    String jsonData = "{"value": " + String(moisturePercent) + ", "plant_id": " + String(plant_id) + "}";
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

  Serial.println("Entering Deep Sleep for configurable interval...");
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
```

---

Happy gardening! 🌱💧
