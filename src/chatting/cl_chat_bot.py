import os
import logging
from typing import Optional
from dotenv import load_dotenv

import openai
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI

class ChatBot:
    def __init__(self, model_id, data_path, api_key="", temperature=0.3):
        """
        Initialize the ChatBot class.
        
        Args:
        - model_id (str): Identifier for the OpenAI fine tuned model ID.
        - data_path (str): Path to the input data directory.
        - api_key (str, optional): OpenAI API key. If not provided, it will be loaded from the environment variables.
        - temperature (float, optional): A parameter for controlling the randomness of the model's output.
        """
        self.model_id = model_id
        self.data_path = data_path
        self.temperature = temperature
        self.__set_api_key(api_key)
        self.__set_document(data_path)


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
                logging.error("OpenAI API key is not provided and not found in environment variables.")
                raise

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

    
    def ask_question(self, question: str) -> Optional[str]:
        """
        Query the OpenAI model with the given question.

        Args:
            question (str): The question to ask the model.

        Returns:
            Optional[str]: The model's response to the question, or None if an error occurs.
        """
        try:
            # Initialize the service context with the specified model and temperature
            ft_context = ServiceContext.from_defaults(
                llm=OpenAI(model=self.model_id, temperature=self.temperature),
                context_window=2048
            )

            # Create a vector store index from the documents
            # Ensure self.documents is a valid and initialized list of documents
            index = VectorStoreIndex.from_documents(self.documents, service_context=ft_context)
            
            # Create a query engine from the index
            query_engine = index.as_query_engine(service_context=ft_context)

            # Query the engine and return the response
            response = query_engine.query(question)
            return response

        except Exception as e:
            # Handle any exceptions that occur during the query
            logging.error(f"The response to the question is None because an error occurred during the query: {e}")
            return None