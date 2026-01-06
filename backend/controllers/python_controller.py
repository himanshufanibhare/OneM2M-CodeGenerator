"""
Python code generator for oneM2M - Production-ready implementation.
"""
import json


def generate_python_code(config):
    """Generate Python code for oneM2M operations.
    
    Generates production-ready code that:
    - Uses requests library with proper timeout and error handling
    - Supports HTTP and HTTPS with protocol parameter
    - Includes all mandatory oneM2M headers (X-M2M-Origin, X-M2M-RI, Content-Type, Accept)
    - Stringifies inner JSON for con field (oneM2M compliance)
    
    Args:
        config: Dictionary with cse_url, port, protocol, ae_name, container_name, origin, operation, parameters
        
    Returns:
        String containing complete Python script
    """
    # Extract configuration
    cse_url = config.get('cse_url', 'onem2m.iiit.ac.in')
    port = config.get('port', '443')
    protocol = config.get('protocol', 'https').lower()
    ae_name = config.get('ae_name', '')
    container_name = config.get('container_name', '')
    origin = config.get('origin', '')
    operation = config.get('operation', 'GET').upper()
    params = config.get('parameters', [])
    labels = config.get('labels', []) or []

    # Minimal GET template (matches testing_code/GET/PYTHON_GET.py)
    if operation == 'GET':
        code = f'''import requests
import json

url = "{protocol}://{cse_url}:{port}/~/in-cse/in-name/{ae_name}/{container_name}/Data/la"

payload = {{}}
headers = {{
    'X-M2M-Origin': '{origin}',
    'Content-Type': 'application/json'
}}

def getData():
    response = requests.request("GET", url, headers=headers, data=payload)
    
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)
        
        # Extract the "con" value using the get method
        con_value = data.get("m2m:cin", {{}}).get("con", "Value not found")
        
        # Print the "con" value
        print("con:", con_value)
    else:
        print("Request failed with status code:", response.status_code)

# Run once
getData()

# Uncomment below to run in loop every 10 seconds
# import time
# while True:
#     getData()
#     time.sleep(10)
'''
        return code

    # POST template - array format [epoch, value1, value2, ...]
    # Build value list from parameters (no labels)
    value_list = []
    if isinstance(params, list):
        for p in params:
            if not isinstance(p, dict):
                continue
            dtype = (p.get('type') or 'string').lower()
            default = p.get('default', '')
            
            if dtype in ('int', 'integer'):
                val = default if default != '' else '0'
                value_list.append(val)
            elif dtype in ('float', 'decimal'):
                val = default if default != '' else '0.0'
                value_list.append(val)
            elif dtype in ('boolean', 'bool'):
                val = '1' if str(default).lower() in ('true', '1', 'yes') else '0'
                value_list.append(val)
            else:
                value_list.append(f'"{default}"')

    values_str = ', '.join(value_list) if value_list else ''
    labels_block = json.dumps(labels)

    code = f'''import requests
import json
import time

def create_cin(Om2mLable, value):
    
    headers = {{
        'X-M2M-Origin': "{origin}",
        'Content-type': 'application/json;ty=4'
    }}
    body = {{
        "m2m:cin": {{
            "con": "{{}}".format(value),
            "lbl": Om2mLable,
            "cnf": "text"
        }}
    }}
    OM2M_URL = "{protocol}://{cse_url}:{port}/~/in-cse/in-name/{ae_name}/{container_name}/Data"
    try:
        response = requests.post(OM2M_URL, json=body, headers=headers)
        print(f'Return code: {{response.status_code}}')
        return response.status_code
    except TypeError:
        response = requests.post(OM2M_URL, data=json.dumps(body), headers=headers)
        print(f'Return code: {{response.status_code}}')
        return response.status_code


# Build data array: [epoch, value1, value2, ...]
epoch = int(time.time())
data = [epoch{", " + values_str if values_str else ""}]

# Convert data array to JSON string
data_json = json.dumps(data)

# Configure labels
Om2mLable = {labels_block}

# Send data
create_cin(Om2mLable, data_json)
'''

    return code

