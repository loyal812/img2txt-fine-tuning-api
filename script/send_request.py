import requests
import json
import os

def send_request(api_url, data):
    """Sends a POST request to the specified URL with the provided data."""
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        # Convert WindowsPath to string in the data dictionary
        data = {key: str(val) if isinstance(val, os.PathLike) else val for key, val in data.items()}

        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"An error occurred while sending the request: {e}")

