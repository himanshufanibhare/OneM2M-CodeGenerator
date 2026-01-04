# oneM2M Code Generator

A professional web-based dashboard that automatically generates oneM2M-compatible client code for multiple platforms.

## 🚀 Features

- **Multi-Platform Support**: Generate code for Arduino Nano 33 IoT, ESP32, ESP8266, and Python
- **User-Friendly Interface**: Clean, modern multi-page workflow
- **Production-Ready Code**: Generates complete, compilable, tested code
- **Full Configuration**: Complete oneM2M server setup and data parameter configuration
- **POST & GET Operations**: Support for both sending and retrieving data
- **Download & Copy**: Easy code export with syntax highlighting

## 📋 Requirements

- Python 3.7+
- Flask 3.0.0
- flask-cors 4.0.0

## 🛠️ Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
.\venv\Scripts\Activate.ps1  # On Windows
```

3. Run the start script:

```bash
chmod +x start.sh
./start.sh
```

**Manual Installation:**

```bash
pip install -r backend/requirements.txt
python app.py
```

## 💻 Usage

1. **Start the Server**:
   ```bash
   ./start.sh
   ```

2. **Open Browser**: Navigate to `http://localhost:5000`

3. **Select Controller**: Choose your target platform
   - Arduino Nano 33 IoT
   - ESP32
   - ESP8266
   - Python (PC/Raspberry Pi/Server)

4. **Configure Settings**:
   - oneM2M CSE Base URL
   - Port number
   - AE Name (Application Entity)
   - Container Name
   - Authentication (X-M2M-Origin header)

5. **Define Data Parameters**:
   - Number of parameters
   - Parameter names
   - Data types (int, float, string, boolean)
   - Default values

6. **Select Operation**:
   - POST: Send data to oneM2M server
   - GET: Retrieve data from oneM2M server

7. **Generate Code**: Click "Generate Code" to get your custom client

8. **Export Code**:
   - Copy to clipboard
   - Download as file (.ino or .py)

## 📁 Project Structure

```
CODE_GENERATOR/
├── app.py                    # Main Flask application
├── backend/
│   ├── requirements.txt      # Python dependencies
│   ├── static/
│   │   └── style.css        # Modern CSS styling
│   └── templates/
│       ├── controller_select.html  # Controller selection page
│       ├── configure.html          # Configuration page
│       └── generate.html           # Code generation & preview
├── venv/                     # Virtual environment (after setup)
├── start.sh                  # Linux/Mac startup script
└── README.md                 # This file
```

## 🎨 Features in Detail

### Controller Support

**Arduino Nano 33 IoT**
- WiFiNINA library integration
- WiFi connection management
- HTTP client implementation
- Serial debugging output

**ESP32**
- Built-in WiFi support
- HTTPClient library
- Advanced error handling
- High-performance networking

**ESP8266**
- Compact WiFi implementation
- ESP8266HTTPClient support
- Resource-efficient code
- Reliable connectivity

**Python**
- Requests library usage
- Cross-platform compatibility
- Continuous operation mode
- Exception handling

### oneM2M Compliance

- Proper X-M2M-Origin headers
- Correct Content-Type headers
- Standard JSON payload structure
- Resource path formatting (~/AE/Container)
- HTTP response code handling

### Code Quality

- ✅ No hardcoded values
- ✅ No placeholder comments
- ✅ Production-ready
- ✅ Fully compilable
- ✅ Error handling included
- ✅ WiFi reconnection logic
- ✅ Serial/console output for debugging

## 🔧 Configuration Examples

### Example 1: Temperature Sensor (Arduino)

```
Controller: Arduino Nano 33 IoT
CSE URL: 192.168.1.100
Port: 8080
AE Name: TempSensor
Container: TemperatureData
Origin: admin:admin
Operation: POST
Parameters:
  - temperature (float): 25.5
  - humidity (int): 60
  - timestamp (string): "2025-12-17"
```

### Example 2: Data Logger (Python)

```
Controller: Python
CSE URL: onem2m.example.com
Port: 8080
AE Name: DataLogger
Container: SensorReadings
Origin: user:password
Operation: POST
Parameters:
  - sensor_id (string): "SENSOR_001"
  - value (float): 123.45
  - status (boolean): true
```

## 🌐 API Endpoints

- `GET /` - Controller selection page
- `GET /configure/<controller>` - Configuration page
- `POST /generate` - Generate code (JSON API)
- `GET /generate-view` - Display generated code
- `POST /download` - Download code file

## 🚨 Troubleshooting

**Server won't start:**
- Check if port 5000 is already in use
- Verify Python is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`

**Generated code won't compile:**
- Arduino: Install required libraries (WiFiNINA, HTTPClient)
- ESP32/ESP8266: Install board support in Arduino IDE
- Python: Install requests library: `pip install requests`

**Connection issues:**
- Verify oneM2M server is running and accessible
- Check firewall settings
- Confirm server URL and port are correct
- Update WiFi credentials in generated code

## 📝 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📧 Support

For issues or questions, please check the troubleshooting section or review the generated code comments.

## 🎯 Roadmap

- [ ] MQTT protocol support
- [ ] CoAP protocol support
- [ ] More controller platforms (STM32, PIC)
- [ ] Template management
- [ ] Project save/load functionality
- [ ] Code snippet library

---

**Built with Flask** | **oneM2M Standards Compliant** | **Production Ready**
