import os
import base64
import requests
import json
from dotenv import load_dotenv

class Mathpix:
    def __init__(self, mathpix_app_id, mathpix_app_key):
        """
        Initialize the Mathpix class with Mathpix app ID and app key.

        Args:
        - mathpix_app_id (str): Mathpix app ID.
        - mathpix_app_key (str): Mathpix app key.
        """
        self.mathpix_app_id = mathpix_app_id
        self.mathpix_app_key = mathpix_app_key
        self.__set_config(mathpix_app_id, mathpix_app_key)

    def __set_config(self, mathpix_app_id, mathpix_app_key):
        """
        Set Mathpix app ID and app key in the environment variables.

        Args:
        - mathpix_app_id (str): Mathpix app ID.
        - mathpix_app_key (str): Mathpix app key.
        """
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

        Args:
        - image_path (str): Path to the local image file.

        Returns:
        - str: Base64 encoded image string.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    def image_uri(self, filename):
        """
        Encodes image to a base64 string using data URI scheme.

        Args:
        - filename (str): Name of the image file.

        Returns:
        - str: Data URI string of the image.
        """
        image_data = open(filename, "rb").read()
        return "data:image/jpg;base64," + base64.b64encode(image_data).decode()

    def image_content(self, contents):
        """
        Encodes image contents to a base64 string using data URI scheme.

        Args:
        - contents (str): Image content to encode.

        Returns:
        - str: Data URI string of the image.
        """
        encoded_string = base64.b64encode(contents).decode()
        return f"data:image/jpg;base64,{encoded_string}"
    
    def latex(self, args, timeout=30):
        """
        Sends a POST request to the Mathpix API to recognize and extract LaTeX from images.

        Args:
        - args (dict): Request payload for the Mathpix API.
        - timeout (int, optional): Timeout value for the request (in seconds).

        Returns:
        - dict: JSON response from the Mathpix API.
        """
        r = requests.post(self.service,
            data=json.dumps(args), headers=self.default_headers, timeout=timeout)
        return json.loads(r.text)
