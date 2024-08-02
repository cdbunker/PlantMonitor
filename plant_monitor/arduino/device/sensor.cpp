#include "sensor.h"
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_SHT31.h>
#include "config.h"

DHT dht(DHTPIN, DHTTYPE);
Adafruit_SHT31 sht30 = Adafruit_SHT31();

void setupSensors() {
  if (sensorType == SENSOR_DHT22) {
    dht.begin();
  } else if (sensorType == SENSOR_SHT30) {
    if (!sht30.begin(SHT30_ADDRESS)) {
      Serial.println("Couldn't find SHT30");
      while (1) delay(1);
    }
  }
}

float readTemperature() {
  if (sensorType == SENSOR_DHT22) {
    return dht.readTemperature();
  } else if (sensorType == SENSOR_SHT30) {
    return sht30.readTemperature();
  }
  return NAN;
}

float readHumidity() {
  if (sensorType == SENSOR_DHT22) {
    return dht.readHumidity();
  } else if (sensorType == SENSOR_SHT30) {
    return sht30.readHumidity();
  }
  return NAN;
}
