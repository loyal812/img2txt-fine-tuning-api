
import os
import gc
import argparse
from pathlib import Path
from datetime import datetime

from src.utils.read_json import read_json
from src.mongodb.MongoDBClass import MongoDBClass
from src.utils.utils_funcs import generate_api_key
from src.models.api_model import APIModel

def create_api_key(args):
    """
    Main function to create an API key and store it in a MongoDB database.
    
    Args:
    - args (argparse.Namespace): Parsed command-line arguments
    """

    # Load payload data from a JSON file
    payload_data = read_json(args.payload_dir)

    # Extract MongoDB URI from payload data
    mongo_uri = payload_data["mongo_uri"]

    # Create an instance of MongoDBClass to interact with the database
    mongodb = MongoDBClass(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=mongo_uri)
    
    # Generate a new API key
    api_key = generate_api_key()

    # Prepare the data for the new API using APIModel
    data:APIModel = {
        "user": str(Path(args.user)),
        "api": api_key,
        "title": str(Path(args.title)),
        "description": str(Path(args.description)),
        "is_removed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    # Store the API key data in the MongoDB database
    mongodb.create_api(data)

    # Perform garbage collection to free up memory
    gc.collect()

if __name__ == "__main__":
    # Clean up buffer memory before starting the program
    gc.collect()

    # Default values for command line arguments
    # Current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Payload directory
    test_name    = "regression_test013"
    payload_name = "mongodb_payload.json"
    payload_dir  = os.path.join(current_dir, "test", "regression", test_name, "payload", payload_name)

    user = "user@gmail.com"
    title = "title"
    description = "description"

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="Create API key.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="Data directory")
    p.add_argument("--user", type=Path, default=user, help="User Email")
    p.add_argument("--title", type=Path, default=title, help="Title")
    p.add_argument("--description", type=Path, default=description, help="Description")
    args = p.parse_args()

    # Call the create_api_key function with the parsed arguments
    create_api_key(args)