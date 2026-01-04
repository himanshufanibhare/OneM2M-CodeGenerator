"""
ESP8266 code generator for oneM2M - Simplified based on working test code.
"""


def generate_esp8266_code(config):
    """Generate ESP8266 code for oneM2M operations.

    Produces minimal GET and POST sketches similar to the testing examples.
    """
    # Extract configuration
    cse_url = config.get('cse_url', 'onem2m.iiit.ac.in')
    port = config.get('port', 443)
    protocol = config.get('protocol', 'https').lower()
    ae_name = config.get('ae_name', '')
    container_name = config.get('container_name', '')
    origin = config.get('origin', '')
    operation = (config.get('operation') or 'POST').upper()
    params = config.get('parameters', []) or []
    labels = config.get('labels', []) or []
    wifi_ssid = config.get('wifi_ssid', '').strip() or 'YOUR_WIFI_SSID'
    wifi_password = config.get('wifi_password', '').strip() or 'YOUR_WIFI_PASSWORD'

    use_ssl = protocol == 'https'
    base_url = f"{protocol}://{cse_url}:{port}"

    # Build ArduinoJson field assignments for POST
    json_assignments = ""
    if isinstance(params, list):
        for p in params:
            if not isinstance(p, dict):
                continue
            name = p.get('name')
            dtype = (p.get('type') or 'string').lower()
            default = p.get('default', '')
            if not name:
                continue
            if dtype in ('string', 'text'):
                json_assignments += f'  innerDoc["{name}"] = "{default}";\n'
            elif dtype in ('int', 'integer'):
                json_assignments += f'  innerDoc["{name}"] = {default or 0};\n'
            elif dtype in ('float', 'decimal'):
                json_assignments += f'  innerDoc["{name}"] = {default or 0.0};\n'
            elif dtype in ('boolean', 'bool'):
                val = 'true' if str(default).lower() in ('1', 'true', 'yes') else 'false'
                json_assignments += f'  innerDoc["{name}"] = {val};\n'

    # Build labels code
    labels_code = ""
    if labels:
        for i, label in enumerate(labels):
            labels_code += f'  cinDoc["m2m:cin"]["lbl"][{i}] = "{label}";\n'

    # Generate minimal GET sketch
    if operation == 'GET':
        code = f'''/*
 * ESP8266 - oneM2M GET Operation (NO SSL)
 * Target: {base_url}/~/in-cse/in-name/{ae_name}/{container_name}/Data/la
 * Protocol: {protocol.upper()}
 * NOTE:
 * - Uses HTTP only
 * - Assumes server allows HTTP access
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

// ---------- WiFi credentials ----------
const char* ssid     = "{wifi_ssid}";
const char* password = "{wifi_password}";


// ---------- oneM2M Server ----------
const char* server = "{protocol}://{cse_url}:{port}";
const char* resourcePath = "/~/in-cse/in-name/{ae_name}/{container_name}/Data/la";

// Authentication
const char* origin = "{origin}";

// ---------- Objects ----------
WiFiClient wifiClient;
HTTPClient http;

// ---------- WiFi Connect ----------
void connectWiFi() {{
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {{
    delay(500);
    Serial.print(".");
  }}

  Serial.println("\\nWiFi connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}}

void setup() {{
  Serial.begin(115200);
  connectWiFi();
}}

void loop() {{
  getOneM2MData();
  delay(10000);
}}

// ---------- oneM2M GET ----------
void getOneM2MData() {{

  if (WiFi.status() != WL_CONNECTED) {{
    Serial.println("WiFi lost. Reconnecting...");
    WiFi.disconnect();
    connectWiFi();
    return;
  }}

  String url = String(server) + resourcePath;

  Serial.println("\\nSending GET request...");
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

  if (httpCode == 200) {{

    StaticJsonDocument<512> doc;
    DeserializationError err = deserializeJson(doc, payload);

    if (err) {{
      Serial.print("JSON parse error: ");
      Serial.println(err.c_str());
    }} else {{
      const char* con = doc["m2m:cin"]["con"];

      if (con) {{
        Serial.print("✅ con value: ");
        Serial.println(con);
      }} else {{
        Serial.println("❌ con not found");
      }}
    }}
  }} else {{
    Serial.println("GET request failed");
  }}

  http.end();
}}
'''
        return code

    # Generate POST sketch
    code = f'''/*
 * ESP8266 - oneM2M POST Operation (NO SSL)
 * Target: {base_url}/~/in-cse/in-name/{ae_name}/{container_name}/Data
 * Protocol: {protocol.upper()}
 * NOTE:
 * - Uses HTTP only
 * - Assumes server allows HTTP access
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

// ---------- WiFi credentials ----------
const char* ssid     = "{wifi_ssid}";
const char* password = "{wifi_password}";

// ---------- oneM2M Server ----------
const char* server = "{protocol}://{cse_url}:{port}";
const char* resourcePath = "/~/in-cse/in-name/{ae_name}/{container_name}/Data";

// Authentication
const char* origin = "{origin}";

// ---------- Objects ----------
WiFiClient wifiClient;
HTTPClient http;

// ---------- WiFi Connect ----------
void connectWiFi() {{
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {{
    delay(500);
    Serial.print(".");
  }}

  Serial.println("\\nWiFi connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}}

void setup() {{
  Serial.begin(9600);
  connectWiFi();
}}

void loop() {{
  postOneM2MData();
  delay(10000);
}}

// ---------- oneM2M POST ----------
void postOneM2MData() {{

  if (WiFi.status() != WL_CONNECTED) {{
    Serial.println("WiFi lost. Reconnecting...");
    WiFi.disconnect();
    connectWiFi();
    return;
  }}

  // Build inner JSON data using ArduinoJson
  StaticJsonDocument<256> innerDoc;
{json_assignments}
  
  // Serialize inner data to string
  String innerJson;
  serializeJson(innerDoc, innerJson);
  
  // Build oneM2M cin payload
  StaticJsonDocument<512> cinDoc;
{labels_code}  cinDoc["m2m:cin"]["con"] = innerJson;
  
  String payload;
  serializeJson(cinDoc, payload);
  
  // Construct the full URL
  String url = String(server) + resourcePath;

  Serial.println("\\nSending POST request...");
  Serial.println("URL: " + url);

  http.begin(wifiClient, url);
  http.addHeader("X-M2M-Origin", origin);
  http.addHeader("Content-Type", "application/json;ty=4");
  
  int httpCode = http.POST(payload);
  String response = http.getString();
  
  Serial.print("HTTP Code: ");
  Serial.println(httpCode);
  Serial.println("Response:");
  Serial.println(response);
  
  if (httpCode == 201) {{
    Serial.println("✅ POST successful");
  }} else {{
    Serial.println("❌ POST failed");
  }}
  
  http.end();
}}
'''
    
    return code
