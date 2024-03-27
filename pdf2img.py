
import os
import gc
import argparse
from pathlib import Path

from src.utils.read_json import read_json
from src.pdf2img.Pdf2ImgClass import Pdf2ImgClass

def pdf2img(args):
    """
    main entry point
    """

    # Payload
    payload_data = read_json(args.payload_dir)

    # Call class instance
    pdf2img = Pdf2ImgClass(
        data_path=payload_data["pdf_data_path"],
        parent_path=payload_data["data_path"])
    
    pdf2img.pdf2img()

    gc.collect()

if __name__ == "__main__":
    # Clean up buffer memory before starting the program
    gc.collect()

    # Default values for command line arguments
    # Current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Payload directory
    test_name    = "regression_test013"
    payload_name = "pdf2img_payload.json"
    payload_dir  = os.path.join(current_dir, "test", "regression", test_name, "payload", payload_name)

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="PDF to Image.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="Data directory")
    args = p.parse_args()

    pdf2img(args)