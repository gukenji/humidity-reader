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
