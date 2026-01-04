# oneM2M Code Generator

A professional web-based code generation tool that creates oneM2M-compliant client code for IoT devices and servers. Generate production-ready code for multiple platforms with a modern, intuitive interface.

## 🚀 Features

### Core Functionality
- **Multi-Platform Support**: Generate code for Arduino Nano 33 IoT, ESP32, ESP8266, and Python
- **Protocol Selection**: HTTP and HTTPS support with automatic port configuration
- **WiFi Configuration**: Built-in WiFi credential management for all microcontrollers
- **Testing Tools**: Optional GET/POST request testing before code generation
- **oneM2M Compliance**: Standard headers, proper JSON structure, and resource paths

### User Experience
- **Multi-Step Workflow**: Clean, intuitive configuration process
- **Real-Time Testing**: Test your oneM2M connection without generating code
- **Live Code Preview**: View generated code with syntax highlighting
- **Easy Export**: Copy to clipboard or download as ready-to-use files
- **Flexible Testing**: Generate code directly or test operations first

## 📋 Requirements

### System Requirements
- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection for library installations

### Python Dependencies
- Flask 3.0.0 - Web framework
- flask-cors 4.0.0 - Cross-Origin Resource Sharing
- requests - HTTP client library (for Python code generation)
- urllib3 - HTTP client (for testing functionality)

### Arduino/ESP Libraries (for generated code)
- **Arduino Nano 33 IoT**: WiFiNINA, ArduinoHttpClient, ArduinoJson
- **ESP32**: WiFi (built-in), HTTPClient, ArduinoJson
- **ESP8266**: ESP8266WiFi, ESP8266HTTPClient, ArduinoJson
- **Python**: requests library

## 🛠️ Installation

### Quick Start (Recommended)

1. **Clone the repository**:
```bash
git clone <repository-url>
cd CODE_GENERATOR
```

2. **Run the start script**:
```bash
chmod +x start.sh
./start.sh
```

The script automatically:
- Creates a virtual environment
- Installs all dependencies
- Starts the Flask server on http://localhost:5000

### Manual Installation

1. **Create virtual environment**:
```bash
python -m venv venv
```

2. **Activate virtual environment**:
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
.\venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r backend/requirements.txt
```

4. **Run the application**:
```bash
cd backend
python app.py
```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## 💻 Usage Guide

### Step-by-Step Workflow

#### 1. **Select Controller Platform**
Navigate to `http://localhost:5000` and choose your target device:
- **Arduino Nano 33 IoT** - WiFiNINA-based microcontroller
- **ESP32** - Powerful dual-core WiFi/Bluetooth SoC
- **ESP8266** - Compact WiFi microcontroller
- **Python** - For PC, Raspberry Pi, or server applications

#### 2. **Configure oneM2M Server Settings**
Enter your oneM2M server configuration:
- **Protocol**: HTTP or HTTPS (auto-selects port 8080 or 443)
- **CSE Base URL**: Your oneM2M server address (e.g., `192.168.1.100` or `onem2m.example.com`)
- **Port**: Server port number (typically 8080 for HTTP, 443 for HTTPS)
- **AE Name**: Application Entity name (your application identifier)
- **Container Name**: Data container name
- **X-M2M-Origin**: Authentication credentials (e.g., `admin:admin`)

#### 3. **Configure WiFi Credentials** (Microcontrollers only)
For Arduino, ESP32, and ESP8266:
- **WiFi SSID**: Your WiFi network name
- **WiFi Password**: Your WiFi password

These credentials are embedded in the generated code for automatic connection.

#### 4. **Define Data Parameters**
Configure the data structure you want to send/receive:
- **Number of Parameters**: How many data fields (1-10)
- For each parameter:
  - **Parameter Name**: Variable name (e.g., `temperature`, `humidity`)
  - **Data Type**: `int`, `float`, `string`, or `boolean`
  - **Default Value**: Initial/example value

