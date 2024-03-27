import gc
import argparse

from send_request import send_request

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
    api_url = "http://localhost:8000/finetuning"

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="Fine-Tuning a model.")
    p.add_argument("--api_url", type=str, default=api_url, help="URL to send the POST request to")
    p.add_argument("--data_id", type=str, default=data_id, help="Data directory")
    p.add_argument("--user", type=str, default=user, help="User Email")
    p.add_argument("--api_key", type=str, default=api_key, help="API key")
    args = p.parse_args()

    # Call the run_fine_tuning function with the parsed arguments
    run_fine_tuning(args)
