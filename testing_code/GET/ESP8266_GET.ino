/*
 * ESP8266 - oneM2M GET Operation (NO SSL)
 * NOTE:
 * - Uses HTTP only
 * - Assumes server allows HTTP access
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

// ---------- WiFi credentials ----------
const char* ssid     = "myssid";
const char* password = "password";

// ---------- oneM2M Server ----------
const char* server = "http://onem2m.iiit.ac.in:443";   // kept same as your POST
const char* resourcePath ="/~/in-cse/in-name/AE-EM/EM-CR-KH95-00/Data/la";

// Authentication
const char* origin = "iiith_guest:iiith_guest";

// ---------- Objects ----------
WiFiClient wifiClient;
HTTPClient http;

// ---------- WiFi Connect ----------
void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(9600);
  connectWiFi();
}

void loop() {
  getOneM2MData();
  delay(10000);
}

// ---------- oneM2M GET ----------
void getOneM2MData() {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi lost. Reconnecting...");
    WiFi.disconnect();
    connectWiFi();
    return;
  }

  String url = String(server) + resourcePath;

  Serial.println("\nSending GET request...");
  Serial.println("URL: " + url);

  http.begin(wifiClient, url);
  http.addHeader("X-M2M-Origin", origin);
  http.addHeader("Accept", "application/json");

  int httpCode = http.GET();
  String payload = http.getString();

  Serial.print("HTTP Code: ");
  Serial.println(httpCode);
  Serial.println("Received payload:");
  Serial.println(payload);

  if (httpCode == 200) {

    StaticJsonDocument<512> doc;
    DeserializationError err = deserializeJson(doc, payload);

    if (err) {
      Serial.print("JSON parse error: ");
      Serial.println(err.c_str());
    } else {
      const char* con = doc["m2m:cin"]["con"];

      if (con) {
        Serial.print("✅ con value: ");
        Serial.println(con);
      } else {
        Serial.println("❌ con not found");
      }
    }
  } else {
    Serial.println("GET request failed");
  }

  http.end();
}
