import gc
from pathlib import Path

from src.utils.read_json import read_json
from src.mongodb.cl_mongodb import MongoDB


def check_api_key(args):
    """
    Function to check the validity of the API key by querying a MongoDB database.
    Args:
    - args (dict): The input arguments containing the payload directory, API key, and user
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

    # Check the validation of the API key using MongoDB
    result = mongodb.check_validation_api(api_key=str(Path(args['api_key'])), user=str(Path(args['user'])))

    # Perform garbage collection to free up memory
    gc.collect()

    return result