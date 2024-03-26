import os
import base64
import requests
import json
from dotenv import load_dotenv

class Mathpix:
    def __init__(self, mathpix_app_id, mathpix_app_key):
        self.mathpix_app_id = mathpix_app_id
        self.mathpix_app_key = mathpix_app_key
        self.set_config(mathpix_app_id, mathpix_app_key)

    def set_config(self, mathpix_app_id, mathpix_app_key):
        if mathpix_app_id:
            self.mathpix_app_id = mathpix_app_id
            self.mathpix_app_key = mathpix_app_key
        else:
            load_dotenv()
            self.mathpix_app_id = os.getenv("MATHPIX_APP_ID")
            self.mathpix_app_key = os.getenv("MATHPIX_APP_KEY")

        if self.mathpix_app_id is not None and self.mathpix_app_key is not None:
            os.environ["MATHPIX_APP_ID"] = self.mathpix_app_id
            os.environ["MATHPIX_APP_KEY"] = self.mathpix_app_key
        else:
            # Handle the absence of the environment variable
            # You might want to log an error, raise an exception, or provide a default value
            # For example, setting a default value
            os.environ["MATHPIX_APP_ID"] = mathpix_app_id
            os.environ["MATHPIX_APP_KEY"] = mathpix_app_key

        self.default_headers = {
            'app_id': self.mathpix_app_id,
            'app_key': self.mathpix_app_key,
            'Content-type': 'application/json'
        }

        self.service = 'https://api.mathpix.com/v3/text'

    def encode_image(self, image_path):
        """
        Encodes a local image to a base64 string.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    def image_uri(self, filename):
        image_data = open(filename, "rb").read()
        return "data:image/jpg;base64," + base64.b64encode(image_data).decode()

    def image_content(self, contents):
        encoded_string = base64.b64encode(contents).decode()
        return f"data:image/jpg;base64,{encoded_string}"
    
    def latex(self, args, timeout=30):
        r = requests.post(self.service,
            data=json.dumps(args), headers=self.default_headers, timeout=timeout)
        return json.loads(r.text)
