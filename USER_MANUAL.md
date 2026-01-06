# oneM2M Code Generator - User Manual

## 📖 Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Step-by-Step Guide](#step-by-step-guide)
4. [Understanding Parameters](#understanding-parameters)
5. [Testing Your Configuration](#testing-your-configuration)
6. [Using Generated Code](#using-generated-code)
7. [Troubleshooting](#troubleshooting)

---

## Introduction

The **oneM2M Code Generator** is a web-based tool that automatically creates ready-to-use code for IoT devices to communicate with oneM2M servers. 

### What does it do?
- Generates code for Arduino, ESP32, ESP8266, and Python
- Handles both sending (POST) and receiving (GET) data
- Creates complete, working code - no manual editing needed
- Tests your connection before generating code

### Who is it for?
- IoT developers working with oneM2M platforms
- Students learning IoT and oneM2M
- Anyone who wants to quickly connect devices to oneM2M servers

---

## Getting Started

### Starting the Application

**Option 1: Using the start script (Recommended)**
```bash
./start.sh
```

**Option 2: Manual start**
```bash
# 1. Activate virtual environment
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

# 2. Navigate to backend
cd backend

# 3. Start the server
python app.py
```

### Accessing the Application
Open your web browser and go to: **http://localhost:5000**

---

## Step-by-Step Guide

### Step 1: Select Your Platform

Choose the device you're coding for:

| Platform | Best For |
|----------|----------|
| **Arduino Nano 33 IoT** | Low-power sensors, small projects |
| **ESP32** | High-performance projects, needs HTTPS |
| **ESP8266** | Budget projects, simple sensors |
| **Python** | Raspberry Pi, servers, PC applications |

**👉 Click on your platform card**

---

### Step 2: Configure Server Settings

Fill in your oneM2M server details:

#### Required Fields:

1. **Server Host**
   - Example: `onem2m.iiit.ac.in`
   - Don't include `http://` or `https://`

2. **Server Port**
   - `443` = HTTPS (secure, encrypted)
   - `8080` = HTTP (faster, local networks)

3. **Application Entity (AE)**
   - Your application name on the server
   - Example: `AE-SL`

4. **Container Name**
   - Where your data is stored
   - Example: `SL-VN03-00`

5. **Authentication (X-M2M-Origin)**
   - Your credentials
   - Format: `username:password`
   - Example: `admin:admin` or `a8d#J7:5Zi@la!5`

#### Optional Fields (for Arduino/ESP devices):

6. **WiFi SSID**
   - Your WiFi network name

7. **WiFi Password**
   - Your WiFi password

**👉 Click "Continue" when done**

---

### Step 3: Choose Operation Type

Select what your device will do:

#### GET Request (Retrieve Data)
- Fetches the latest data from the server
- Use when: Reading sensor data uploaded by other devices
- Example: Display temperature from cloud

#### POST Request (Send Data)
- Sends data to the server
- Use when: Uploading sensor readings
- Example: Send temperature every 10 seconds

**👉 Select operation and click "Proceed"**

---

### Step 4: Define Data Parameters

#### For POST Request:

Add the data fields you want to send:

**Example 1: Temperature Sensor**
- Parameter 1: `temperature`, Type: `Decimal`, Value: `25.5`

**Example 2: Multi-Sensor**
- Parameter 1: `temperature`, Type: `Decimal`, Value: `25.5`
- Parameter 2: `humidity`, Type: `Integer`, Value: `60`
- Parameter 3: `status`, Type: `Text`, Value: `OK`

##### Data Types:
- **Integer**: Whole numbers (25, 100, -5)
- **Decimal**: Numbers with decimals (25.5, 98.6)
- **Text**: Words or strings ("hello", "OK")
- **True/False**: Boolean values (true, false)

**👉 Click "Add Parameter" for more fields**

#### Labels (Optional):
Add metadata tags for your data:
- Example: `AE-SL`, `V2.0.1`, `Room-101`

**👉 Click "Add Label" for more tags**

---

### Step 5: Test Your Connection (Optional but Recommended)

Before generating code, test if your configuration works:

**For GET Request:**
1. Click **"Test GET Request"**
2. Wait for response
3. ✅ Green badge = Success
4. ❌ Red badge = Check your settings

**For POST Request:**
1. Click **"Test POST Request"**
2. Wait for response
3. ✅ Status 201 = Data sent successfully
4. ❌ Status 401 = Wrong credentials
5. ❌ Status 404 = Check AE/Container names

**Common Status Codes:**
- `200-201` ✅ Success
- `401` ❌ Authentication failed
- `404` ❌ Resource not found
- `500` ❌ Server error

---

### Step 6: Generate Code

**👉 Click "Generate Code" button**

The code appears with:
- Complete, working code
- All your settings included
- WiFi configuration (if applicable)
- Comments explaining each part

---

### Step 7: Download or Copy Code

Choose how to save your code:

**Option 1: Copy to Clipboard**
1. Click **"Copy"** button
2. Paste in your Arduino IDE / Python editor

**Option 2: Download File**
1. Click **"Download File"** button
2. Open file in your editor

**File Names:**
- Arduino: `onem2m_client.ino`
- Python: `onem2m_client.py`

---

## Understanding Parameters

### Data Format
Generated code sends data as an array:
```
[epoch_timestamp, value1, value2, value3, ...]
```

**Example:**
- Parameters: temperature=25.5, humidity=60
- Sent as: `[1767678448, 25.5, 60]`
- First value is always current timestamp

### Why This Format?
- Efficient for IoT devices
- Easy to parse on server side
- Timestamp shows when data was collected

---

## Testing Your Configuration

### Before Generating Code

**✅ Always test your configuration first!**

Why?
- Verifies server is reachable
- Checks credentials are correct
- Confirms AE and Container exist
- Saves time debugging later

### Test Results

**Green (Success):**
- Configuration is correct
- Ready to generate code
- Device will work with same settings

**Red (Failed):**
- Review error message
- Common issues:
  - Wrong server URL
  - Incorrect credentials
  - AE/Container doesn't exist
  - Network/firewall blocking

---

## Using Generated Code

### For Arduino/ESP Devices

1. **Open Arduino IDE**
2. **Paste or open the generated code**
3. **Install required libraries:**
   - Arduino Nano 33 IoT: `WiFiNINA`, `ArduinoHttpClient`, `ArduinoJson`
   - ESP32: `ArduinoJson` (WiFi built-in)
   - ESP8266: `ArduinoJson` (WiFi built-in)
4. **Select correct board:** Tools → Board
5. **Select correct port:** Tools → Port
6. **Upload code** (Ctrl+U)
7. **Open Serial Monitor** (Ctrl+Shift+M)
8. **Set baud rate:**
   - Arduino/ESP32: 115200
   - ESP8266: 9600

### For Python

1. **Save the generated code:** `onem2m_client.py`
2. **Install requirements:**
   ```bash
   pip install requests
   ```
3. **Run the code:**
   ```bash
   python onem2m_client.py
   ```

### Modifying Generated Code

**For Python:**
```python
# You can easily change values:
temperature = 25.5  # Change this
humidity = 60       # Change this

# Data sent: [timestamp, 25.5, 60]
```

**For Arduino:**
```cpp
// In the loop() function:
void loop() {
  postOneM2MData();
  delay(10000);  // Change delay time (milliseconds)
}
```

---

## Troubleshooting

### Application Won't Start

**Problem:** Port 5000 already in use
```
Solution: Change port in backend/app.py
app.run(port=5001)  # Use different port
```

**Problem:** Module not found
```bash
Solution: Install dependencies
pip install -r backend/requirements.txt
```

---

### Code Generation Issues

**Problem:** "Failed to generate code"
- Check all required fields are filled
- Test connection first
- Refresh page and try again

**Problem:** WiFi credentials not in code
- Fill in WiFi SSID and Password fields
- Regenerate code

---

### Arduino/ESP Upload Issues

**Problem:** Compilation error - Library not found
```
Solution:
1. Open Arduino IDE
2. Tools → Manage Libraries
3. Search and install missing library
4. Try upload again
```

**Problem:** Upload fails - Port not found
```
Solution:
1. Check USB cable (must be data cable)
2. Install USB drivers for your board
3. Select correct COM port in Tools → Port
```

**Problem:** WiFi won't connect
```
Solution:
1. Check SSID and password are correct
2. ESP8266 only works on 2.4GHz WiFi
3. Check WiFi is in range
4. Try different WiFi network
```

---

### Server Connection Issues

**Problem:** Test shows 401 Unauthorized
```
Solution: Check X-M2M-Origin credentials
```

**Problem:** Test shows 404 Not Found
```
Solution:
- Verify AE Name exists on server
- Verify Container Name exists
- Check spelling (case-sensitive)
```

**Problem:** Test shows timeout
```
Solution:
- Check server URL is correct
- Verify port number
- Test server in web browser
- Check firewall settings
```

**Problem:** GET works but POST fails
```
Solution:
- Check you have write permissions
- Verify Container accepts content instances
```

---

### Python Code Issues

**Problem:** Import error
```bash
Solution: Install requests
pip install requests
```

**Problem:** Connection refused
```
Solution:
- Verify server URL and port
- Check internet connection
- Test with curl or browser first
```

---

## Tips and Best Practices

### 1. Always Test First
✅ Use the "Test" button before generating code

✅ Verify green success status

✅ Read any error messages carefully


### 2. Start Simple
✅ Begin with 1-2 parameters

✅ Test with known working values

✅ Add complexity gradually

### 3. Naming Conventions
✅ Use clear parameter names: `temperature`, not `t`

✅ Avoid spaces and special characters

✅ Use lowercase or camelCase

### 4. Security
⚠️ Don't share credentials publicly

⚠️ Use HTTPS (port 443) for production

⚠️ Change default passwords

### 5. Development Workflow
1. Configure settings
2. Test connection
3. Generate code
4. Upload/run code
5. Monitor Serial output
6. Verify data on server

---

## Quick Reference

### Keyboard Shortcuts
- Generate new code: Click logo or "Generate New Code"
- Copy code: Copy button in code view
- Download: Download button in code view

### Default Values
- HTTP Port: 8080
- HTTPS Port: 443
- POST Interval: 10 seconds
- Serial Baud Rate (Arduino/ESP32): 115200
- Serial Baud Rate (ESP8266): 9600

### Common Ports
- 8080 = HTTP (local/development)
- 443 = HTTPS (production/secure)
- 80 = HTTP (alternative)

---

## Need Help?

### Getting Support
1. Check this manual first
2. Review the troubleshooting section
3. Test your configuration using the built-in test feature
4. Check server logs if available
5. Open an issue on GitHub (if applicable)

### Useful Resources
- [oneM2M Official Documentation](https://www.onem2m.org/)
- [Arduino Documentation](https://www.arduino.cc/reference/)
- [ESP32 Documentation](https://docs.espressif.com/)

---

## Appendix: Example Configurations

### Example 1: Temperature Logger (Arduino Nano 33 IoT)

**Configuration:**
- Platform: Arduino Nano 33 IoT
- Server: `onem2m.iiit.ac.in`
- Port: `443` (HTTPS)
- AE: `AE-TempSensor`
- Container: `TempData`
- Origin: `sensor:password123`
- WiFi SSID: `HomeWiFi`
- WiFi Password: `mypassword`
- Operation: POST
- Parameters:
  - `temperature` (Decimal): `25.5`

**Result:** Device sends temperature every 10 seconds

---

### Example 2: Weather Station (ESP32)

**Configuration:**
- Platform: ESP32
- Server: `192.168.1.100`
- Port: `8080` (HTTP)
- AE: `AE-Weather`
- Container: `WeatherData`
- Origin: `admin:admin`
- Operation: POST
- Parameters:
  - `temperature` (Decimal): `22.5`
  - `humidity` (Integer): `65`
  - `pressure` (Decimal): `1013.25`

**Result:** Device sends weather data to local server

---

### Example 3: Data Retriever (Python)

**Configuration:**
- Platform: Python
- Server: `onem2m.iiit.ac.in`
- Port: `443` (HTTPS)
- AE: `AE-Monitor`
- Container: `SensorData`
- Origin: `monitor:pass`
- Operation: GET

**Result:** Script retrieves latest sensor reading

---

**Version:** 1.0  
**Last Updated:** January 6, 2026  
**© 2026 oneM2M Code Generator**
