import sys
import os
import json
import importlib
# Ensure project root on path (script may be executed from different cwd)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import the Flask app object from the module (not package) to avoid running the server
mod = importlib.import_module('backend.app')
flask_app = getattr(mod, 'app')

payload = {
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
print("TEST: oneM2M Code Generation with Dynamic URL Construction")
print("=" * 80)
print(f"Target URL: {payload['protocol']}://{payload['cse_url']}:{payload['port']}")
print(f"Path: /~/in-cse/in-name/{payload['ae_name']}/{payload['container_name']}/{payload['sub_container']}")
print("=" * 80)

with flask_app.test_client() as client:
    resp = client.post('/generate', json=payload)
    print('STATUS:', resp.status_code)
    
    if resp.status_code == 200:
        result = resp.get_json()
        code = result.get('code', '')
        print("\n✓ Code generated successfully!")
        print(f"Filename: {result.get('filename')}")
        print(f"Controller: {result.get('controller')}")
        print(f"Code length: {len(code)} bytes")
        
        # Verify critical parts
        print("\n" + "=" * 80)
        print("VERIFICATION:")
        print("=" * 80)
        
        checks = [
            ('WiFiSSLClient (HTTPS)', 'WiFiSSLClient' in code),
            ('Dynamic path construction', 'String path = "/~/in-cse/in-name/"' in code),
            ('AE variable used', 'path += aeName' in code),
            ('Container variable used', 'path += containerName' in code),
            ('Sub-container variable used', 'path += subContainer' in code),
            ('ArduinoJson library', '#include <ArduinoJson.h>' in code),
            ('Mandatory X-M2M-Origin header', 'X-M2M-Origin' in code),
            ('Mandatory X-M2M-RI header', 'X-M2M-RI' in code),
            ('Mandatory Content-Type header', 'Content-Type: application/json;ty=4' in code),
            ('Connection close header', 'Connection: close' in code),
            ('con field as string', 'cinDoc["m2m:cin"]["con"] = innerJson' in code),
        ]
        
        for check_name, check_result in checks:
            status = "✓" if check_result else "✗"
            print(f"{status} {check_name}")
        
        # Extract and display critical code snippets
        print("\n" + "=" * 80)
        print("KEY CODE SNIPPETS:")
        print("=" * 80)
        
        # Find path construction code
        if 'String path =' in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if 'String path =' in line:
                    print("\nPath Construction:")
                    for j in range(i, min(i+6, len(lines))):
                        print(f"  {lines[j]}")
                    break
        
        # Find HTTP request building
        if 'POST' in code and 'HTTP/1.1' in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if 'String request = "POST' in line or 'request = "POST' in line or 'request += path' in line:
                    print("\nHTTP Request Building:")
                    for j in range(max(0,i-1), min(i+8, len(lines))):
                        print(f"  {lines[j]}")
                    break
        
    else:
        error_data = resp.get_data(as_text=True)
        print(f"\n✗ Generation failed!")
        print(f"Error: {error_data}")
