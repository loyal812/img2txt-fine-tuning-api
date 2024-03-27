import gc
import argparse

from send_request import send_request

def total_process(args):
    """
    Posts data to a specified API URL and prints the result
    Args:
        args: Command line arguments
    """
    # Prepare the data to be sent in the request
    data = {
        "user": str(args.user),
        "title": str(args.title),
        "description": str(args.description),
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
    title = "title"
    description = "description"
    data_id = ""
    api_url = "http://localhost:5000/total"
    question = "hi"

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="Total Process: Create API key, Fine Tuning, Chatting.")
    p.add_argument("--api_url", type=str, default=api_url, help="URL to send the POST request to")
    p.add_argument("--data_id", type=str, default=data_id, help="Data directory")
    p.add_argument("--user", type=str, default=user, help="User Email")
    p.add_argument("--title", type=str, default=title, help="Title")
    p.add_argument("--description", type=str, default=description, help="Description")
    p.add_argument("--question", type=str, default=question, help="User's question")
    args = p.parse_args()

    # Call the total_process function with the parsed arguments
    total_process(args)