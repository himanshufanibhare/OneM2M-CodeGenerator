from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import io
import re
import requests
import json
import urllib3

# Disable SSL warnings for testing (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from controllers import (
    generate_arduino_code,
    generate_esp32_code,
    generate_esp8266_code,
    generate_python_code
)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)


# Basic routes
@app.route('/')
def index():
    return render_template('controller_select.html')


@app.route('/configure/<controller>')
def configure(controller):
    valid_controllers = ['arduino_nano', 'esp32', 'esp8266', 'python']
    if controller not in valid_controllers:
        return "Invalid controller", 400
    return render_template('configure.html', controller=controller)


@app.route('/generate-view')
def generate_view():
    return render_template('generate.html')


def validate_request_config(data, controller):
    """Validate incoming config for URL/port and platform rules.

    Returns (True, None) or (False, message)
    """
    cse = (data.get('cse_url') or '').strip()
    port = data.get('port')
    protocol = data.get('protocol', 'https').lower()

    if not cse:
        return False, 'CSE host is required.'

    if re.match(r'^https?://', cse, re.IGNORECASE):
        return False, 'CSE host should not include a protocol (enter host only).'

    try:
        p = int(port)
        if not (1 <= p <= 65535):
            return False, 'Port must be between 1 and 65535.'
    except Exception:
        return False, 'Port must be an integer.'
    
    # Validate protocol
    if protocol not in ('http', 'https'):
        return False, 'Protocol must be either http or https.'
    
    data['protocol'] = protocol  # Ensure protocol is in data for generators to use

    if controller in ('esp32', 'esp8266', 'arduino_nano'):
        if cse.lower() in ('localhost', '127.0.0.1', '::1'):
            return False, 'Localhost is not allowed for microcontroller targets.'

    return True, None


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json or {}
    controller = data.get('controller')
    
    print(f"[DEBUG] Received generate request for controller: {controller}")
    print(f"[DEBUG] Config data: {data}")

    valid, msg = validate_request_config(data, controller)
    if not valid:
        print(f"[DEBUG] Validation failed: {msg}")
        return jsonify({'error': msg}), 400

    try:
        if controller == 'arduino_nano':
            code = generate_arduino_code(data)
            filename = 'onem2m_client.ino'
        elif controller == 'esp32':
            code = generate_esp32_code(data)
            filename = 'onem2m_client.ino'
        elif controller == 'esp8266':
            code = generate_esp8266_code(data)
            filename = 'onem2m_client.ino'
        elif controller == 'python':
            code = generate_python_code(data)
            filename = 'onem2m_client.py'
        else:
            return jsonify({'error': 'Invalid controller'}), 400
        
        print(f"[DEBUG] Code generated successfully, length: {len(code)}")
        return jsonify({'code': code, 'filename': filename, 'controller': controller})
        
    except Exception as e:
        print(f"[ERROR] Failed to generate code: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate code: {str(e)}'}), 500


@app.route('/download', methods=['POST'])
def download():
    data = request.json or {}
    code = data.get('code', '')
    filename = data.get('filename', 'code.txt')
    stream = io.BytesIO(code.encode('utf-8'))
    stream.seek(0)
    return send_file(stream, as_attachment=True, download_name=filename, mimetype='text/plain')


@app.route('/test-get', methods=['POST'])
def test_get():
    """Test GET operation to oneM2M server"""
    data = request.json or {}
    
    print(f"[DEBUG] Test GET request: {data}")
    
    # Validate config
    valid, msg = validate_request_config(data, 'python')
    if not valid:
        return jsonify({'error': msg}), 400
    
    try:
        # Build URL - use /la endpoint to get latest resource
        protocol = data.get('protocol', 'http')
        cse_url = data.get('cse_url')
        port = data.get('port')
        ae_name = data.get('ae_name')
        container_name = data.get('container_name')
        origin = data.get('origin')
        
        # GET endpoint: /~/in-cse/in-name/{AE}/{Container}/Data/la
        url = f"{protocol}://{cse_url}:{port}/~/in-cse/in-name/{ae_name}/{container_name}/Data/la"
        
        # Set headers
        headers = {
            'X-M2M-Origin': origin,
            'Accept': 'application/json'
        }
        
        print(f"[DEBUG] GET URL: {url}")
        print(f"[DEBUG] Headers: {headers}")
        
        # Execute GET request
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        print(f"[DEBUG] Response Status: {response.status_code}")
        
        return jsonify({
            'success': True,
            'status_code': response.status_code,
            'response': response.text,
            'url': url
        })
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout. Server did not respond.'}), 408
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection error. Could not reach server.'}), 503
    except Exception as e:
        print(f"[ERROR] Test GET failed: {str(e)}")
        return jsonify({'error': f'Test failed: {str(e)}'}), 500


@app.route('/test-post', methods=['POST'])
def test_post():
    """Test POST operation to oneM2M server"""
    data = request.json or {}
    
    print(f"[DEBUG] Test POST request: {data}")
    
    # Validate config
    valid, msg = validate_request_config(data, 'python')
    if not valid:
        return jsonify({'error': msg}), 400
    
    try:
        # Build URL
        protocol = data.get('protocol', 'http')
        cse_url = data.get('cse_url')
        port = data.get('port')
        ae_name = data.get('ae_name')
        container_name = data.get('container_name')
        origin = data.get('origin')
        params = data.get('parameters', [])
        labels = data.get('labels', [])
        
        url = f"{protocol}://{cse_url}:{port}/~/in-cse/in-name/{ae_name}/{container_name}/Data"
        
        # Build payload
        inner_data = {}
        for p in params:
            if isinstance(p, dict):
                name = p.get('name')
                value = p.get('default', '')
                dtype = p.get('type', 'string')
                
                if dtype in ('int', 'integer'):
                    try:
                        inner_data[name] = int(value)
                    except:
                        inner_data[name] = 0
                elif dtype in ('float', 'decimal'):
                    try:
                        inner_data[name] = float(value)
                    except:
                        inner_data[name] = 0.0
                elif dtype in ('boolean', 'bool'):
                    inner_data[name] = str(value).lower() in ('true', '1', 'yes')
                else:
                    inner_data[name] = str(value)
        
        # Build oneM2M payload
        payload = {
            "m2m:cin": {
                "con": json.dumps(inner_data)
            }
        }
        
        # Add labels if provided
        if labels:
            payload["m2m:cin"]["lbl"] = labels
        
        # Set headers
        headers = {
            'X-M2M-Origin': origin,
            'Content-Type': 'application/json;ty=4',
            'Accept': 'application/json'
        }
        
        print(f"[DEBUG] POST URL: {url}")
        print(f"[DEBUG] Payload: {json.dumps(payload, indent=2)}")
        print(f"[DEBUG] Headers: {headers}")
        
        # Execute POST request
        response = requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
        
        print(f"[DEBUG] Response Status: {response.status_code}")
        
        return jsonify({
            'success': True,
            'status_code': response.status_code,
            'response': response.text,
            'url': url,
            'payload': payload
        })
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout. Server did not respond.'}), 408
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection error. Could not reach server.'}), 503
    except Exception as e:
        print(f"[ERROR] Test POST failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Test failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
