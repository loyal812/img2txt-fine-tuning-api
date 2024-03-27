import gc
from pathlib import Path
from urllib.parse import quote_plus

from src.utils.read_json import read_json
from src.chatting.ChattingClass import ChattingClass
from src.mongodb.MongoDBClass import MongoDBClass

def chatting(args):
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

    is_available = mongodb.check_validation_api(api_key=str(Path(args['api_key'])), user=str(Path(args['user'])))

    if is_available:
        print("valid api key")
        # Call class instance
        chatting = ChattingClass(
            data_path=payload_data["data_path"],
            api_key=payload_data["api_key"],
            model_id=payload_data["model_id"],
            temperature=payload_data["temperature"])
            
        response = chatting.ask_question(args['question'])
        print(response)
    else:
        print("invalide api key")

    gc.collect()