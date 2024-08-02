#include "config.h"
#include "sensor.h"
#include "wireless.h"
#include "data_logger.h"
#include <ArduinoJson.h>

char buffer[256];  // Buffer to hold JSON data

void setup() {
  Serial.begin(115200);
  setupWiFi();
  setupSD();
  setupSensors();
}

void loop() {
  // Read sensors
  float temperature = readTemperature();
  float humidity = readHumidity();

  // Check if any reads failed and exit early (to try again).
  if (isnan(temperature) || isnan(humidity) || moisture == -1) {
    Serial.println("Failed to read from sensors!");
    delay(60000);  // Retry after 60 seconds
    return;
  }

  // Create JSON object
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["uuid"] = UUID;
  jsonDoc["temperature"] = temperature;
  jsonDoc["humidity"] = humidity;
  serializeJson(jsonDoc, buffer);

  // Try to send data wirelessly
  if (sendToServer(buffer)) {
    Serial.println("Data sent successfully");
  } else {
    // If sending fails, log to SD card
    logToSD(buffer);
  }

  // Wait a while before the next loop
  delay(60000);  // Send data every 60 seconds
}
