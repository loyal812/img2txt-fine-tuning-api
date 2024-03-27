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

from src.models.main_model import MainModel


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


# Define a route to handle the root endpoint and redirect to the API documentation
@app.get("/")
async def root():
    return RedirectResponse(app.docs_url)


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

    total_process(args)
