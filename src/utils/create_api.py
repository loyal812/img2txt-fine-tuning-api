
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
    payload_data = read_json(args['payload_dir'])

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
        "user": str(Path(args['user'])),
        "api": api_key,
        "title": str(Path(args['title'])),
        "description": str(Path(args['description'])),
        "is_removed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    mongodb.create_api(data)

    gc.collect()
