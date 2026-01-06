"""
Arduino Nano 33 IoT code generator for oneM2M - Simplified based on working test code.
"""


def generate_arduino_code(config):
    """Generate Arduino Nano 33 IoT code for oneM2M operations.
    
    Generates production-ready code that:
    - Dynamically builds oneM2M URL path ending with /Data
    - Auto-selects WiFiClient (HTTP) or WiFiSSLClient (HTTPS) based on protocol
    - Uses ArduinoJson for JSON payload construction
    - Includes all mandatory oneM2M headers
    
    Args:
        config: Dictionary with protocol, cse_url, port, ae_name, container_name, 
                origin, operation, parameters
        
    Returns:
        String containing complete Arduino sketch
    """
    # Extract configuration
    cse_url = config.get('cse_url', '')
    port = config.get('port', '8080')
    protocol = config.get('protocol', 'http').lower()
    ae_name = config.get('ae_name', '')
    container_name = config.get('container_name', '')
    origin = config.get('origin', '')
    operation = config.get('operation', 'post').upper()
    params = config.get('parameters', [])
    labels = config.get('labels', [])
    wifi_ssid = config.get('wifi_ssid', '').strip() or 'YOUR_WIFI_SSID'
    wifi_password = config.get('wifi_password', '').strip() or 'YOUR_WIFI_PASSWORD'
    
    # Auto-select WiFi client based on protocol
    use_ssl = protocol == 'https'
    
    # Build labels array for ArduinoJson
    labels_code = ""
    if labels:
        for i, label in enumerate(labels):
            labels_code += f'  cinDoc["m2m:cin"]["lbl"][{i}] = "{label}";\n'
    client_type = "WiFiSSLClient" if use_ssl else "WiFiClient"
    
    # Build base URL for comments
    base_url = f"{protocol}://{cse_url}:{port}"
    
    # Build array of values (no labels) - [epoch, value1, value2, ...]
    value_list = []
    if isinstance(params, list):
        for p in params:
            name = p.get('name') if isinstance(p, dict) else None
            dtype = (p.get('type') if isinstance(p, dict) else None) or 'string'
            default = p.get('default') if isinstance(p, dict) else ''
            if not name:
                continue
            if dtype in ('string', 'text'):
                value_list.append(f'"{default}"')
            elif dtype in ('int', 'integer'):
                value_list.append(str(default))
            elif dtype in ('float', 'decimal'):
                value_list.append(str(default))
            elif dtype in ('boolean', 'bool'):
                val = '1' if str(default).lower() in ('1', 'true', 'yes') else '0'
                value_list.append(val)
    
    values_str = ', " + String(' + ') + ", " + String('.join(value_list) + ')' if value_list else ''

    
    # If GET operation requested, produce minimal GET sample
    if operation == 'GET':
        code = f'''/*
 * Arduino Nano 33 IoT - oneM2M GET Operation
 * Target: {base_url}/~/in-cse/in-name/{ae_name}/{container_name}/Data/la
 * Protocol: {protocol.upper()}
 */

#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>

// ---------- WiFi ----------
const char* ssid     = "{wifi_ssid}";
const char* password = "{wifi_password}";


// ---------- oneM2M ----------
const char* server = "{cse_url}";
const int   port   = {port};

// MUST end with /la
const char* resourcePath = "/~/in-cse/in-name/{ae_name}/{container_name}/Data/la";

// oneM2M credentials
const char* origin = "{origin}";

// ---------- Clients ----------
{client_type} wifi;
HttpClient client(wifi, server, port);

void setup() {{
  Serial.begin(115200);
  while (!Serial);

  connectWiFi();
}}

void loop() {{
  getOneM2MData();
  delay(10000);
}}

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

// ---------- oneM2M GET ----------
void getOneM2MData() {{

  if (WiFi.status() != WL_CONNECTED) {{
    Serial.println("WiFi disconnected");
    return;
  }}

  Serial.println("\\nSending GET request...");

  client.beginRequest();
  client.get(resourcePath);
  client.sendHeader("X-M2M-Origin", origin);
  client.sendHeader("Accept", "application/json");
  client.endRequest();

  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("HTTP Status: ");
  Serial.println(statusCode);

  if (statusCode != 200) {{
    Serial.println("GET failed");
    Serial.println(response);
    return;
  }}

  // Print raw JSON
  Serial.println("Raw JSON:");
  Serial.println(response);

  // ---------- Parse JSON ----------
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, response);

  if (error) {{
    Serial.print("JSON error: ");
    Serial.println(error.c_str());
    return;
  }}

  const char* con = doc["m2m:cin"]["con"];

  if (!con) {{
    Serial.println("con not found");
    return;
  }}

  Serial.print("✅ con value: ");
  Serial.println(con);
}}
'''

        return code

    # POST fallback: original POST generation
    code = f'''/*
 * Arduino Nano 33 IoT - oneM2M POST Operation
 * Target: {base_url}/~/in-cse/in-name/{ae_name}/{container_name}/Data
 * Protocol: {protocol.upper()}
 */

#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>

// ---------- WiFi ----------
const char* ssid     = "{wifi_ssid}";
const char* password = "{wifi_password}";

// ---------- oneM2M ----------
const char* server = "{cse_url}";
const int   port   = {port};
const char* resourcePath = "/~/in-cse/in-name/{ae_name}/{container_name}/Data";

// oneM2M credentials
const char* origin = "{origin}";

// ---------- Clients ----------
{client_type} wifi;
HttpClient client(wifi, server, port);

void setup() {{
  Serial.begin(115200);
  while (!Serial);
  
  connectWiFi();
}}

void loop() {{
  postOneM2MData();
  delay(10000);
}}

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

// ---------- oneM2M POST ----------
void postOneM2MData() {{
  
  if (WiFi.status() != WL_CONNECTED) {{
    Serial.println("WiFi disconnected");
    return;
  }}
  
  Serial.println("\\nSending POST request...");
  
  // Build data array: [epoch, value1, value2, ...]
  unsigned long epoch = millis() / 1000; // Seconds since boot (use RTC for actual time)
  String dataArray = "[" + String(epoch){values_str} + "]";
  
  // Build oneM2M cin payload
  StaticJsonDocument<512> cinDoc;
{labels_code}  cinDoc["m2m:cin"]["con"] = dataArray;
  
  String payload;
  serializeJson(cinDoc, payload);
  
  // Send POST request
  client.beginRequest();
  client.post(resourcePath);
  client.sendHeader("X-M2M-Origin", origin);
  client.sendHeader("Content-Type", "application/json;ty=4");
  client.sendHeader("Content-Length", payload.length());
  client.beginBody();
  client.print(payload);
  client.endRequest();
  
  int statusCode = client.responseStatusCode();
  String response = client.responseBody();
  
  Serial.print("HTTP Status: ");
  Serial.println(statusCode);
  
  if (statusCode == 201) {{
    Serial.println("✅ POST successful");
  }} else {{
    Serial.println("POST failed");
    Serial.println(response);
  }}
}}
'''
    
    return code
