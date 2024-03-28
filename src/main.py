import os
import sys

# Get the current script's directory
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the project root path
project_root = os.path.abspath(os.path.join(current_script_directory, os.pardir))

# Append the project root and current script directory to the system path
sys.path.append(project_root)
sys.path.append(current_script_directory)

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.status import HTTP_201_CREATED

from src.models.basic_model import BasicModel
from src.models.create_api_model import CreateAPIModel
from src.models.chatting_model import ChattingModel
from src.models.main_model import MainModel

from utils.total_process import total_process
from utils.create_api import create_api_key
from src.utils.delete_api import delete_api_key
from src.utils.check_api import check_api_key
from utils.chatting import chatting

# Create a FastAPI application
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://example.com",
    "https://www.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Define a route to handle the root endpoint and redirect to the API documentation
@app.get("/")
async def root():
    return RedirectResponse(app.docs_url)

# Function to get the payload directory
def __get_payload_dir(data_id: str):
    """Get the directory path for the payload file."""
    payload_name = "payload.json"
    if data_id == "":
        test_name  = "regression_test013"
    else:
        test_name  = data_id

    payload_dir  = os.path.join(parent_dir, "test", "regression", test_name, "payload", payload_name)

    return payload_dir

@app.post("/total")
async def total(request_body: MainModel):
    payload_dir  = __get_payload_dir(request_body.data_id)
    
    if request_body.user == "":
        user = "user@gmail.com"
    else:
        user = request_body.user

    args = {
        'payload_dir' : payload_dir,
        'user' : user,
        'title' : request_body.title,
        'description' : request_body.description,
        'question': request_body.question
    }

    result_create_api = create_api_key(args)

    if result_create_api['status'] == 'success':
        print(result_create_api)

        args = {
            'payload_dir' : payload_dir,
            'user' : user,
            'title' : request_body.title,
            'description' : request_body.description,
            'question': request_body.question,
            "api_key": result_create_api['api_key']
        }

        result_finetuning = total_process(args)

        if result_finetuning['status'] == 'success':
            print(result_finetuning)

            result_chatting = chatting(args)
            print(result_chatting)

            return result_chatting
        else:
            print(result_finetuning)
            return result_finetuning
    else:
        print(result_create_api)
        return result_create_api


@app.post("/finetuning")
async def finetuning(request_body: BasicModel):
    payload_dir  = __get_payload_dir(request_body.data_id)

    if request_body.user == "":
        user = "user@gmail.com"
    else:
        user = request_body.user

    if request_body.api_key == "":
        api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA1"
    else:
        api_key = request_body.api_key

    args = {
        'payload_dir' : payload_dir,
        'user' : user,
        'api_key' : api_key
    }

    result = total_process(args)

    return result


@app.post("/create_api")
async def create_api(request_body: CreateAPIModel):
    payload_dir  = __get_payload_dir(request_body.data_id)
    
    if request_body.user == "":
        user = "user@gmail.com"
    else:
        user = request_body.user

    args = {
        'payload_dir' : payload_dir,
        'user' : user,
        'title' : request_body.title,
        'description' : request_body.description
    }

    result = create_api_key(args)

    return result


@app.post("/delete_api")
async def delete_api(request_body: BasicModel):
    payload_dir  = __get_payload_dir(request_body.data_id)
    
    if request_body.user == "":
        user = "user@gmail.com"
    else:
        user = request_body.user

    if request_body.api_key == "":
        api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA1"
    else:
        api_key = request_body.api_key

    args = {
        'payload_dir' : payload_dir,
        'user' : user,
        'api_key' : api_key
    }

    result = delete_api_key(args)

    return result


@app.post("/check_api")
async def check_api(request_body: BasicModel):
    payload_dir  = __get_payload_dir(request_body.data_id)
    
    if request_body.user == "":
        user = "user@gmail.com"
    else:
        user = request_body.user

    if request_body.api_key == "":
        api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA1"
    else:
        api_key = request_body.api_key

    args = {
        'payload_dir' : payload_dir,
        'user' : user,
        'api_key' : api_key
    }

    result = check_api_key(args)

    return result


@app.post("/conversation")
async def conversation(request_body: ChattingModel):
    payload_dir  = __get_payload_dir(request_body.data_id)
    
    if request_body.user == "":
        user = "user@gmail.com"
    else:
        user = request_body.user

    if request_body.api_key == "":
        api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA1"
    else:
        api_key = request_body.api_key

    args = {
        'payload_dir' : payload_dir,
        'user' : user,
        'api_key' : api_key,
        'question' : request_body.question
    }

    result = chatting(args)

    return result