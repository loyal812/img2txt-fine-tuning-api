import os
import logging
import openai
import random
import time
import json
from itertools import cycle

from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
from llama_index.llms import OpenAI
from llama_index.evaluation import DatasetGenerator
from llama_index.callbacks import OpenAIFineTuningHandler
from llama_index.callbacks import CallbackManager

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness

from dotenv import load_dotenv

class FineTuning:
    def __init__(self, data_path, parent_path, api_key="", model='gpt-3.5-turbo', temperature=0.3, max_retries=5):
        """Initialize the FineTuning.

        Args:
        - data_path (str): The path to the data for fine-tuning.
        - parent_path (str): The parent directory path.
        - api_key (str, optional): OpenAI API key. If not provided, it will be loaded from the environment variables.
        - model (str, optional): The OpenAI model to use for fine-tuning.
        - temperature (float, optional): A parameter for controlling the randomness of the model's output.
        - max_retries (int, optional): The maximum number of retries for fine-tuning operations.
        """
        self.data_path = data_path
        self.parent_path = parent_path
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries
        self.retry_delay = 60
        self.__set_api_key(api_key)
        self.__set_document(data_path)
        self.__generate_subfolder(parent_path)

    def __set_api_key(self, api_key=None):
        """
        Set the OpenAI API key for authorization.

        Args:
        - api_key (str, optional): OpenAI API key. Default is None.
        """
        # If api_key is provided and not empty
        if api_key and api_key.strip():
            self.api_key = api_key
        else:
            # Load API key from environment variables
            load_dotenv()
            self.api_key = os.getenv("OPENAI_API_KEY")

            # If API key is not found in the environment variables, handle the situation
            if not self.api_key:
                # Here, you can log an error, raise an exception, or provide further instructions
                raise ValueError("OpenAI API key is not provided and not found in environment variables.")

        # Set the OpenAI API key in the environment and OpenAI library
        os.environ["OPENAI_API_KEY"] = self.api_key
        openai.api_key = self.api_key
        return True
    
    
    def __set_document(self, data_path):
        """
        Load documents from the specified data directory.

        Args:
        - data_path (str): Path to the input data directory.

        Raises:
        - FileNotFoundError: If the specified data path does not exist or is inaccessible.
        """
        try:
            self.documents = SimpleDirectoryReader(data_path).load_data()
        except FileNotFoundError as e:
            logging.error(f"The specified data path '{data_path}' does not exist or is inaccessible: {e}")
            raise
        except Exception as e:
            logging.error(f"An error occurred while loading data from '{data_path}': {e}")
            raise

    def __generate_subfolder(self, parent_path):
        """Generate a subfolder for storing generated data.

        Args:
        - parent_path (str): The parent directory path.
        """
        subfolder_name = "generated_data"
        subfolder_path = os.path.join(parent_path, subfolder_name)
        os.makedirs(subfolder_path, exist_ok=True)

    def train_generation(self):
        """
        Generate and save questions for training and evaluation.

        This method generates questions using the provided context and saves
        them to separate files for training and evaluation.

        Raises:
        - Exception: If an error occurs during question generation.
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                half_point = len(self.documents) // 2  # Get the index for the halfway point of the documents
                random.seed(42)
                random.shuffle(self.documents)

                # Initialize the OpenAI model and context
                gpt_35_context = ServiceContext.from_defaults(
                    llm=OpenAI(model=self.model, temperature=self.temperature)
                )

                # Define the query for question generation
                question_gen_query = (
                    "You are a Teacher/ Professor. Your task is to setup "
                    "a quiz/examination. Using the provided context, formulate "
                    "a single question that captures an important fact from the "
                    "context. Restrict the question to the context information provided."
                )

                def generate_and_save_questions(documents, output_file, num_questions):
                    """
                    Generate and save questions to a file.

                    Args:
                    - documents (list): List of documents for question generation.
                    - output_file (str): Output file path for saving the questions.
                    - num_questions (int): Number of questions to generate.
                    """
                    dataset_generator = DatasetGenerator.from_documents(
                        documents,
                        question_gen_query=question_gen_query,
                        service_context=gpt_35_context
                    )
                    questions = []
                    # Create an iterator that cycles through available documents
                    documents_cycle = cycle(documents)
                    
                    # Generate questions until reaching the desired count
                    while len(questions) < num_questions:
                        # Use the next document in the cycle
                        next_document = next(documents_cycle)
                        dataset_generator = dataset_generator.from_documents([next_document])
                        
                        # Generate questions from the updated dataset
                        new_questions = dataset_generator.generate_questions_from_nodes(num=num_questions - len(questions))
                        questions.extend(new_questions)
                        
                    print(f"Generated {len(questions)} questions")
                    
                    with open(output_file, "w", encoding='utf-8') as f:
                        for question in questions:
                            f.write(question + "\n")

                generate_and_save_questions(self.documents[:half_point], f'{self.parent_path}/generated_data/train_questions.txt', 40)
                generate_and_save_questions(self.documents[half_point:], f'{self.parent_path}/generated_data/eval_questions.txt', 40)

                break
            except Exception as e:
                print(f"Error in attempt {attempt}: {e}")
                time.sleep(self.retry_delay * attempt)
                
    def initial_eval(self):
        """Perform initial evaluation based on the generated questions and answers."""
        questions = []
        with open(f'{self.parent_path}/generated_data/eval_questions.txt', "r", encoding='utf-8') as f:
            for line in f:
                questions.append(line.strip())

        # limit the context window to 2048 tokens so that refine is used
        gpt_35_context = ServiceContext.from_defaults(
            llm=OpenAI(model=self.model, temperature=self.temperature), context_window=2048
        )

        index = VectorStoreIndex.from_documents(
            self.documents, service_context=gpt_35_context
        )

        # Perform query to retrieve the contexts and answers for the generated questions
        query_engine = index.as_query_engine(similarity_top_k=2)
        contexts = []
        answers = []

        for question in questions:
            response = query_engine.query(question)
            contexts.append([x.node.get_content() for x in response.source_nodes])
            answers.append(str(response))


        # Create a dataset from the questions, answers, and contexts
        ds = Dataset.from_dict(
            {
                "question": questions,
                "answer": answers,
                "contexts": contexts,
            }
        )

        # Evaluate the dataset using specific metrics and print the result
        result = evaluate(ds, [answer_relevancy, faithfulness])
        print(result)

    def jsonl_generation(self):
        """
        Generate JSONL file for fine-tuning events and perform model refinement.
        """
        # Initialize OpenAI FineTuningHandler and CallbackManager
        finetuning_handler = OpenAIFineTuningHandler()
        callback_manager = CallbackManager([finetuning_handler])

        # Create a ServiceContext for the GPT-4 model with refined context window
        gpt_4_context = ServiceContext.from_defaults(
            llm=OpenAI(model="gpt-4", temperature=self.temperature),
            context_window=2048,  # limit the context window artifically to test refine process
            callback_manager=callback_manager,
        )

        # Load questions for fine-tuning from a file
        questions = []
        with open(f'{self.parent_path}/generated_data/train_questions.txt', "r", encoding='utf-8') as f:
            for line in f:
                questions.append(line.strip())

        try:
            # Generate responses to the questions using GPT-4 and save the fine-tuning events to a JSONL file
            index = VectorStoreIndex.from_documents(
                self.documents, service_context=gpt_4_context
            )
            query_engine = index.as_query_engine(similarity_top_k=2)
            for question in questions:
                response = query_engine.query(question)
        except Exception as e:
            # Handle the exception here, you might want to log the error or take appropriate action
            print(f"An error occurred: {e}")
        finally:
            # Save the fine-tuning events to a JSONL file
            finetuning_handler.save_finetuning_events(f'{self.parent_path}/generated_data/finetuning_events.jsonl')

        
    def finetune(self):
        """
        Initiate the fine-tuning process and update model information.
        """
        # Create a file upload for the fine-tuning events JSONL file
        # new version openai >= 1.1.0
        file_upload = openai.files.create(file=open(f'{self.parent_path}/generated_data/finetuning_events.jsonl', "rb"), purpose="fine-tune")
        print("Uploaded file id", file_upload.id)

        # Wait for the file to be processed before initiating fine-tuning
        while True:
            print("Waiting for file to process...")
            file_handle = openai.files.retrieve(file_id=file_upload.id)
            if file_handle and file_handle.status == "processed":
                print("File processed")
                break
            time.sleep(3)

        try:
            # Initiate the fine-tuning job and monitor the process until completion
            job = openai.fine_tuning.jobs.create(training_file=file_upload.id, model=self.model)

            while True:
                print("Waiting for fine-tuning to complete...")
                job_handle = openai.fine_tuning.jobs.retrieve(fine_tuning_job_id=job.id)
                print(f"status: {job_handle.status}")
                if job_handle.status == "succeeded":
                    print("Fine-tuning complete")
                    print("Fine-tuned model info", job_handle)
                    print("Model id", job_handle.fine_tuned_model)

                    with open(f'{self.parent_path}/generated_data/model.txt', "w", encoding='utf-8') as f:
                        f.write(job_handle.fine_tuned_model + "\n")
                    
                    # Load the JSON data from the file
                    with open(f'{self.parent_path}/payload/chatting_payload.json', 'r', encoding='utf-8') as file:
                        payload = json.load(file)

                    # Update the model_id with specific data
                    payload['model_id'] = job_handle.fine_tuned_model

                    # Write the updated JSON back to the file
                    with open(f'{self.parent_path}/payload/chatting_payload.json', 'w', encoding='utf-8') as file:
                        json.dump(payload, file, indent=4)

                    # Load the JSON data from the file
                    with open(f'{self.parent_path}/payload/payload.json', 'r', encoding='utf-8') as file:
                        payload = json.load(file)

                    # Update the model_id with specific data
                    payload['model_id'] = job_handle.fine_tuned_model

                    # Write the updated JSON back to the file
                    with open(f'{self.parent_path}/payload/payload.json', 'w', encoding='utf-8') as file:
                        json.dump(payload, file, indent=4)

                    return job_handle.fine_tuned_model
                time.sleep(3)
        except Exception as e:
            print(f"An error occurred during fine-tuning: {e}")

        # # old version openai < 1.1.0
        # file_upload = openai.File.create(file=open(f'{self.data_path}/generated_data/finetuning_events.jsonl', "rb"), purpose="fine-tune")
        # print("Uploaded file id", file_upload.id)

        # while True:
        #     print("Waiting for file to process...")
        #     file_handle = openai.File.retrieve(id=file_upload.id)
        #     if file_handle and file_handle.status == "processed":
        #         print("File processed")
        #         break
        #     time.sleep(3)

        # try:
        #     job = openai.FineTuningJob.create(training_file=file_upload.id, model=self.model)

        #     while True:
        #         print("Waiting for fine-tuning to complete...")
        #         job_handle = openai.FineTuningJob.retrieve(id=job.id)
        #         if job_handle.status == "succeeded":
        #             print("Fine-tuning complete")
        #             print("Fine-tuned model info", job_handle)
        #             print("Model id", job_handle.fine_tuned_model)

        #             with open(f'{self.data_path}/generated_data/model.txt', "w", encoding='utf-8') as f:
        #                 f.write(job_handle.fine_tuned_model + "\n")
                    
        #             # Load the JSON data from the file
        #             with open(f'{self.data_path}/payload/chatting_payload.json', 'r', encoding='utf-8') as file:
        #                 payload = json.load(file)

        #             # Update the model_id with specific data
        #             payload['model_id'] = job_handle.fine_tuned_model

        #             # Write the updated JSON back to the file
        #             with open(f'{self.data_path}/payload/chatting_payload.json', 'w', encoding='utf-8') as file:
        #                 json.dump(payload, file, indent=4)

        #             return job_handle.fine_tuned_model
        #         time.sleep(3)
        # except Exception as e:
        #     print(f"An error occurred during fine-tuning: {e}")