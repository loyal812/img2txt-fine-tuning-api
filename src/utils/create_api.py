import gc
from pathlib import Path
from datetime import datetime

from src.utils.read_json import read_json
from src.mongodb.cl_mongodb import MongoDB
from src.utils.utils_funcs import generate_api_key
from src.models.api_model import APIModel

def create_api_key(args):
    """
    Function to create an API key and store it in a MongoDB database.
    Args:
    - args (dict): The input arguments containing the payload directory, user, title, and description
    """

    # Load payload data from a JSON file
    payload_data = read_json(args['payload_dir'])

    # Extract MongoDB URI from payload data
    mongo_uri = payload_data["mongo_uri"]

    # Create an instance of MongoDB connection
    mongodb = MongoDB(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=mongo_uri)
    
    # Generate a new API key
    api_key = generate_api_key()

    # Prepare the data for the new API key using the specified model
    data:APIModel = {
        "user": str(Path(args['user'])),
        "api": api_key,
        "title": str(Path(args['title'])),
        "description": str(Path(args['description'])),
        "is_removed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    # Create the API key in the MongoDB database
    result = mongodb.create_api(data)

    # Perform garbage collection to free up memory
    gc.collect()

    return result
