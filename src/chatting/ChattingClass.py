import openai
import os
import argparse
from dotenv import load_dotenv
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI

class ChattingClass:
    def __init__(self, model_id, data_path, api_key="", temperature=0.3):
        self.model_id = model_id
        self.data_path = data_path
        self.temperature = temperature
        self.set_api_key(api_key)
        self.set_document(data_path)

    def set_api_key(self, api_key):
        if api_key:
            self.api_key = api_key
        else:
            load_dotenv()
            self.api_key = os.getenv("OPENAI_API_KEY")

        if self.api_key is not None:
            os.environ["OPENAI_API_KEY"] = self.api_key
            openai.api_key = self.api_key
            return True
        else:
            # Handle the absence of the environment variable
            # You might want to log an error, raise an exception, or provide a default value
            # For example, setting a default value
            os.environ["OPENAI_API_KEY"] = "your_default_api_key"
            openai.api_key = "openai_api_key"
            return False

    def set_document(self, data_path):
        self.documents = SimpleDirectoryReader(
            data_path
        ).load_data()

    def ask_question(self, question):
        ft_context = ServiceContext.from_defaults(
            llm=OpenAI(model=self.model_id, temperature=self.temperature),
            context_window=2048
        )

        index = VectorStoreIndex.from_documents(self.documents, service_context=ft_context)
        query_engine = index.as_query_engine(service_context=ft_context)

        response = query_engine.query(question)
        return response

# Using argparse to get the question input from the user
parser = argparse.ArgumentParser(description='Chatting Engine')
# parser.add_argument('api_key', type=str, help='Openai API Key')
parser.add_argument('data_path', type=str, help='Data Path')
parser.add_argument('model_id', type=str, help='model')
parser.add_argument('question', type=str, help='question')
# parser.add_argument('temperature', type=str, help='temperature')
args = parser.parse_args()

# model_id = 'ft:gpt-3.5-turbo-0613:personal::8XaasBXv'
# data_path = "./src/test/regression/regression_test003"
chatbot = ChattingClass(model_id=args.model_id, data_path=args.data_path)

response = chatbot.ask_question(args.question)
print(response)