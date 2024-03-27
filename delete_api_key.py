
import os
import gc
import argparse
from pathlib import Path

from src.utils.read_json import read_json
from src.mongodb.MongoDBClass import MongoDBClass

def delete_api_key(args):
    """
    Main function to delete an API key from the MongoDB database collection.

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

    # Delete the API key identified by the user and the API key value
    mongodb.delete_api(api_key=str(Path(args.api_key)), user=str(Path(args.user)))

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
    api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA"

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="Delete API key.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="Data directory")
    p.add_argument("--user", type=Path, default=user, help="User Email")
    p.add_argument("--api_key", type=Path, default=api_key, help="API key")
    args = p.parse_args()

    delete_api_key(args)