#### 5. **Select Operation Type**
Choose the oneM2M operation:
- **POST Request**: Send data to the oneM2M server (create Content Instance)
- **GET Request**: Retrieve the latest data from the server

#### 6. **Optional Testing**
Before generating code, you can test the connection:
- Click **"Test GET Request"** or **"Test POST Request"**
- View the response from your oneM2M server
- Verify your configuration is correct
- Testing is optional - you can skip directly to generation

#### 7. **Generate Code**
Click **"Generate Code"** to create your custom client:
- View the complete, ready-to-use code
- Includes all libraries, setup, loop, and helper functions
- WiFi credentials pre-configured
- Server settings embedded

#### 8. **Export Your Code**
- **Copy**: Click "Copy" button to copy code to clipboard
- **Download**: Click "Download File" to save as `.ino` (Arduino) or `.py` (Python)
- **Generate New**: Start over with different settings

## 📁 Project Structure

```
CODE_GENERATOR/
├── backend/
│   ├── app.py                          # Flask application & API routes
│   ├── requirements.txt                # Python dependencies
│   │
│   ├── controllers/                    # Code generation modules
│   │   ├── __init__.py                # Controller exports
│   │   ├── arduino.py                 # Arduino Nano 33 IoT generator
│   │   ├── esp32.py                   # ESP32 generator
│   │   ├── esp8266.py                 # ESP8266 generator
│   │   ├── python_controller.py       # Python generator
│   │   └── utils.py                   # Shared utilities
│   │
│   ├── static/
│   │   └── style.css                  # Application styling
│   │
│   └── templates/                      # HTML templates
│       ├── controller_select.html     # Platform selection page
│       ├── configure.html             # Configuration & testing page
│       └── generate.html              # Code preview & download page
│
├── testing_code/                       # Example test files
│   ├── GET/                           # Working GET examples
│   │   ├── ESP32_GET.ino
│   │   ├── ESP8266_GET.ino
│   │   ├── NANO33_GET.ino
│   │   └── PYTHON_GET.py
│   └── POST/                          # Working POST examples
│       ├── ESP32-OM2M-TEST.ino
│       └── ESP8266-OM2M-TEST.ino
│
├── start.sh                            # Startup script (Linux/Mac)
├── README.md                           # Documentation (this file)
├── om2mHandler.h                       # oneM2M helper header (reference)
└── test_*.py                           # Test scripts
```

## 🎨 Platform-Specific Features

### Arduino Nano 33 IoT
**Libraries Used**:
- `WiFiNINA.h` - WiFi connectivity management
- `ArduinoHttpClient.h` - HTTP client for requests
- `ArduinoJson.h` - JSON parsing and serialization

**Key Features**:
- Automatic WiFi connection with reconnection logic
- WiFi status indication via Serial monitor
- GET: Parses JSON response and extracts `m2m:cin` content
- POST: Builds proper oneM2M payload structure
- Serial debugging output (115200 baud)
- Error handling and status codes

**Generated Code Includes**:
- WiFi credentials (SSID & password)
- Server configuration (URL, port, paths)
- `connectWiFi()` function
- `sendOneM2MData()` or `getOneM2MData()` function
- Proper HTTP headers (X-M2M-Origin, X-M2M-RI, Content-Type)

### ESP32
**Libraries Used**:
- `WiFi.h` - Built-in WiFi support
- `HTTPClient.h` - HTTP/HTTPS client
- `ArduinoJson.h` - JSON handling

**Key Features**:
- High-performance dual-core processor
- HTTPS support with SSL/TLS
- Automatic WiFi reconnection on disconnect
- GET: JSON parsing with visual feedback (✅/❌)
- POST: ArduinoJson-based payload construction
- Serial output at 115200 baud
- IP address display on connection

**Unique Capabilities**:
- Can handle both HTTP and HTTPS
- More memory for larger JSON documents
- Faster processing than ESP8266

### ESP8266
**Libraries Used**:
- `ESP8266WiFi.h` - WiFi functionality
- `ESP8266HTTPClient.h` - HTTP client
- `ArduinoJson.h` - JSON operations

