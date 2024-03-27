import gc
from pathlib import Path
from datetime import datetime

from src.utils.read_json import read_json
from src.mongodb.MongoDBClass import MongoDBClass
from src.utils.utils_funcs import generate_api_key
from src.models.api_model import APIModel

def create_api_key(args):
    """
    main entry point
    """

    # Payload
    payload_data = read_json(args['payload_dir'])

    # Construct the MongoDB Atlas URI
    mongo_uri = payload_data["mongo_uri"]

    # Call class instance
    mongodb = MongoDBClass(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=mongo_uri)
    
    api_key = generate_api_key()

    data:APIModel = {
        "user": str(Path(args['user'])),
        "api": api_key,
        "title": str(Path(args['title'])),
        "description": str(Path(args['description'])),
        "is_removed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    result = mongodb.create_api(data)

    gc.collect()

    return result
