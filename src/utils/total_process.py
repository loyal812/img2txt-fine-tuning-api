
import os
import gc
import time
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
from src.mongodb.MongoDBClass import MongoDBClass

from src.utils.utils_funcs import is_image_file, is_pdf_file, is_text_file, copy_file_to_folder, get_image_pages_percentage

def total_process(args):
    start_time = time.time()
    
    payload_data = read_json(args['payload_dir'])

    # Extract MongoDB URI from payload data
    mongo_uri = payload_data["mongo_uri"]

    # Call class instance
    mongodb = MongoDBClass(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=mongo_uri)

    is_available = mongodb.check_validation_api(api_key=str(Path(args['api_key'])), user=str(Path(args['user'])))

    if is_available['status'] == "success":
        print("valid api key")
        # Separate the data 
        separate_data(payload_data["data_path"], payload_data["threshold_image_percent_of_pdf"])

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
        fine_tuned_model = fine_tune.finetune()

        # Write into log file
        end_time = time.time()
        msg = f"Total processing time: {end_time - start_time} seconds"
        print(msg)

        return {"status": "success", "fine_tuned_model": fine_tuned_model}
    else:
        print("invalide api key")

        return {"status": "failed", "message": "invalide api key"}


def save_to_txt(payload_data, result: str):
    """
    Save the analyzed result to a text file.

    Args:
    - payload_data (dict): Data containing the path where the file should be saved.
    - result (str): The analyzed result to be saved to the file.
    """
    current_time = datetime.now().strftime('%y_%m_%d_%H_%M_%S')
    train_path = os.path.join(payload_data["data_path"], "train_data")
    os.makedirs(train_path, exist_ok=True)  # This line will create the directory if it doesn't exist

    with open(f'{train_path}/{current_time}_data.txt', "a", encoding="utf-8") as f:
        f.write(result + "\n\n")  # Append the new data to the end of the file

def img2txt(img_translator: ImageTranslator, image):
    """
    Analyzes the given image using the ImageTranslator and retrieves the textual content from the analysis.

    Args:
    - img_translator (ImageTranslator): An instance of the ImageTranslator class.
    - image: The image to be analyzed.

    Returns:
    - str: The textual content obtained from the analysis.
    
    Raises:
    - Exception: If a valid response is not obtained after the maximum number of retries.
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
    Create a single result from the provided results and initiate a conversation with ChatGPT.

    Args:
    - payload_data (dict): Data containing the merge_prompt, api_key, and language_model for ChatGPT.
    - results (list of str): List of individual results to be included in the conversation.

    Returns:
    - str: The response from ChatGPT after the conversation.

    Raises:
    - Exception: If a valid response is not obtained from ChatGPT after the maximum number of retries.
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

def separate_data(path, threshold):
    """
    Separate the files in the specified directory based on their type and content.

    Args:
    - path (str): The path to the source folder.
    - threshold (float): The threshold for determining the content type of PDF files.
    """
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
                if get_image_pages_percentage(file_path) < threshold:
                    # pdf is mostly consist of text
                    copy_file_to_folder(file_path, train_folder)
                else:
                    # pdf is mostly consist of image
                    copy_file_to_folder(file_path, pdf_folder)