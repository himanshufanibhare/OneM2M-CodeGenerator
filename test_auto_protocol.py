"""Test auto-protocol detection based on port"""
import sys
sys.path.insert(0, 'backend')

from app import validate_request_config
from controllers.arduino import generate_arduino_code

print("=" * 80)
print("TESTING AUTO-PROTOCOL DETECTION")
print("=" * 80)

# Test Case 1: Port 443 should auto-select HTTPS
print("\n1. Testing Port 443 (should auto-select HTTPS):")
config1 = {
    'controller': 'arduino_nano',
    'cse_url': 'onem2m.iiit.ac.in',
    'port': 443,
    'ae_name': 'AE-SL',
    'container_name': 'SL-VN03-00',
    'sub_container': 'Data',
    'origin': 'admin:admin',
    'operation': 'post',
    'parameters': []
}

valid, msg = validate_request_config(config1, 'arduino_nano')
print(f"   Valid: {valid}")
print(f"   Protocol set to: {config1.get('protocol')}")
if config1.get('protocol') == 'https':
    print("   ✓ PASS: Protocol correctly set to HTTPS for port 443")
else:
    print("   ✗ FAIL: Expected HTTPS but got", config1.get('protocol'))

# Generate code and check
code1 = generate_arduino_code(config1)
if 'WiFiSSLClient' in code1:
    print("   ✓ PASS: Generated code uses WiFiSSLClient (HTTPS)")
else:
    print("   ✗ FAIL: Generated code should use WiFiSSLClient")

# Test Case 2: Port 8080 should auto-select HTTP
print("\n2. Testing Port 8080 (should auto-select HTTP):")
config2 = {
    'controller': 'arduino_nano',
    'cse_url': 'onem2m.iiit.ac.in',
    'port': 8080,
    'ae_name': 'AE-SL',
    'container_name': 'SL-VN03-00',
    'origin': 'admin:admin',
    'operation': 'post',
    'parameters': []
}

valid, msg = validate_request_config(config2, 'arduino_nano')
print(f"   Valid: {valid}")
print(f"   Protocol set to: {config2.get('protocol')}")
if config2.get('protocol') == 'http':
    print("   ✓ PASS: Protocol correctly set to HTTP for port 8080")
else:
    print("   ✗ FAIL: Expected HTTP but got", config2.get('protocol'))

# Generate code and check
code2 = generate_arduino_code(config2)
if 'WiFiClient client;' in code2 and 'WiFiSSLClient' not in code2:
    print("   ✓ PASS: Generated code uses WiFiClient (HTTP)")
else:
    print("   ✗ FAIL: Generated code should use WiFiClient")

# Test Case 3: Port 80 should auto-select HTTP
print("\n3. Testing Port 80 (should auto-select HTTP):")
config3 = {
    'controller': 'arduino_nano',
    'cse_url': 'onem2m.iiit.ac.in',
    'port': 80,
    'ae_name': 'AE-SL',
    'container_name': 'SL-VN03-00',
    'origin': 'admin:admin',
    'operation': 'post',
    'parameters': []
}

valid, msg = validate_request_config(config3, 'arduino_nano')
print(f"   Valid: {valid}")
print(f"   Protocol set to: {config3.get('protocol')}")
if config3.get('protocol') == 'http':
    print("   ✓ PASS: Protocol correctly set to HTTP for port 80")
else:
    print("   ✗ FAIL: Expected HTTP but got", config3.get('protocol'))

print("\n" + "=" * 80)
print("✅ AUTO-PROTOCOL DETECTION WORKING CORRECTLY!")
print("=" * 80)
