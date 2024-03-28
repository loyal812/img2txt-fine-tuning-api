import os
import gc
import argparse
from pathlib import Path

from src.utils.read_json import read_json
from chatting.cl_chat_bot import ChatBot
from src.mongodb.MongoDBClass import MongoDBClass

def chatting(args):
    """
    Main entry point for the chatting process
    Args:
        args: Command line arguments
    """

    # Load payload data from the provided directory
    payload_data = read_json(args.payload_dir)

    # Extract MongoDB URI from payload data
    mongo_uri = payload_data["mongo_uri"]

    # Create an instance of MongoDBClass for database operations
    mongodb = MongoDBClass(
        db_name=payload_data["db_name"], 
        collection_name=payload_data["collection_name"], 
        mongo_uri=mongo_uri)

    # Check if the API key is valid using MongoDB
    is_available = mongodb.check_validation_api(api_key=str(Path(args.api_key)), user=str(Path(args.user)))

    if is_available:
        print("valid api key")
        # Initialize the ChatBot instance for conversation
        chatting = ChatBot(
            data_path=payload_data["data_path"],
            api_key=payload_data["api_key"],
            model_id=payload_data["model_id"],
            temperature=payload_data["temperature"])

        # Ask a question using the ChatBot instance and get the response  
        response = chatting.ask_question(args.question)
        print(response)
    else:
        print("invalide api key")

    gc.collect()

if __name__ == "__main__":
    # Clean up buffer memory before starting the program
    gc.collect()

    # Default values for command line arguments
    # Current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Payload directory
    test_name    = "regression_test003"
    payload_name = "chatting_payload.json"
    payload_dir  = os.path.join(current_dir, "test", "regression", test_name, "payload", payload_name)

    user = "user@gmail.com"
    api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA1"

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="Conversational Agent.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="Data directory")
    p.add_argument("--question", type=str)
    p.add_argument("--user", type=Path, default=user, help="User Email")
    p.add_argument("--api_key", type=Path, default=api_key, help="API key")
    args = p.parse_args()

    # Call the chatting function with the parsed arguments
    chatting(args)