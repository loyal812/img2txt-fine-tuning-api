import gc
import argparse

from send_request import send_request

def chatting(args):
    """
    main entry point
    """

    data = {
        "api_key": str(args.api_key),
        "user": str(args.user),
        "data_id": str(args.data_id),
        "question": str(args.question)
    }

    result = send_request(args.api_url, data)

    gc.collect()

    print(result)

if __name__ == "__main__":
    """
    Form command lines
    """
    # Clean up buffer memory
    gc.collect()

    user = "user@gmail.com"
    api_key = "AMEYbpdcmrUxNu_Fb80qutukUZdlsmYiH4g7As5LzNA"
    data_id = ""
    api_url = "http://localhost:8000/conversation"
    question = "hi"

    # Add options
    p = argparse.ArgumentParser()
    p = argparse.ArgumentParser(description="Translate text within an image.")
    p.add_argument("--api_url", type=str, default=api_url, help="URL to send the POST request to")
    p.add_argument("--data_id", type=str, default=data_id, help="payload directory to the test example")
    p.add_argument("--user", type=str, default=user, help="user")
    p.add_argument("--question", type=str, default=question, help="user's question")
    p.add_argument("--api_key", type=str, default=api_key, help="api key")
    args = p.parse_args()


    chatting(args)
