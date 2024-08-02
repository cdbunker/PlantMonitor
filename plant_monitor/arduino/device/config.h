#ifndef CONFIG_H
#define CONFIG_H

#define DHTPIN 2
#define DHTTYPE DHT22
#define SD_CS_PIN 4
#define SHT30_ADDRESS 0x44 // I2C address for the SHT30

const char* UUID = "UUID";
const char* ssid = "SSID";
const char* password = "PASSWORD";
const char* server_ip = "IP";


enum SensorType {
  SENSOR_DHT22,
  SENSOR_SHT30
};

const SensorType sensorType = SENSOR_DHT22;  // Set to SENSOR_DHT22 or SENSOR_SHT30

#endif
