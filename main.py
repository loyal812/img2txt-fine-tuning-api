
import os
import gc
import time
import argparse
from pathlib import Path
import concurrent.futures
from datetime import datetime
import json

from src.utils.read_json import read_json
from src.utils.image_translator import ImageTranslator
from src.utils.chatgpt_communicator import ChatGPTCommunicator
from src.pdf2img.Pdf2ImgClass import Pdf2ImgClass
from src.finetune.FineTuningClass import FineTuningClass
from src.mathpix.Mathpix import Mathpix

from src.utils.utils import is_image_file, is_pdf_file, is_text_file, copy_file_to_folder, get_image_pages_percentage

def main(args):
    start_time = time.time()
    
    payload_data = read_json(args.payload_dir)

    # Separate the data 
    separate_data(payload_data["data_path"], payload_data["threasold_image_percent_of_pdf"])

    # pdf to image feature
    pdf2img = Pdf2ImgClass(
        data_path=payload_data["pdf_data_path"],
        parent_path=payload_data["data_path"])
    
    pdf2img.pdf2img()

    # img to text feature
    # Read images from the image directory
    image_list = []
    image_data_path = payload_data["images_data_path"]

    try:
        image_list = [img for img in os.listdir(image_data_path) if img.endswith(".png") or img.endswith(".jpeg") or img.endswith(".jpg")]
    except FileNotFoundError:
        print("The specified path does not exist or is inaccessible.")

    # Call class instance
    img_translator = ImageTranslator(api_key=payload_data["api_key"])
    mathpix = Mathpix(mathpix_app_id=payload_data["mathpix_app_id"], mathpix_app_key=payload_data["mathpix_app_key"])
    
    # Loop over number of images and append all images
    # NOTE: User can upload image and add image URLs or just upload image or just add image URLs
    images = []
    image_paths = []
    if (len(image_list) > 0) and (len(payload_data["image_url"]) > 0):
        for image in image_list:
            image_path = os.path.join(image_data_path, image)
            # Encode image
            base64_image = img_translator.encode_image(image_path)
            images.append((base64_image, False, "auto"))
            image_paths.append(image_path)
        for img_url in payload_data["image_url"]:
            images.append((img_url, True, "auto"))
            image_paths.append(img_url)
    elif (len(image_list) > 0) and (len(payload_data["image_url"]) == 0):
        for image in image_list:
            image_path = os.path.join(image_data_path, image)
            # Encode image
            base64_image = img_translator.encode_image(image_path)
            images.append((base64_image, False, "auto"))
            image_paths.append(image_path)
    elif (len(image_list) == 0) and (len(payload_data["image_url"]) > 0):
        for img_url in payload_data["image_url"]:
            images.append((img_url, True, "auto"))
            image_paths.append(img_url)

    if payload_data["is_gpt"]:
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
    else:
        for path in image_paths:
            result = mathpix.latex({
                'src': mathpix.image_uri(path),
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

            # print(json.loads(json.dumps(result, indent=4, sort_keys=True))["text"])

            save_to_txt(payload_data, json.loads(json.dumps(result, indent=4, sort_keys=True))["text"])

    # fine tuning
    fine_tune = FineTuningClass(
        data_path=payload_data["train_data_path"],
        parent_path=payload_data["data_path"],
        api_key=payload_data["api_key"],
        model=payload_data["model"],
        temperature=payload_data["temperature"],
        max_retries=payload_data["max_retries"])
    
    # Generate the train and eval data
    fine_tune.train_generation()

    # Generate the jsonl
    fine_tune.jsonl_generation()

    # Fine tuning
    fine_tune.finetune()

    # Write into log file
    end_time = time.time()
    msg = f"Total processing time: {end_time - start_time} seconds"
    print(msg)
    gc.collect()

def save_to_txt(payload_data, result: str):
    current_time = datetime.now().strftime('%y_%m_%d_%H_%M_%S')
    train_path = os.path.join(payload_data["data_path"], "train_data")
    os.makedirs(train_path, exist_ok=True)  # This line will create the directory if it doesn't exist

    with open(f'{train_path}/{current_time}_data.txt', "a", encoding="utf-8") as f:
        f.write(result + "\n\n")  # Append the new data to the end of the file

def img2txt(img_translator: ImageTranslator, image):
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

def separate_data(path, threasold):
    source_folder = path
    images_folder = os.path.join(path, "images")
    pdf_folder = os.path.join(path, "pdf")
    train_folder = os.path.join(path, "train_data")

    file_list = os.listdir(source_folder)
    for file_name in file_list:
        file_path = os.path.join(source_folder, file_name)
        if os.path.isfile(file_path):
            if is_image_file(file_path):
                copy_file_to_folder(file_path, images_folder)
            elif is_text_file(file_path):
                copy_file_to_folder(file_path, train_folder)
            elif is_pdf_file(file_path):
                # if check_pdf_content(file_path) == "text":
                #     copy_file_to_folder(file_path, train_folder)
                # if has_text(file_path):
                #     copy_file_to_folder(file_path, train_folder)
                if get_image_pages_percentage(file_path) < threasold:
                    # pdf is mostly consist of text
                    copy_file_to_folder(file_path, train_folder)
                else:
                    # pdf is mostly consist of image
                    copy_file_to_folder(file_path, pdf_folder)

if __name__ == "__main__":
    """
    Form command lines
    """
    # Clean up buffer memory
    gc.collect()

    # Current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Payload directory
    test_name    = "regression_test013"
    payload_name = "payload.json"
    payload_dir  = os.path.join(current_dir, "test", "regression", test_name, "payload", payload_name)

    # Add options
    p = argparse.ArgumentParser()
    p = argparse.ArgumentParser(description="Translate text within an image.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="payload directory to the test example")
    args = p.parse_args()

    main(args)