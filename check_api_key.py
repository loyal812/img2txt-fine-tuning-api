
import os
import gc
import argparse
from pathlib import Path

from src.utils.read_json import read_json
from src.mongodb.MongoDBClass import MongoDBClass


def check_api_key(args):
    """
    main entry point
    """

    # Payload
    payload_data = read_json(args.payload_dir)

    # Construct the MongoDB Atlas URI
    mongo_uri = payload_data["mongo_uri"]

    # Call class instance
    mongodb = MongoDBClass(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=mongo_uri)

    mongodb.check_validation_api(api_key=str(Path(args.api_key)), user=str(Path(args.user)))

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
    api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA"

    # Add options
    p = argparse.ArgumentParser()
    p = argparse.ArgumentParser(description="Translate text within an image.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="payload directory to the test example")
    p.add_argument("--user", type=Path, default=user, help="user")
    p.add_argument("--api_key", type=Path, default=api_key, help="title")
    args = p.parse_args()

    check_api_key(args)