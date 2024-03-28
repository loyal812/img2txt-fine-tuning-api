import gc
from pathlib import Path

from src.utils.read_json import read_json
from src.chatting.cl_chat_bot import ChatBot
from src.api_access.cl_api_access import ApiAccess

def chatting(args):
    """
    Main entry point for the chatting functionality
    Args:
    - args (dict): The input arguments for the chatting process
    """

    # Load payload data from a JSON file
    payload_data = read_json(args['payload_dir'])

    # Extract MongoDB URI from payload data
    mongo_uri = payload_data["mongo_uri"]

    # Create an instance of MongoDB connection
    apiAccess = ApiAccess(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=mongo_uri)

    # Check if the API key is valid using MongoDB
    is_available = apiAccess.check_validation_api(api_key=str(Path(args['api_key'])), user=str(Path(args['user'])))

    if is_available:
        print("valid api key")
        # Create an instance of ChatBot
        chatting = ChatBot(
            data_path=payload_data["data_path"],
            api_key=payload_data["api_key"],
            model_id=payload_data["model_id"],
            temperature=payload_data["temperature"])

        # Ask a question using the ChatBot instance   
        response = chatting.ask_question(args['question'])
        print(response)
    
        # Perform garbage collection to free up memory
        gc.collect()
        
        # Return the result
        return {"status": "success", "api_key": args["api_key"], "response": response.response}
    else:
        print("invalide api key")

        # Perform garbage collection to free up memory
        gc.collect()

        # Return response for invalid API key
        return {"status": "success", "fine_tuned_model": "invalide api key"}