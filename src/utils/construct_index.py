from llama_index import SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper
# from llama_index import VectorStoreIndex, SimpleDirectoryReader
from langchain.llms import OpenAI
import sys
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is not None:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    # Handle the absence of the environment variable
    # You might want to log an error, raise an exception, or provide a default value
    # For example, setting a default value
    os.environ["OPENAI_API_KEY"] = "your_default_api_key"
    
def construct_index(file_path):
    # documents = SimpleDirectoryReader(file_path).load_data()
    # index = VectorStoreIndex.from_documents(documents)
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(file_path).load_data()

    index = GPTVectorStoreIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('aaaaaaa-index.json')

    return index