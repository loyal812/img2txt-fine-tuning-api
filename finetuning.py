import os
import gc
import argparse
from pathlib import Path

from src.utils.read_json import read_json
from src.finetune.FineTuningClass import FineTuningClass

def run_fine_tuning(args):
    """
    Main function to execute the fine-tuning process using the provided payload.

    Args:
    - args (argparse.Namespace): Parsed command-line arguments
    """

    # Load payload data from a JSON file
    payload_data = read_json(args.payload_dir)
    
    # Create an instance of FineTuningClass to handle the fine-tuning process
    fine_tune = FineTuningClass(
        data_path=payload_data["data_path"],
        parent_path=payload_data["parent_path"],
        api_key=payload_data["api_key"],
        model=payload_data["model"],
        temperature=payload_data["temperature"],
        max_retries=payload_data["max_retries"])
    
    # Generate the train and eval data
    fine_tune.train_generation()

    # Generate the jsonl
    fine_tune.jsonl_generation()

    # Fine tuning
    fine_tune.finetune()

    # Perform garbage collection to free up memory
    gc.collect()

if __name__ == "__main__":
    # Clean up buffer memory before starting the program
    gc.collect()

    # Default values for command line arguments
    # Current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Payload directory
    test_name    = "regression_test003"
    payload_name = "finetuning_payload.json"
    payload_dir  = os.path.join(current_dir, "test", "regression", test_name, "payload", payload_name)

    # Set up command line argument parser
    p = argparse.ArgumentParser(description="Fine tuning.")
    p.add_argument("--payload_dir", type=Path, default=payload_dir, help="Data directory")
    args = p.parse_args()

    # Call the run_fine_tuning function with the parsed arguments
    run_fine_tuning(args)
