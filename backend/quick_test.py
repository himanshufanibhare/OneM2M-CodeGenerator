import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.controllers.arduino import generate_arduino_code

config = {
    'controller': 'arduino_nano',
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

print("=" * 80)
print("TESTING: Arduino Code Generator with Dynamic URL Construction")
print("=" * 80)
print(f"Target: https://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN03-00/Data")
print("=" * 80)

code = generate_arduino_code(config)

print("\n✓ Code generated successfully!")
print(f"Code length: {len(code)} bytes\n")

# Verification checks
checks = [
    ('WiFiSSLClient for HTTPS', 'WiFiSSLClient client;' in code),
    ('Dynamic path construction', 'String path = "/~/in-cse/in-name/"' in code),
    ('AE variable in path', 'path += aeName' in code),
    ('Container variable in path', 'path += containerName' in code),
    ('Sub-container variable in path', 'path += subContainer' in code),
    ('ArduinoJson library', '#include <ArduinoJson.h>' in code),
    ('X-M2M-Origin header', 'X-M2M-Origin' in code),
    ('X-M2M-RI header', 'X-M2M-RI' in code),
    ('Content-Type header', 'Content-Type: application/json;ty=4' in code),
    ('Connection close', 'Connection: close' in code),
    ('con as string (not object)', 'cinDoc["m2m:cin"]["con"] = innerJson' in code),
]

print("VERIFICATION:")
print("=" * 80)
all_passed = True
for check_name, check_result in checks:
    status = "✓" if check_result else "✗"
    print(f"{status} {check_name}")
    if not check_result:
        all_passed = False

print("=" * 80)

if all_passed:
    print("\n✓✓✓ ALL CHECKS PASSED! Code is oneM2M compliant.")
else:
    print("\n✗✗✗ SOME CHECKS FAILED!")

# Show key snippets
print("\n" + "=" * 80)
print("PATH CONSTRUCTION CODE:")
print("=" * 80)
lines = code.split('\n')
for i, line in enumerate(lines):
    if 'Build oneM2M resource path' in line:
        for j in range(i, min(i+8, len(lines))):
            print(lines[j])
        break

print("\n" + "=" * 80)
print("CLIENT TYPE:")
print("=" * 80)
for i, line in enumerate(lines):
    if 'WiFiClient' in line or 'WiFiSSLClient' in line:
        print(line)
        break

# Save to file for inspection
output_path = os.path.join(os.path.dirname(__file__), '..', 'test_output_arduino.ino')
with open(output_path, 'w') as f:
    f.write(code)
print(f"\n✓ Full code saved to: {output_path}")
