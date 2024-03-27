import gc
import argparse

from send_request import send_request

def chatting(args):
    """
    Main entry point for the chat application
    Args:
        args: Command line arguments
    """
    # Prepare the data to be sent in the request
    data = {
        "api_key": str(args.api_key),
        "user": str(args.user),
        "data_id": str(args.data_id),
        "question": str(args.question)
    }

    # Send the request and get the result
    result = send_request(args.api_url, data)

    # Clean up and free memory
    gc.collect()

    # Print the result
    print(result)

if __name__ == "__main__":
    # Clean up buffer memory before starting the program
    gc.collect()

    # Default values for command line arguments
    user = "user@gmail.com"
    api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA"
    data_id = ""
    api_url = "http://localhost:8000/conversation"
    question = "hi"

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="Chatting")
    p.add_argument("--api_url", type=str, default=api_url, help="URL to send the POST request to")
    p.add_argument("--data_id", type=str, default=data_id, help="Data directory")
    p.add_argument("--user", type=str, default=user, help="User Email")
    p.add_argument("--question", type=str, default=question, help="User's question")
    p.add_argument("--api_key", type=str, default=api_key, help="API key")
    args = p.parse_args()

    # Call the chatting function with the parsed arguments
    chatting(args)
