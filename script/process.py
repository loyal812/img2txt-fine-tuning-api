import gc
import argparse

from send_request import send_request

def create_api_key(args):
    """
    Function to create a new API key
    Args:
        args: Command line arguments
    """
    # Prepare the data to be sent in the request
    data = {
        "user": str(args.user),
        "title": str(args.title),
        "description": str(args.description),
        "data_id": str(args.data_id)
    }

    url = f'{args.api_url}/create_api'

    # Send the request and get the result
    result = send_request(url, data)

    # Clean up and free memory
    gc.collect()

    # Print the result
    print(result)

def delete_api_key(args):
    """
    Function to delete an API key
    Args:
        args: Command line arguments
    """
    # Prepare the data to be sent in the request
    data = {
        "api_key": str(args.api_key),
        "user": str(args.user),
        "data_id": str(args.data_id)
    }

    url = f'{args.api_url}/delete_api'
    # Send the request and get the result
    result = send_request(url, data)

    # Clean up and free memory
    gc.collect()

    # Print the result
    print(result)

def check_api_key(args):
    """
    Function to check the validity of an API key
    Args:
        args: Command line arguments
    """
    # Prepare the data to be sent in the request
    data = {
        "api_key": str(args.api_key),
        "user": str(args.user),
        "data_id": str(args.data_id)
    }

    url = f'{args.api_url}/check_api'
    # Send the request and get the result
    result = send_request(url, data)

    # Clean up and free memory
    gc.collect()

    # Print the result
    print(result)

def run_fine_tuning(args):
    """
    Function to initiate fine-tuning of a model
    Args:
        args: Command line arguments
    """
    # Prepare the data to be sent in the request
    data = {
        "api_key": str(args.api_key),
        "user": str(args.user),
        "data_id": str(args.data_id)
    }

    url = f'{args.api_url}/finetuning'
    # Send the request and get the result
    result = send_request(url, data)

    # Clean up and free memory
    gc.collect()

    # Print the result
    print(result)

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

    url = f'{args.api_url}/conversation'
    # Send the request and get the result
    result = send_request(url, data)

    # Clean up and free memory
    gc.collect()

    # Print the result
    print(result)

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

    url = f'{args.api_url}/total'
    # Send the request and get the result
    result = send_request(url, data)

    # Clean up and free memory
    gc.collect()

    # Print the result
    print(result)

if __name__ == "__main__":
    # Clean up buffer memory before starting the program
    gc.collect()

    # Default values for command line arguments
    step = "create_api"
    user = "user@gmail.com"
    title = "title"
    description = "description"
    data_id = ""
    api_url = "http://localhost:8000"
    api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA"
    question = 'hi'

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="Oridos AI Process.")
    p.add_argument("--step", type=str, default=step, help="Select the process step.")
    p.add_argument("--api_url", type=str, default=api_url, help="URL to send the POST request to")
    p.add_argument("--data_id", type=str, default=data_id, help="Data directory")
    p.add_argument("--user", type=str, default=user, help="User Email")
    p.add_argument("--title", type=str, default=title, help="Title")
    p.add_argument("--description", type=str, default=description, help="Description")
    p.add_argument("--api_key", type=str, default=api_key, help="API key")
    p.add_argument("--question", type=str, default=question, help="User's question")
    args = p.parse_args()

    if args.step == "create_api":
        # Call the create_api_key function with the parsed arguments
        create_api_key(args)
    elif args.step == "delete_api":
        # Call the delete_api_key function with the parsed arguments
        delete_api_key(args)
    elif args.step == "check_api":
        # Call the check_api_key function with the parsed arguments
        check_api_key(args)
    elif args.step == "finetuning":
        # Call the run_fine_tuning function with the parsed arguments
        run_fine_tuning(args)
    elif args.step == "chatting":
        # Call the chatting function with the parsed arguments
        chatting(args)
    elif args.step == "all":
        # Call the total_process function with the parsed arguments
        total_process(args)
    else:
        print("The API doesn't exist!!!")
        