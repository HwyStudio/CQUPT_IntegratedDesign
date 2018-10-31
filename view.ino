#include <dht11.h>
#include <ESP8266WiFi.h>
#include <Arduino.h>

#define DHT11_PIN 2

dht11 DHT11;
WiFiClient client;

const char* ssid     = "CQUPT_CC";
const char* password = "0987654321";
const char* host = "192.168.1.110";
const int tcpPort = 8889;
String getTarget;

void setup() {
  Serial.begin(9600);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); 
    Serial.println("error");
  }
  while(!client.connect(host,tcpPort));
  Serial.println("connect ok");
}

void loop() {
  while (client.available() > 0) {
    char ch = client.read();
    getTarget += ch;
  }
  
  if (getTarget == "getTemperature") {
    int chk = DHT11.read(DHT11_PIN);
    show(chk);
    int temperature = DHT11.temperature;
    Serial.println(temperature);
    client.print(temperature); 
    getTarget = "";
  } else if (getTarget == "getHumidity") {
    int chk = DHT11.read(DHT11_PIN);
    show(chk);
    int humidity = DHT11.humidity;
    Serial.println(humidity);
    client.print(humidity);
    getTarget = "";
  }

  delay(2000);
}

void show(int chk) {
  switch (chk)
  {
    case 0:  Serial.print("OK,\t"); break;
    case -1: Serial.print("Checksum error,\t"); break;
    case -2: Serial.print("Time out error,\t"); break;
    default: Serial.print("Unknown error,\t"); break;
  }
}

