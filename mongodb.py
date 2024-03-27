
import os
import gc
import argparse
from pathlib import Path

from src.utils.read_json import read_json
from src.mongodb.MongoDBClass import MongoDBClass

def mongodb(args):
    """
    main entry point
    """

    # Payload
    payload_data = read_json(args.payload_dir)

    # Call class instance
    mongodb = MongoDBClass(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=payload_data["mongo_uri"])
    
    mongodb.mongo_connect()

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

    # Add options
    p = argparse.ArgumentParser()
    p = argparse.ArgumentParser(description="Translate text within an image.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="payload directory to the test example")
    args = p.parse_args()

    mongodb(args)