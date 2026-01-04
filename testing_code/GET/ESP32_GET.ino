/*
 * ESP32 - oneM2M GET Operation
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "myssid";
const char* password = "password";

// oneM2M Server Configuration
const char* server = "http://onem2m.iiit.ac.in:443";
const char* resourcePath = "/~/in-cse/in-name/AE-AQ/AQ-VN90-00/Data/la";
HTTPClient http;
String url = String(server) + resourcePath;

// Authentication
const char* origin = "iiith_guest:iiith_guest";

// ---------- WiFi Handling ----------
void connectWiFi() {
    Serial.print("Connecting to WiFi");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  }

// ---------- Setup ----------
void setup() {
    Serial.begin(115200);
    connectWiFi();
}

// ---------- Loop ----------
void loop() {
    getOneM2MData();
    delay(10000);
}

// ---------- oneM2M GET ----------
void getOneM2MData()
{
    if (WiFi.status() != WL_CONNECTED)
    {
    Serial.println("WiFi lost. Reconnecting...");
    WiFi.disconnect();
    connectWiFi();
    }

    http.begin(url);
    http.addHeader("X-M2M-Origin", origin);
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.GET();
    String payload = http.getString();

    Serial.print("HTTP Code: ");
    Serial.println(httpCode);
    Serial.println("Response Payload:");
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
    }

    http.end();
}
