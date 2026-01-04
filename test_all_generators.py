#!/usr/bin/env python3
"""
Comprehensive test for all Arduino-based platform generators.
Tests dynamic URL construction, protocol handling, and oneM2M compliance.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.controllers.arduino import generate_arduino_code
from backend.controllers.esp32 import generate_esp32_code
from backend.controllers.esp8266 import generate_esp8266_code

# Test configuration
test_config = {
    'protocol': 'https',
    'cse_url': 'onem2m.iiit.ac.in',
    'port': '443',
    'ae_name': 'AE-SL',
    'container_name': 'SL-VN03-00',
    'sub_container': 'Data',
    'origin': 'admin:admin',
    'operation': 'POST',
    'parameters': [
        {'name': 'temperature', 'type': 'float', 'default': '25.5'},
        {'name': 'humidity', 'type': 'int', 'default': '60'},
    ]
}

def verify_code(code, platform):
    """Verify generated code meets oneM2M requirements."""
    checks = {
        'HTTPS client': 'WiFiSSLClient' in code or 'WiFiClientSecure' in code,
        'Dynamic path': 'String path = "/~/in-cse/in-name/"' in code,
        'AE variable': 'path += aeName' in code,
        'Container variable': 'path += containerName' in code,
        'Sub-container variable': 'path += subContainer' in code,
        'ArduinoJson': '#include <ArduinoJson.h>' in code,
        'X-M2M-Origin': 'X-M2M-Origin' in code,
        'X-M2M-RI': 'X-M2M-RI' in code,
        'Content-Type': 'application/json;ty=4' in code,
        'Connection close': 'Connection' in code and 'close' in code,
        'con as string': 'cinDoc["m2m:cin"]["con"] = innerJson' in code,
        'No hardcoded path': '/AE-SL/SL-VN03-00' not in code,
    }
    
    passed = all(checks.values())
    
    print(f"\n{'=' * 80}")
    print(f"{platform.upper()} GENERATOR")
    print('=' * 80)
    print(f"Code length: {len(code)} bytes")
    print(f"\nVerification:")
    
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
    
    if passed:
        print(f"\n✓✓✓ {platform.upper()} - ALL CHECKS PASSED!")
    else:
        print(f"\n✗✗✗ {platform.upper()} - SOME CHECKS FAILED!")
    
    return passed

print("=" * 80)
print("TESTING ALL ARDUINO-BASED GENERATORS")
print("=" * 80)
print(f"Target: {test_config['protocol']}://{test_config['cse_url']}:{test_config['port']}")
print(f"Path: /~/in-cse/in-name/{test_config['ae_name']}/{test_config['container_name']}/{test_config['sub_container']}")
print("=" * 80)

results = {}

# Test Arduino Nano 33 IoT
try:
    arduino_code = generate_arduino_code(test_config)
    results['Arduino Nano 33 IoT'] = verify_code(arduino_code, 'Arduino Nano 33 IoT')
except Exception as e:
    print(f"\n✗ Arduino Nano 33 IoT generator FAILED: {e}")
    results['Arduino Nano 33 IoT'] = False

# Test ESP32
try:
    esp32_code = generate_esp32_code(test_config)
    results['ESP32'] = verify_code(esp32_code, 'ESP32')
except Exception as e:
    print(f"\n✗ ESP32 generator FAILED: {e}")
    results['ESP32'] = False

# Test ESP8266
try:
    esp8266_code = generate_esp8266_code(test_config)
    results['ESP8266'] = verify_code(esp8266_code, 'ESP8266')
except Exception as e:
    print(f"\n✗ ESP8266 generator FAILED: {e}")
    results['ESP8266'] = False

# Summary
print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)

all_passed = all(results.values())

for platform, passed in results.items():
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status:8} {platform}")

print("=" * 80)

if all_passed:
    print("\n🎉 SUCCESS! All generators produce oneM2M-compliant code with dynamic URL construction.")
    sys.exit(0)
else:
    print("\n❌ FAILURE! Some generators failed verification.")
    sys.exit(1)
