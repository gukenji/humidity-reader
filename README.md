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
- After irrigation, the ESP32 goes into **deep sleep mode for 10 minutes** to save power.

## 🔌 Arduino Code Summary

The ESP32 firmware does the following:

1. Connects to a Wi-Fi network.
2. Reads the soil moisture sensor value.
3. Converts the raw sensor value to a percentage using calibration values:
   - Dry soil = 3200
   - Wet soil = 1000
4. Sends the moisture value via HTTP POST to the FastAPI server:
   ```
   POST http://<ip>/humidity/
   Body: { "value": moisturePercent }
   ```
5. If the soil is too dry (`< 50%`), it activates the water pump using a relay.
6. The pump runs until the soil reaches sufficient moisture (`>= 50%`).
7. Disconnects from Wi-Fi and enters **deep sleep for 10 minutes**.

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

const char* ssid = <ssid>;
const char* password = <password>;

const char* serverURL = "http://<ip>/humidity/";

const int moistureSensorPin = 34;
const int relayPin = 26;
const int moistureThreshold = 50;

int dryValue = 3200;      // Sensor value when soil is dry
int wetValue = 1000;      // Sensor value when soil is wet

void setup() {
  Serial.begin(115200);
  delay(100);  // Short delay to stabilize serial connection

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);  // Turn relay off

  // Connect to Wi-Fi
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

    // Read sensor
    int rawReading = analogRead(moistureSensorPin);
    int moisturePercent = map(rawReading, dryValue, wetValue, 0, 100);
    moisturePercent = constrain(moisturePercent, 0, 100);

    Serial.print("Raw reading: ");
    Serial.print(rawReading);
    Serial.print(" | Moisture: ");
    Serial.print(moisturePercent);
    Serial.println("%");

    // Send data via HTTP POST
    HTTPClient http;
    http.begin(serverURL);
    http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"value\": " + String(moisturePercent) + "}";
    int httpResponseCode = http.POST(jsonData);

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    Serial.println("Payload sent: " + jsonData);

    http.end();

    // Activate pump and keep checking until moisture is sufficient
    if (moisturePercent < moistureThreshold) {
      Serial.println("Soil is dry! Starting irrigation...");

      digitalWrite(relayPin, HIGH);  // Turn pump on

      while (true) {
        delay(5000);  // Wait 5 seconds between readings

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

      digitalWrite(relayPin, LOW);  // Turn pump off
    }

    WiFi.disconnect(true);  // Disconnect to save power
  } else {
    Serial.println("Failed to connect to Wi-Fi");
  }

  // Enter Deep Sleep for 10 minutes
  Serial.println("Entering Deep Sleep for 10 minutes...");
  esp_sleep_enable_timer_wakeup(10 * 60 * 1000000LL); // 10 minutes in microseconds
  esp_deep_sleep_start();
}

void loop() {
  // Will never be called — all logic is in setup()
}
```

---

Happy gardening! 🌱💧
