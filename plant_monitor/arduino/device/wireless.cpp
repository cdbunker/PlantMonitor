#include "wireless.h"
#include <ESP8266WiFi.h>
#include "config.h"

void setupWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

bool sendToServer(const char* data) {
  WiFiClient client;
  if (client.connect(server_ip, 5000)) {
    client.println("POST /receive_data HTTP/1.1");
    client.println("Host: your_server_ip");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(strlen(data));
    client.println();
    client.println(data);
    client.stop();
    return true;
  }
  return false;
}
