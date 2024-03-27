import gc
from pathlib import Path

from src.utils.read_json import read_json
from src.mongodb.MongoDBClass import MongoDBClass

def delete_api_key(args):
    """
    Function to delete an API key from a MongoDB database.
    Args:
    - args (dict): The input arguments containing the payload directory, API key, and user
    """

    # Load payload data from a JSON file
    payload_data = read_json(args['payload_dir'])

    # Extract MongoDB URI from payload data
    mongo_uri = payload_data["mongo_uri"]

    # Create an instance of MongoDB connection
    mongodb = MongoDBClass(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=mongo_uri)

    # Delete the API key from the MongoDB database
    result = mongodb.delete_api(api_key=str(Path(args['api_key'])), user=str(Path(args['user'])))

    # Perform garbage collection to free up memory
    gc.collect()

    return result