#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22      // AM2302 uses the DHT22 protocol

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  Serial.println("AM2302 Sensor Ready");
}

void loop() {
  delay(2000); // AM2302 sampling rate is 0.5Hz — 2s minimum

  float humidity     = dht.readHumidity();
  float temperatureC = dht.readTemperature();
  float temperatureF = dht.readTemperature(true);

  if (isnan(humidity) || isnan(temperatureC) || isnan(temperatureF)) {
    Serial.println("Failed to read from AM2302 sensor!");
    return;
  }

  Serial.print("Humidity: ");
  Serial.print(humidity, 1);
  Serial.print(" %  |  Temp: ");
  Serial.print(temperatureC, 1);
  Serial.print(" °C  |  ");
  Serial.print(temperatureF, 1);
  Serial.println(" °F");
}