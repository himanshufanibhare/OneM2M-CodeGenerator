import requests
import json

url = "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SR/SR-EM/SR-EM-KH04-01/Data/la"

payload = {}
headers = {
    'X-M2M-Origin': 'iiith_guest:iiith_guest',
    'Content-Type': 'application/json'
}

def getData():
    response = requests.request("GET", url, headers=headers, data=payload)
    
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)
        
        # Extract the "con" value using the get method
        con_value = data.get("m2m:cin", {}).get("con", "Value not found")
        
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