**Key Features**:
- Compact, cost-effective solution
- HTTP support (HTTPS possible but resource-intensive)
- WiFi connection management
- GET: JSON response parsing
- POST: Structured payload generation
- Serial output at 9600 baud
- Lower power consumption

**Important Notes**:
- Best performance with HTTP (port 8080)
- HTTPS requires `WiFiClientSecure` and more memory
- Ideal for simple, periodic data transmission

### Python
**Libraries Used**:
- `requests` - HTTP client
- `json` - JSON handling
- `time` - Timing and intervals

**Key Features**:
- Cross-platform (Windows, Linux, macOS)
- Full HTTP/HTTPS support with certificate verification
- Comprehensive error handling (Timeout, ConnectionError)
- GET: Parses and displays JSON response
- POST: Clean payload structure with proper headers
- Console output with status messages
- Configurable request timeouts (10 seconds)
- Continuous operation mode (10-second intervals)

**Use Cases**:
- Server-side applications
- Raspberry Pi edge computing
- Data aggregation and forwarding
- Testing and development
- Long-running services

## 🔌 oneM2M Compliance

### Standard Headers
All generated code includes mandatory oneM2M headers:

```
X-M2M-Origin: <your-auth-credentials>    # Authentication identifier
X-M2M-RI: <unique-request-id>            # Unique request identifier (timestamp-based)
Content-Type: application/json;ty=4      # Content Instance type
Accept: application/json                  # Response format
```

### Payload Structure
**POST Request** - Create Content Instance:
```json
{
  "m2m:cin": {
    "con": "{\"temperature\":25.5,\"humidity\":60}"
  }
}
```
- The `con` field MUST be a stringified JSON object
- Inner data is serialized to string before wrapping in `m2m:cin`
- This is the standard oneM2M Content Instance format

**GET Request** - Retrieve Latest Content Instance:
- Resource path: `/<cse-base>/<ae-name>/<container-name>/la`
- `la` suffix retrieves the latest Content Instance
- Response contains `m2m:cin` with `con` field

### Resource Paths
Generated code uses standard oneM2M resource paths:
- **CSE Base**: `/~/` (CSE-relative) or `/` (absolute)
- **AE Path**: `/<cse-base>/<ae-name>`
- **Container Path**: `/<cse-base>/<ae-name>/<container-name>`
- **Latest CI**: `/<cse-base>/<ae-name>/<container-name>/la`

### HTTP Methods
- **POST**: Create Content Instance (send data)
- **GET**: Retrieve resource (fetch data)
- Both include proper Content-Type and Accept headers

## 🎯 Code Quality Standards

Generated code follows professional standards:

### ✅ Production-Ready Features
- **No Hardcoded Values**: All configuration comes from user input
- **No Placeholders**: Complete, working code with no TODOs
- **Fully Compilable**: Ready to upload to devices without modification
- **Error Handling**: Comprehensive error checking and reporting
- **WiFi Management**: Automatic connection and reconnection logic
- **Debug Output**: Serial/console messages for troubleshooting
- **Clean Structure**: Well-organized functions and clear variable names
- **Comments**: Explanatory comments for key sections

### Microcontroller Code Structure
```cpp
// Libraries
#include <WiFiNINA.h>  // or appropriate WiFi library
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>

// Configuration (from your input)
const char* WIFI_SSID = "YourNetwork";
const char* WIFI_PASSWORD = "YourPassword";
const char* SERVER = "192.168.1.100";
const int PORT = 8080;
// ... other config

void setup() {
  Serial.begin(115200);
  connectWiFi();
}

void loop() {
  sendOneM2MData();  // or getOneM2MData()
  delay(10000);
}

void connectWiFi() {
  // WiFi connection with status feedback
}

void sendOneM2MData() {
  // Complete POST implementation with JSON
}
```

