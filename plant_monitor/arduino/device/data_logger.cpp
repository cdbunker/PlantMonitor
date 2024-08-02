#include "data_logger.h"
#include <SPI.h>
#include <SD.h>
#include "config.h"

File dataFile;

void setupSD() {
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Card failed, or not present");
  } else {
    Serial.println("Card initialized.");
  }
}

void logToSD(const char* data) {
  dataFile = SD.open("datalog.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println(data);
    dataFile.close();
    Serial.println("Data logged to SD");
  } else {
    Serial.println("Error opening datalog.txt");
  }
}
