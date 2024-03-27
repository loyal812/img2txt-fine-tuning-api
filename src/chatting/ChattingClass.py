import openai
import os
from dotenv import load_dotenv
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI

class ChattingClass:
    def __init__(self, model_id, data_path, api_key="", temperature=0.3):
        """
        Initialize the ChattingClass.
        
        Args:
        - model_id (str): Identifier for the OpenAI model.
        - data_path (str): Path to the data directory.
        - api_key (str, optional): OpenAI API key. If not provided, it will be loaded from the environment variables.
        - temperature (float, optional): A parameter for controlling the randomness of the model's output.
        """
        self.model_id = model_id
        self.data_path = data_path
        self.temperature = temperature
        self.set_api_key(api_key)
        self.set_document(data_path)

    def set_api_key(self, api_key):
        """
        Set the OpenAI API key for authorization.

        Args:
        - api_key (str): OpenAI API key.
        """
        if api_key:
            self.api_key = api_key
        else:
            # Load API key from environment variables using dotenv
            load_dotenv()
            self.api_key = os.getenv("OPENAI_API_KEY")

        # Set the OpenAI API key in the environment and OpenAI library
        if self.api_key is not None:
            os.environ["OPENAI_API_KEY"] = self.api_key
            openai.api_key = self.api_key
            return True
        else:
            # In case the API key is not available, handle the situation 
            # This could involve logging an error, raising an exception, or providing a default value
            os.environ["OPENAI_API_KEY"] = "your_default_api_key"
            openai.api_key = "openai_api_key"
            return False

    def set_document(self, data_path):
        """
        Load documents from the specified data directory.

        Args:
        - data_path (str): Path to the data directory.
        """
        self.documents = SimpleDirectoryReader(
            data_path
        ).load_data()

    def ask_question(self, question):
        """
        Query the OpenAI model with the given question.

        Args:
        - question (str): The question to ask the model.

        Returns:
        - response (str): The model's response to the question.
        """
        ft_context = ServiceContext.from_defaults(
            llm=OpenAI(model=self.model_id, temperature=self.temperature),
            context_window=2048
        )

        index = VectorStoreIndex.from_documents(self.documents, service_context=ft_context)
        query_engine = index.as_query_engine(service_context=ft_context)

        response = query_engine.query(question)
        return response