### Python Code Structure
```python
import requests
import json
import time

# Configuration (from your input)
SERVER = "192.168.1.100"
PORT = 8080
PROTOCOL = "http"
# ... other config

def send_onem2m_data():
    # Complete POST implementation
    
def get_onem2m_data():
    # Complete GET implementation

if __name__ == "__main__":
    while True:
        send_onem2m_data()  # or get_onem2m_data()
        time.sleep(10)
```

## � Configuration Examples

### Example 1: Temperature & Humidity Monitor (Arduino Nano 33 IoT)

**Scenario**: IoT sensor sending environmental data to oneM2M server

```
Platform: Arduino Nano 33 IoT
Protocol: HTTP
CSE URL: 192.168.1.100
Port: 8080
AE Name: TempSensor
Container: EnvironmentalData
X-M2M-Origin: admin:admin
WiFi SSID: HomeNetwork
WiFi Password: MySecurePassword

Operation: POST
Parameters:
  1. temperature (float): 25.5
  2. humidity (int): 60
  3. timestamp (string): "2026-01-04T10:30:00"
```

**Generated Code**: Complete Arduino sketch with WiFiNINA, sends data every 10 seconds

---

### Example 2: Smart Home Controller (ESP32)

**Scenario**: ESP32 retrieving latest sensor readings from server

```
Platform: ESP32
Protocol: HTTPS
CSE URL: onem2m.smarthome.local
Port: 443
AE Name: HomeController
Container: SensorReadings
X-M2M-Origin: home:controller123
WiFi SSID: SmartHome_5G
WiFi Password: SecureHome2026

Operation: GET
Parameters: (retrieved from server)
  - sensor_id (string)
  - value (float)
  - status (boolean)
```

**Generated Code**: ESP32 code with HTTPS support, parses JSON response

---

### Example 3: Industrial Data Logger (Python)

**Scenario**: Raspberry Pi sending machine data to cloud oneM2M platform

```
Platform: Python
Protocol: HTTPS
CSE URL: onem2m.industry.cloud
Port: 443
AE Name: FactoryDataLogger
Container: MachineMetrics
X-M2M-Origin: factory_001:secure_token

Operation: POST
Parameters:
  1. machine_id (string): "MACHINE_001"
  2. production_count (int): 1500
  3. power_consumption (float): 3.75
  4. operational_status (boolean): true
  5. error_code (string): "NONE"
```

**Generated Code**: Python script with continuous operation, error handling, HTTPS verification

---

### Example 4: Weather Station (ESP8266)

**Scenario**: Low-cost weather monitoring station

```
Platform: ESP8266
Protocol: HTTP
CSE URL: 192.168.0.50
Port: 8080
AE Name: WeatherStation
Container: WeatherData
X-M2M-Origin: weather:station01
WiFi SSID: WeatherNet
WiFi Password: Weather2026

Operation: POST
Parameters:
  1. temperature (float): 18.5
  2. pressure (float): 1013.25
  3. wind_speed (float): 12.3
  4. rainfall (int): 0
```

**Generated Code**: ESP8266 code optimized for low power, HTTP-only for efficiency

## 🌐 API Endpoints

The Flask backend provides the following REST API endpoints:

### Page Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Controller platform selection page |
| GET | `/configure/<controller>` | Configuration page for selected platform |
| GET | `/generate-view` | Code preview and download page |

