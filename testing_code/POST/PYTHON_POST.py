import requests
import json

def create_cin(Om2mLable, value):
    
    headers = {
        'X-M2M-Origin': "a8d#J7:5Zi@la!5",
        'Content-type': f'application/json;ty=4'
        }
    body = {
        "m2m:cin": {
            "con": "{}".format(value),
            "lbl": Om2mLable,
            "cnf": "text"
        }
    }
    OM2M_URL=f"http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-PL96-00/Data"
    try:
        response = requests.post(OM2M_URL, json=body, headers=headers)
        print(f'Return code: {response.status_code}')
        return response.status_code
    except TypeError:
        response = requests.post(OM2M_URL, data=json.dumps(body), headers=headers)
        return response.status_code
        return response.status_code


data = "[1767621020,230, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"
Om2mLable =["AE-SL","SL-PL96-00","V2.0.1"]
create_cin(Om2mLable, data)
    