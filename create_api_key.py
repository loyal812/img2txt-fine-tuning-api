
import os
import gc
import argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus

from src.utils.read_json import read_json
from src.mongodb.MongoDBClass import MongoDBClass
from src.utils.utils_funcs import generate_api_key
from src.models.api_model import APIModel

def create_api_key(args):
    """
    main entry point
    """

    # Payload
    payload_data = read_json(args.payload_dir)

    # Your MongoDB Atlas connection details
    mongodb_username = payload_data["mongodb_username"]
    mongodb_password = payload_data["mongodb_password"]
    mongodb_cluster_name = payload_data["mongodb_cluster_name"]
    mongodb_database_name = payload_data["mongodb_database_name"]

    # Escape the mongodb_username and mongodb_password
    mongodb_escaped_username = quote_plus(mongodb_username)
    mongodb_escaped_password = quote_plus(mongodb_password)

    # Construct the MongoDB Atlas URI
    mongo_uri = f"mongodb+srv://{mongodb_escaped_username}:{mongodb_escaped_password}@{mongodb_cluster_name}.mongodb.net/{mongodb_database_name}"

    # Call class instance
    mongodb = MongoDBClass(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=mongo_uri)
    
    api_key = generate_api_key()

    data:APIModel = {
        "user": str(Path(args.user)),
        "api": api_key,
        "title": str(Path(args.title)),
        "description": str(Path(args.description)),
        "is_removed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    mongodb.create_api(data)

    gc.collect()

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
    payload_name = "mongodb_payload.json"
    payload_dir  = os.path.join(current_dir, "test", "regression", test_name, "payload", payload_name)

    user = "user@gmail.com"
    title = "title"
    description = "description"

    # Add options
    p = argparse.ArgumentParser()
    p = argparse.ArgumentParser(description="Translate text within an image.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="payload directory to the test example")
    p.add_argument("--user", type=Path, default=user, help="user")
    p.add_argument("--title", type=Path, default=title, help="title")
    p.add_argument("--description", type=Path, default=description, help="title")
    args = p.parse_args()

    create_api_key(args)