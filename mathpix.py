import os
import gc
import time
import json
import argparse
from pathlib import Path

from src.utils.read_json import read_json
from src.mathpix.Mathpix import Mathpix

def mathpix(args):
    """
    main entry point
    """

    # Payload
    payload_data = read_json(args.payload_dir)

    # Read images from the image directory
    image_data_path = payload_data["images_data_path"]
    image_list = [img for img in os.listdir(image_data_path) if img.endswith(".png") or img.endswith(".jpeg") or img.endswith(".jpg")]

    # Call class instance
    mathpix_api = Mathpix(mathpix_app_id=payload_data["mathpix_app_id"], mathpix_app_key=payload_data["mathpix_app_key"])
    
    # Loop over number of images and append all images
    # NOTE: User can upload image and add image URLs or just upload image or just add image URLs
    images = []
    if (len(image_list) > 0) and (len(payload_data["image_url"]) > 0):
        for image in image_list:
            image_path = os.path.join(image_data_path, image)
            # # Encode image
            # base64_image = mathpix_api.encode_image(image_path)
            # images.append((base64_image, False, "auto"))
            images.append(image_path)
            # images.append((image_path, True, "auto"))
        for img_url in payload_data["image_url"]:
            images.append(img_url)
            # images.append((img_url, True, "auto"))
    elif (len(image_list) > 0) and (len(payload_data["image_url"]) == 0):
        for image in image_list:
            image_path = os.path.join(image_data_path, image)
            # Encode image
            # base64_image = mathpix_api.encode_image(image_path)
            # images.append((base64_image, False, "auto"))
            images.append(image_path)
            # images.append((image_path, True, "auto"))
    elif (len(image_list) == 0) and (len(payload_data["image_url"]) > 0):
        for img_url in payload_data["image_url"]:
            images.append(img_url)
            # images.append((img_url, True, "auto"))


    # Loop over number of requests
    for image in images:
        print("ssss", image)
        # Timer
        start_time = time.time()

        # Instantiate class
        result = mathpix_api.latex({
            'src': mathpix_api.image_uri(image),
            'ocr': ['math', 'text'],
            'formats': ['text', 'latex_styled', 'asciimath', 'mathml', 'latex_simplified'],
            'format_options': {
                'text': {
                    'transforms': ['rm_spaces', 'rm_newlines'],
                    'math_delims': ['$', '$']
                },
                'latex_styled': {'transforms': ['rm_spaces']}
            }
        })

        print(json.loads(json.dumps(result, indent=4, sort_keys=True))["text"])

        # Print time
        end_time = time.time()
        msg = f"Total processing time for payload {end_time - start_time} seconds"
        print(msg)
    
    
    # Delete class objects and clean the buffer memory using the garbage collection
    gc.collect()


if __name__ == "__main__":
    # Clean up buffer memory before starting the program
    gc.collect()

    # Default values for command line arguments
    # Current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Payload directory
    test_name    = "regression_test013"
    payload_name = "img2txt_payload.json"
    payload_dir  = os.path.join(current_dir, "test", "regression", test_name, "payload", payload_name)

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="Convert image to text using MathPIX API.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="Data directory")
    args = p.parse_args()

    mathpix(args)