### API Routes
| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/generate` | Generate code based on configuration | JSON config object |
| POST | `/download` | Download generated code as file | `{code, filename}` |
| POST | `/test-get` | Test GET request to oneM2M server | JSON config object |
| POST | `/test-post` | Test POST request to oneM2M server | JSON config object with parameters |

### Configuration Object Structure
```json
{
  "protocol": "http",
  "cse_url": "192.168.1.100",
  "port": 8080,
  "ae_name": "MyApp",
  "container_name": "MyContainer",
  "origin": "admin:admin",
  "wifi_ssid": "MyNetwork",
  "wifi_password": "MyPassword",
  "operation": "POST",
  "num_params": 2,
  "param_1_name": "temperature",
  "param_1_type": "float",
  "param_1_default": "25.5",
  "param_2_name": "humidity",
  "param_2_type": "int",
  "param_2_default": "60"
}
```

### Response Formats

**Success Response** (`/generate`):
```json
{
  "code": "// Generated Arduino code...",
  "filename": "onem2m_client.ino"
}
```

**Test Response** (`/test-get`, `/test-post`):
```json
{
  "success": true,
  "status_code": 200,
  "response": {
    "m2m:cin": {
      "con": "{\"temperature\":25.5}"
    }
  }
}
```

**Error Response**:
```json
{
  "error": "Error message description"
}
```

## 🚨 Troubleshooting

### Installation Issues

**Problem**: Server won't start
- **Check Python version**: `python --version` (must be 3.7+)
- **Check port availability**: Port 5000 might be in use by another application
- **Try different port**: Modify `app.py` line `app.run(port=5000)` to use different port
- **Reinstall dependencies**: 
  ```bash
  pip uninstall flask flask-cors
  pip install -r backend/requirements.txt
  ```

**Problem**: Module import errors
- **Activate virtual environment**: Make sure `venv` is activated (see Installation section)
- **Wrong directory**: Navigate to `backend/` folder before running `python app.py`
- **Check installation**: `pip list | grep Flask`

---

### Generated Code Issues

**Arduino/ESP32/ESP8266 - Compilation Errors**

**Problem**: Library not found
- **Install required libraries** via Arduino IDE Library Manager:
  - Arduino Nano 33 IoT: `WiFiNINA`, `ArduinoHttpClient`, `ArduinoJson`
  - ESP32: `ArduinoJson` (WiFi and HTTPClient are built-in)
  - ESP8266: `ArduinoJson` (WiFi libraries are built-in)

**Problem**: Board not recognized
- **Install board support**:
  - ESP32: Add `https://dl.espressif.com/dl/package_esp32_index.json` to Additional Board URLs
  - ESP8266: Add `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
  - Arduino Nano 33 IoT: Install "Arduino SAMD Boards" from Boards Manager

**Problem**: Upload fails
- **Select correct board**: Tools → Board → [Your exact board model]
- **Select correct port**: Tools → Port → [COM port or /dev/ttyUSBx]
- **Check USB cable**: Some cables are power-only (use data cable)

**Python - Runtime Errors**

**Problem**: `ModuleNotFoundError: No module named 'requests'`
- **Install requests**: `pip install requests`

**Problem**: Connection timeout
- **Check server status**: Verify oneM2M server is running
- **Test connectivity**: `ping <server-ip>` to verify network connection
- **Firewall**: Ensure firewall allows connections on the specified port
- **Increase timeout**: Modify `timeout=10` parameter in requests call

---

### WiFi Connection Issues (Microcontrollers)

**Problem**: WiFi won't connect
- **Verify credentials**: Check SSID and password are correct (case-sensitive)
- **Check WiFi band**: ESP8266 only supports 2.4GHz (not 5GHz)
- **Signal strength**: Move device closer to router
- **Serial monitor**: Check connection status messages at correct baud rate
  - Arduino Nano 33: 115200
  - ESP32: 115200
  - ESP8266: 9600

**Problem**: WiFi connects but HTTP fails
- **Server reachability**: Ensure device and server are on same network (or server is publicly accessible)
- **Port forwarding**: Check if port forwarding is needed
- **Protocol mismatch**: Verify HTTP vs HTTPS settings match server

---

### oneM2M Server Communication

**Problem**: HTTP 401 Unauthorized
- **Check X-M2M-Origin**: Verify authentication credentials are correct
- **Format**: Should be `username:password` or as specified by your server

**Problem**: HTTP 404 Not Found
- **Verify resource paths**: Check AE Name and Container Name exist on server
- **Case sensitivity**: Resource names are case-sensitive
- **CSE Base**: Verify the CSE base URL is correct

**Problem**: HTTP 400 Bad Request
- **Check JSON format**: Payload must have correct `m2m:cin` structure
- **Content-Type header**: Must include `application/json;ty=4`
- **con field**: Must be a string (not an object)

**Problem**: No response / timeout
- **Server running**: Verify oneM2M CSE is running
- **Network path**: Check firewall rules and network routing
- **Protocol**: Confirm HTTP vs HTTPS matches server configuration

---

### Testing Feature Issues

**Problem**: "Test GET/POST Request" button does nothing
- **Open browser console**: Press F12, check Console tab for errors
- **Check server logs**: Flask terminal should show incoming requests
- **CORS issues**: Verify flask-cors is installed

**Problem**: Test succeeds but code generation fails
- **Different validation**: Code generation has stricter validation
- **Check all fields**: Ensure all required fields are filled
- **Browser refresh**: Try refreshing the page and reconfiguring

---

### Copy/Download Issues

**Problem**: Copy button doesn't work
- **Browser compatibility**: Try a different browser (Chrome, Firefox, Edge)
- **HTTPS requirement**: Some browsers restrict clipboard access on HTTP
- **Manual copy**: Use Ctrl+A to select all, then Ctrl+C

**Problem**: Downloaded file is empty
- **Check sessionStorage**: Code should be in browser sessionStorage
- **Regenerate code**: Go back and generate code again
- **Check browser permissions**: Allow file downloads

## � Security Considerations

### Development vs Production

This tool generates code suitable for development and prototyping. For production deployment, consider:

**HTTPS/SSL**
- Use HTTPS (port 443) for production servers
- For microcontrollers, implement proper certificate verification:
  ```cpp
  // Instead of client.setInsecure()
  client.setCACert(root_ca);  // Use actual CA certificate
  ```

**Credentials Management**
- **Don't hardcode credentials** in production code
- Use secure storage mechanisms:
  - Arduino: EEPROM or encrypted storage
  - ESP32: NVS (Non-Volatile Storage)
  - Python: Environment variables or secrets management

**Authentication**
- Use strong X-M2M-Origin credentials
- Consider token-based authentication for production
- Rotate credentials regularly

**Network Security**
- Use WPA2/WPA3 WiFi encryption
- Implement firewall rules
- Use VPN for remote access

### Generated Code Security

Current generated code includes:
- ✅ HTTPS support option
- ✅ Basic error handling
- ⚠️ Self-signed certificates accepted (setInsecure)
- ⚠️ WiFi credentials in plaintext

**Recommended Improvements for Production**:
1. Implement certificate pinning
2. Encrypt stored credentials
3. Add rate limiting
4. Implement retry backoff
5. Add input validation
6. Use secure random for Request IDs

## � Testing

### Test Code Examples

The `testing_code/` directory contains working examples that serve as references:

**GET Operations** (`testing_code/GET/`):
- `NANO33_GET.ino` - Arduino Nano 33 IoT GET example
- `ESP32_GET.ino` - ESP32 GET example with JSON parsing
- `ESP8266_GET.ino` - ESP8266 GET example
- `PYTHON_GET.py` - Python GET example

**POST Operations** (`testing_code/POST/`):
- `ESP32-OM2M-TEST.ino` - ESP32 POST example with full workflow
- `ESP8266-OM2M-TEST.ino` - ESP8266 POST example

### Testing Your Generated Code

**Microcontrollers** (Arduino IDE):
1. Open generated `.ino` file in Arduino IDE
2. Select correct board: Tools → Board
3. Select correct port: Tools → Port
4. Upload code to device
5. Open Serial Monitor (Ctrl+Shift+M)
6. Set correct baud rate (9600 or 115200)
7. Observe connection status and data transmission

**Python**:
1. Save generated `.py` file
2. Run: `python onem2m_client.py`
3. Observe console output for connection status
4. Press Ctrl+C to stop

### Verifying oneM2M Server

Use the built-in testing feature:
1. Configure all settings in the web interface
2. Click "Test GET Request" or "Test POST Request"
3. View server response in real-time
4. Verify data format and response codes
5. Proceed to generate code if test succeeds

### Manual API Testing

Test your oneM2M server with `curl`:

```bash
# GET request
curl -X GET \
  -H "X-M2M-Origin: admin:admin" \
  -H "Accept: application/json" \
  http://192.168.1.100:8080/~/MyApp/MyContainer/la

