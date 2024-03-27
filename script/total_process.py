import gc
import argparse

from send_request import send_request

def total_process(args):
    """
    main entry point
    """

    data = {
        "user": str(args.user),
        "title": str(args.title),
        "description": str(args.description),
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
    title = "title"
    description = "description"
    data_id = ""
    api_url = "http://localhost:5000/total"
    question = "hi"

    # Add options
    p = argparse.ArgumentParser()
    p = argparse.ArgumentParser(description="Translate text within an image.")
    p.add_argument("--api_url", type=str, default=api_url, help="URL to send the POST request to")
    p.add_argument("--data_id", type=str, default=data_id, help="payload directory to the test example")
    p.add_argument("--user", type=str, default=user, help="user")
    p.add_argument("--title", type=str, default=title, help="title")
    p.add_argument("--description", type=str, default=description, help="title")
    p.add_argument("--question", type=str, default=question, help="user's question")
    args = p.parse_args()

    total_process(args)