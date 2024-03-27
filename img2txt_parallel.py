
import os
import gc
import time
import argparse
from pathlib import Path
import concurrent.futures
from datetime import datetime

from src.utils.read_json import read_json
from src.utils.image_translator import ImageTranslator
from src.utils.chatgpt_communicator import ChatGPTCommunicator


def main(args):
    """
    The main entry point for the image to text conversion process.

    Args:
    - args (argparse.Namespace): Parsed command-line arguments
    """
    # Timer
    start_time = time.time()

    # Payload
    payload_data = read_json(args.payload_dir)
    
    # Read images from the image directory
    image_data_path = payload_data["images_data_path"]
    image_list = [img for img in os.listdir(image_data_path) if img.endswith(".png") or img.endswith(".jpeg") or img.endswith(".jpg")]

    # Create an instance of ImageTranslator for image encoding and translation
    img_translator = ImageTranslator(api_key=payload_data["api_key"])
    
    # Loop over number of images and append all images
    # NOTE: User can upload image and add image URLs or just upload image or just add image URLs
    images = []
    if (len(image_list) > 0) and (len(payload_data["image_url"]) > 0):
        for image in image_list:
            image_path = os.path.join(image_data_path, image)
            # Encode image
            base64_image = img_translator.encode_image(image_path)
            images.append((base64_image, False, "auto"))
        for img_url in payload_data["image_url"]:
            images.append((img_url, True, "auto"))
    elif (len(image_list) > 0) and (len(payload_data["image_url"]) == 0):
        for image in image_list:
            image_path = os.path.join(image_data_path, image)
            # Encode image
            base64_image = img_translator.encode_image(image_path)
            images.append((base64_image, False, "auto"))
    elif (len(image_list) == 0) and (len(payload_data["image_url"]) > 0):
        for img_url in payload_data["image_url"]:
            images.append((img_url, True, "auto"))

    for image in images:
        if payload_data["is_parallel"]:
            params = [{
                img_translator: img_translator,
                image: image
            }] * payload_data["parallel_count"]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(lambda args: img2txt(*args), params))
            
            result = make_one_result(payload_data, results)
        else:
            result = img2txt(img_translator, image)

        save_to_txt(payload_data, result)

    
    # Write into log file
    end_time = time.time()
    msg = f"Total processing time: {end_time - start_time} seconds"
    print(msg)

    # Delete class objects and clean the buffer memory using the garbage collection
    gc.collect()

def save_to_txt(payload_data, result: str):
    """
    Save the result to a text file.

    Args:
    - payload_data (dict): Payload data
    - result (str): The result to be saved
    """
    current_time = datetime.now().strftime('%y_%m_%d_%H_%M_%S')
    train_path = os.path.join(payload_data["data_path"], "train_data")
    os.makedirs(train_path, exist_ok=True)  # This line will create the directory if it doesn't exist

    with open(f'{train_path}/{current_time}_data.txt', "a", encoding="utf-8") as f:
        f.write(result + "\n\n")  # Append the new data to the end of the file

def img2txt(img_translator: ImageTranslator, image):
    """
    Process image to text using the ImageTranslator instance.

    Args:
    - img_translator (ImageTranslator): Instance of ImageTranslator
    - image (str): Image data

    Returns:
    - str: Translated text from the image
    """
    max_retries = 5
    last_error = ""

    img_translator_response = None  # Define the variable and initialize it to None

    for attempt in range(max_retries):
        try:
            response = img_translator.analyze_images([image])

            if "choices" in response and response["choices"]:
                first_choice = response["choices"][0]
                if "message" in first_choice and "content" in first_choice["message"] and first_choice["message"]["content"]:
                    img_translator_response = first_choice["message"]["content"]
                    break  # Successful response, break out of the loop
                else:
                    last_error = "No valid content in the response."
            else:
                last_error = "The response structure is not as expected."

        except Exception as e:
            last_error = f"Attempt {attempt + 1} failed: {e}"

        if img_translator_response:
            break  # If a successful response is obtained, exit the loop

    if img_translator_response is None:
        raise Exception("Failed to get a valid response after " + str(max_retries) + " attempts. Last error: " + last_error)
    
    return img_translator_response

def make_one_result(payload_data, results: [str]):
    """
    Combine and process the results using ChatGPT.

    Args:
    - payload_data (dict): Payload data
    - results (list): List of results from image processing

    Returns:
    - str: Final result after processing with ChatGPT
    """
    response = payload_data["merge_prompt"]
    for index, result in enumerate(results):
        response += f"\nresult {index + 1}: {result}"

    # Create chatGPT communicator
    chatgpt_communicator = ChatGPTCommunicator(api_key=payload_data["api_key"], language_model=payload_data["language_model"])

    # Start conversation with ChatGPT using the transcribed or translated text
    chatgpt_communicator.create_chat(response)

    # Get conversation with ChatGPT
    max_retries = 3
    chatgpt_response = None

    for attempt in range(max_retries):
        try:
            chatgpt_response = chatgpt_communicator.get_response()
            # Check if the response is valid (not None and not empty)
            if chatgpt_response:
                break  # Valid response, break out of the loop
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise Exception(f"Failed to get a valid response from ChatGPT after {max_retries} attempts. Last error: {e}")

    # Print response and use it somewhere else
    # print(chatgpt_response)


    return chatgpt_response

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
    p = argparse.ArgumentParser(description="Image to Text with parallel.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="Data directory")
    args = p.parse_args()

    main(args)
