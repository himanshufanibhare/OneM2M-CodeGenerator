"""
ESP32 code generator for oneM2M - Simplified based on working test code.
"""


def generate_esp32_code(config):
        """Generate ESP32 code for oneM2M operations.

        Produces minimal GET and POST sketches that match the examples in
        `testing_code/GET` and `testing_code/POST`.
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

        # Build array of values (no labels) - [epoch, value1, value2, ...]
        value_list = []
        if isinstance(params, list):
                for p in params:
                        if not isinstance(p, dict):
                                continue
                        dtype = (p.get('type') or 'string').lower()
                        default = p.get('default', '')
                        name = p.get('name')
                        if not name:
                                continue
                        if dtype in ('string', 'text'):
                                value_list.append(f'"{default}"')
                        elif dtype in ('int', 'integer'):
                                value_list.append(str(default or 0))
                        elif dtype in ('float', 'decimal'):
                                value_list.append(str(default or 0.0))
                        elif dtype in ('boolean', 'bool'):
                                val = '1' if str(default).lower() in ('1', 'true', 'yes') else '0'
                                value_list.append(val)
        
        values_str = ', " + String(' + ') + ", " + String('.join(value_list) + ')' if value_list else ''

        # Build labels code
        labels_code = ""
        if labels:
                for i, label in enumerate(labels):
                        labels_code += f'  cinDoc["m2m:cin"]["lbl"][{i}] = "{label}";\n'

        # Generate minimal GET sketch
        if operation == 'GET':
                code = f'''/*
 * ESP32 - oneM2M GET Operation
 * Target: {base_url}/~/in-cse/in-name/{ae_name}/{container_name}/Data/la
 * Protocol: {protocol.upper()}
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid     = "{wifi_ssid}";
const char* password = "{wifi_password}";


// oneM2M Server Configuration
const char* server = "{protocol}://{cse_url}:{port}";
const char* resourcePath = "/~/in-cse/in-name/{ae_name}/{container_name}/Data/la";
HTTPClient http;
String url = String(server) + resourcePath;

// Authentication
const char* origin = "{origin}";

// ---------- WiFi Handling ----------
void connectWiFi() {{
    Serial.print("Connecting to WiFi");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) 
    {{
        delay(500);
        Serial.print(".");
    }}
    Serial.println("\\nWiFi connected");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}}

// ---------- Setup ----------
void setup() {{
    Serial.begin(115200);
    connectWiFi();
}}

// ---------- Loop ----------
void loop() {{
    getOneM2MData();
    delay(10000);
}}

// ---------- oneM2M GET ----------
void getOneM2MData()
{{
    if (WiFi.status() != WL_CONNECTED)
    {{
        Serial.println("WiFi lost. Reconnecting...");
        WiFi.disconnect();
        connectWiFi();
    }}

    http.begin(url);
    http.addHeader("X-M2M-Origin", origin);
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.GET();
    String payload = http.getString();

    Serial.print("HTTP Code: ");
    Serial.println(httpCode);
    Serial.println("Response Payload:");
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
    }}

    http.end();
}}
'''
                return code

        # Generate POST sketch
        code = f'''/*
 * ESP32 - oneM2M POST Operation
 * Target: {base_url}/~/in-cse/in-name/{ae_name}/{container_name}/Data
 * Protocol: {protocol.upper()}
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "{wifi_ssid}";
const char* password = "{wifi_password}";

// oneM2M Server Configuration
const char* server = "{protocol}://{cse_url}:{port}";
const char* resourcePath = "/~/in-cse/in-name/{ae_name}/{container_name}/Data";
HTTPClient http;
String url = String(server) + resourcePath;

// Authentication
const char* origin = "{origin}";

// ---------- WiFi Handling ----------
void connectWiFi() {{
    Serial.print("Connecting to WiFi");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) 
    {{
        delay(500);
        Serial.print(".");
    }}
    Serial.println("\\nWiFi connected");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}}

// ---------- Setup ----------
void setup() {{
    Serial.begin(115200);
    connectWiFi();
}}

// ---------- Loop ----------
void loop() {{
    postOneM2MData();
    delay(10000);
}}

// ---------- oneM2M POST ----------
void postOneM2MData()
{{
    if (WiFi.status() != WL_CONNECTED)
    {{
        Serial.println("WiFi lost. Reconnecting...");
        WiFi.disconnect();
        connectWiFi();
    }}

    // Build data array: [epoch, value1, value2, ...]
    unsigned long epoch = millis() / 1000; // Seconds since boot (use RTC for actual time)
    String dataArray = "[" + String(epoch){values_str} + "]";

    // Build oneM2M cin payload
    StaticJsonDocument<512> cinDoc;
{labels_code}  cinDoc["m2m:cin"]["con"] = dataArray;

    String payload;
    serializeJson(cinDoc, payload);

    http.begin(url);
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
