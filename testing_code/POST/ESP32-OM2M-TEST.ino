#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* ssid = "myssid";
const char* password = "password";

// OneM2M server details
const char* server = "http://dev-onem2m.iiit.ac.in:443";
const char* resourcePath = "/~/in-cse/in-name/AE-WN/WN-KH04-05/Data";

// LED pin for status indication
#define LED_PIN 2  // Use GPIO2 for the built-in LED on most ESP32 boards

WiFiClient wifiClient;
HTTPClient http;

void setup() {
  // Start Serial for debugging
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
}

void loop() {
  // Prepare the payload
  String payload = R"(
  {
      "m2m:cin": {
          "lbl": [
              "AE-EM",
              "EM-CR-KH95-00",
              "V2.0.0",
              "EM-V2.0.0"
          ],
          "con": "[1736574818, 7053,2,3,4,5,6,7]"
      }
  }
  )";

  // Construct the full URL
  String url = String(server) + resourcePath;

  // Debugging: Show URL and payload
  Serial.println("Sending POST request to oneM2M...");
  Serial.println("URL: " + url);
  Serial.println("Payload: " + payload);

  // Send the POST request
  if (WiFi.status() == WL_CONNECTED) {
    http.begin(wifiClient, url);  // Initialize HTTP client without SSL verification
    http.addHeader("X-M2M-Origin", "Tue_20_12_22:Tue_20_12_22");  // Add headers
    http.addHeader("Content-Type", "application/json;ty=4");

    int httpResponseCode = http.POST(payload);  // Send POST request
    String response = http.getString();        // Get the response

    // Debugging: Print response
    Serial.print("HTTP Response Code: ");
    Serial.println(httpResponseCode);
    Serial.println("Response: ");
    Serial.println(response);

    // Indicate success or failure with the LED
    if (httpResponseCode == 201) {
      Serial.println("Data successfully sent to oneM2M.");
      digitalWrite(LED_PIN, HIGH);
      delay(500);
      digitalWrite(LED_PIN, LOW);
    } else {
      Serial.println("Failed to send data to oneM2M.");
    }

    http.end();  // Close the connection
  } else {
    Serial.println("WiFi not connected.");
  }

  delay(10000);  // Wait 10 seconds before sending again
}
