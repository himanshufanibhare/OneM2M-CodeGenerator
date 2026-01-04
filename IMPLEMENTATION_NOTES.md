# oneM2M Code Generator - Implementation Notes

## Overview
This document describes the implementation of HTTP/HTTPS protocol support and oneM2M-compliant code generation for the CODE_GENERATOR application.

## Key Features Implemented

### 1. Protocol Selection (HTTP/HTTPS)
- **Frontend**: Added protocol dropdown in [configure.html](backend/templates/configure.html)
  - Auto-selects port 443 for HTTPS, 8080 for HTTP
  - Validates protocol-port combinations
  - Sends protocol field to backend

- **Backend**: Updated [app.py](backend/app.py) validation
  - Accepts protocol parameter from config
  - Enforces protocol-port rules (port 443 requires HTTPS)
  - Warns if HTTPS uses non-standard ports

### 2. ArduinoJson Integration (Microcontrollers)
All microcontroller generators now use **ArduinoJson** library instead of manual string building:

- **Arduino Nano 33 IoT** ([arduino.py](backend/controllers/arduino.py))
  - Uses `StaticJsonDocument<128>` for inner data
  - Uses `StaticJsonDocument<256>` for cin wrapper
  - Selects `WiFiClient` (HTTP) or `WiFiSSLClient` (HTTPS)

- **ESP32** ([esp32.py](backend/controllers/esp32.py))
  - Uses ArduinoJson for all JSON operations
  - Selects `WiFiClient` (HTTP) or `WiFiClientSecure` (HTTPS)
  - Includes `client.setInsecure()` for HTTPS (certificate validation can be added)

- **ESP8266** ([esp8266.py](backend/controllers/esp8266.py))
  - Uses ArduinoJson library
  - Selects `WiFiClient` (HTTP) or `WiFiClientSecure` (HTTPS)
  - Includes `client.setInsecure()` for HTTPS

### 3. Python Generator ([python_controller.py](backend/controllers/python_controller.py))
- Uses `requests` library with proper timeout (10 seconds)
- Supports HTTP and HTTPS with `verify` parameter
- Includes comprehensive error handling (Timeout, ConnectionError, RequestException)
- Stringifies inner JSON for con field

### 4. oneM2M Compliance

All generators now include **mandatory oneM2M headers**:
- `X-M2M-Origin`: Authentication/authorization identifier
- `X-M2M-RI`: Unique Request Identifier (UUID or timestamp-based)
- `Content-Type: application/json;ty=4`: Content Instance type
- `Accept: application/json`: Response format

**Critical payload structure**:
```json
{
  "m2m:cin": {
    "con": "<STRINGIFIED_JSON>"  // con MUST be a string, NOT an object
  }
}
```

### 5. Microcontroller Payload Generation Pattern

**Using ArduinoJson** (all platforms):
```cpp
// Build inner JSON data
StaticJsonDocument<128> innerDoc;
innerDoc["temperature"] = 25.5;
innerDoc["humidity"] = 60;

// Serialize to string
String innerJson;
serializeJson(innerDoc, innerJson);

// Build cin payload - con is the stringified JSON
StaticJsonDocument<256> cinDoc;
cinDoc["m2m:cin"]["con"] = innerJson;  // con MUST be string

String payload;
serializeJson(cinDoc, payload);
```

### 6. Python Payload Generation Pattern

```python
# Build inner data
inner = {
    "temperature": temperature,
    "humidity": humidity
}

# Build cin payload - con is stringified inner dict
payload = {
    'm2m:cin': {
        'con': json.dumps(inner)  # con MUST be string
    }
}
```

## Required Libraries

### Arduino Nano 33 IoT
- `WiFiNINA.h` - WiFi connectivity
- `ArduinoJson.h` - JSON serialization
- (HTTPS) `WiFiSSLClient` included in WiFiNINA

### ESP32
- `WiFi.h` - WiFi connectivity
- `HTTPClient.h` - HTTP/HTTPS requests
- `WiFiClientSecure.h` - HTTPS support
- `ArduinoJson.h` - JSON serialization

### ESP8266
- `ESP8266WiFi.h` - WiFi connectivity
- `ESP8266HTTPClient.h` - HTTP/HTTPS requests
- `WiFiClientSecure.h` - HTTPS support
- `ArduinoJson.h` - JSON serialization

### Python
- `requests` - HTTP/HTTPS client
- `json` - JSON serialization (built-in)
- `uuid` - Request ID generation (built-in)

## Installation Instructions

