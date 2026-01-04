#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>

// ---------- WiFi ----------
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ---------- oneM2M ----------
const char* server = "onem2m.iiit.ac.in";
const int   port   = 443;

// MUST end with /la
const char* resourcePath =
"/~/in-cse/in-name/AE-SL/SL-PL96-00/Data/la";

// oneM2M credentials
const char* origin = "iiith_guest:iiith_guest";

// ---------- Clients ----------
WiFiClient wifi;
HttpClient client(wifi, server, port);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  connectWiFi();
}

void loop() {
  getOneM2MData();
  delay(10000);
}

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

// ---------- oneM2M GET ----------
void getOneM2MData() {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected");
    return;
  }

  Serial.println("\nSending GET request...");

  client.beginRequest();
  client.get(resourcePath);
  client.sendHeader("X-M2M-Origin", origin);
  client.sendHeader("Accept", "application/json");
  client.endRequest();

  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("HTTP Status: ");
  Serial.println(statusCode);

  if (statusCode != 200) {
    Serial.println("GET failed");
    Serial.println(response);
    return;
  }

  // Print raw JSON
  Serial.println("Raw JSON:");
  Serial.println(response);

  // ---------- Parse JSON ----------
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, response);

  if (error) {
    Serial.print("JSON error: ");
    Serial.println(error.c_str());
    return;
  }

  const char* con = doc["m2m:cin"]["con"];

  if (!con) {
    Serial.println("con not found");
    return;
  }

  Serial.print("✅ con value: ");
  Serial.println(con);
}