# POST request
curl -X POST \
  -H "X-M2M-Origin: admin:admin" \
  -H "Content-Type: application/json;ty=4" \
  -H "X-M2M-RI: test-123" \
  -d '{"m2m:cin":{"con":"{\"temperature\":25.5}"}}' \
  http://192.168.1.100:8080/~/MyApp/MyContainer
```

## 🎯 Future Roadmap

### Planned Features
- [ ] **MQTT Support** - Alternative protocol for IoT communication
- [ ] **CoAP Support** - Constrained Application Protocol for resource-limited devices
- [ ] **More Platforms** - STM32, Raspberry Pi Pico, PIC microcontrollers
- [ ] **Template Management** - Save and reuse configurations
- [ ] **Project Export** - Export complete projects with multiple devices
- [ ] **Code Snippets Library** - Reusable code patterns and examples
- [ ] **Batch Code Generation** - Generate code for multiple devices at once
- [ ] **Advanced oneM2M Operations** - UPDATE, DELETE operations
- [ ] **Subscription Support** - Notification handling
- [ ] **WebSocket Support** - Real-time bidirectional communication

### Potential Improvements
- [ ] Dark mode UI theme
- [ ] Code syntax highlighting in preview
- [ ] Configuration import/export (JSON)
- [ ] Docker containerization
- [ ] API authentication for web interface
- [ ] Multi-language support (i18n)
- [ ] Code optimization options (memory/speed)
- [ ] Custom code templates
- [ ] Integration testing suite
- [ ] Documentation generator from code

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues
- Check existing issues first
- Provide clear description of the problem
- Include steps to reproduce
- Share error messages and logs
- Specify your environment (OS, Python version, browser)

### Submitting Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Development Guidelines
- Follow existing code style
- Add comments for complex logic
- Update README if adding features
- Test generated code on actual hardware when possible
- Maintain oneM2M compliance

### Areas Needing Help
- Testing on different hardware platforms
- oneM2M server compatibility testing
- UI/UX improvements
- Documentation improvements
- Bug fixes and optimizations

## 📧 Support & Community

### Getting Help
1. **Check Documentation**: This README and troubleshooting section
2. **Review Examples**: Check `testing_code/` directory for working examples
3. **Test Feature**: Use built-in testing to verify server connectivity
4. **Generated Comments**: Read comments in generated code
5. **Open Issue**: Create a GitHub issue with details

### Useful Resources
- [oneM2M Official Website](https://www.onem2m.org/)
- [oneM2M Technical Specifications](https://www.onem2m.org/technical/published-documents)
- [Arduino Reference](https://www.arduino.cc/reference/)
- [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- [Python Requests Documentation](https://requests.readthedocs.io/)

## 📝 License

This project is provided as-is for educational and development purposes.

**MIT License** - Feel free to use, modify, and distribute with attribution.

### Third-Party Licenses
Generated code uses libraries with their own licenses:
- **ArduinoJson** - MIT License
- **WiFiNINA** - LGPL 2.1
- **ESP32/ESP8266 Libraries** - LGPL 2.1
- **Python Requests** - Apache 2.0

---

## 📊 Project Status

**Current Version**: 1.0.0  
**Status**: Active Development  
**Last Updated**: January 2026

### Recent Updates
- ✅ Added WiFi credential configuration
- ✅ Implemented optional testing workflow
- ✅ Updated all platform templates with working code patterns
- ✅ Improved UI with better button layout
- ✅ Fixed copy to clipboard functionality
- ✅ Enhanced error handling across all platforms

---

**Built with Flask** | **oneM2M Standards Compliant** | **Production Ready**

**Supported Platforms**: Arduino Nano 33 IoT • ESP32 • ESP8266 • Python

---

*Made for IoT developers, by IoT developers* 🚀