### ArduinoJson Library
Install via Arduino IDE Library Manager:
1. Sketch → Include Library → Manage Libraries
2. Search "ArduinoJson"
3. Install version 6.x or later

Or via PlatformIO:
```ini
lib_deps = bblanchon/ArduinoJson@^6.21.0
```

### Python Dependencies
```bash
pip install requests
```

## Security Considerations

### HTTPS Certificate Validation

**Current implementation** (development):
- ESP32: `client.setInsecure()` - skips certificate validation
- ESP8266: `client.setInsecure()` - skips certificate validation
- Python: `verify=True` - validates certificates by default

**Production recommendations**:
- **ESP32**: Use `client.setCACert(root_ca)` with server's CA certificate
- **ESP8266**: Use `client.setFingerprint(fingerprint)` with server's certificate fingerprint
- **Arduino Nano 33 IoT**: Use `client.setCACert()` if supported
- **Python**: Set `verify="/path/to/ca-bundle.crt"` for custom CA or corporate proxies

## Testing

### Test Configuration
1. Select controller (Arduino/ESP32/ESP8266/Python)
2. Configure server:
   - Protocol: HTTP or HTTPS
   - Host: CSE hostname (e.g., `onem2m.example.com`)
   - Port: 443 (HTTPS) or 8080 (HTTP)
3. Configure oneM2M resources:
   - AE Name: Application Entity identifier
   - Container Name: Data container
   - Origin: Authentication credentials
4. Add parameters (temperature, humidity, etc.)
5. Generate code

### Expected Output (Example)

**Arduino HTTP Request**:
```
POST /~/in-cse/in-name/MyAE/MyContainer HTTP/1.1
Host: 192.168.1.100
X-M2M-Origin: admin:admin
X-M2M-RI: req-123456
Content-Type: application/json;ty=4
Accept: application/json
Content-Length: 78

{"m2m:cin":{"con":"{\"temperature\":25.5,\"humidity\":60}"}}
```

## Validation Rules

### Backend Validation ([app.py](backend/app.py))
- CSE host must NOT include protocol (no `http://` or `https://`)
- Port must be 1-65535
- Port 443 requires HTTPS protocol
- HTTPS with non-standard ports shows warning
- Microcontrollers cannot use localhost

### Frontend Validation ([configure.html](backend/templates/configure.html))
- All required fields must be filled
- Protocol is mandatory
- Auto-strips `http://` and `https://` from host input

## File Structure
```
backend/
├── app.py                          # Main Flask application with validation
├── controllers/
│   ├── __init__.py                 # Module initialization
│   ├── arduino.py                  # Arduino Nano 33 IoT generator (ArduinoJson)
│   ├── esp32.py                    # ESP32 generator (ArduinoJson)
│   ├── esp8266.py                  # ESP8266 generator (ArduinoJson)
│   ├── python_controller.py        # Python generator (requests + json)
│   └── utils.py                    # Shared utilities (legacy helpers)
├── templates/
│   ├── controller_select.html      # Controller selection page
│   ├── configure.html              # Configuration form (with protocol dropdown)
│   └── generate.html               # Generated code view
frontend/
├── src/
│   ├── components/                 # React components (if applicable)
│   ├── pages/                      # Frontend pages
│   └── styles/                     # CSS stylesheets
```

## Known Issues & Limitations

1. **Certificate validation disabled by default** on ESP32/ESP8266 for development
2. **X-M2M-RI uses timestamp/millis()** instead of true UUID on microcontrollers (UUID library adds significant code size)
3. **WiFi credentials hardcoded** in generated sketches (users must replace before uploading)
4. **No retry logic** on microcontroller HTTP failures (single-shot requests)

## Future Enhancements

1. **Certificate management UI** for uploading CA certificates
2. **WiFi credential injection** via compile-time defines or config portal
3. **Retry/backoff logic** for failed oneM2M requests
4. **Response parsing** and error handling based on oneM2M response codes
5. **Support for other operations** (retrieve, update, delete) beyond Content Instance creation

## References

- **oneM2M Specification**: [oneM2M.org](https://www.onem2m.org)
- **ArduinoJson Documentation**: [arduinojson.org](https://arduinojson.org)
- **WiFiNINA Library**: [Arduino WiFiNINA](https://www.arduino.cc/en/Reference/WiFiNINA)
- **ESP32 Arduino Core**: [ESP32 Arduino](https://github.com/espressif/arduino-esp32)
- **ESP8266 Arduino Core**: [ESP8266 Arduino](https://github.com/esp8266/Arduino)
