from llama_index import ServiceContext, SimpleDirectoryReader
from llama_index.llms import OpenAI
from llama_index.callbacks import OpenAIFineTuningHandler
from llama_index.callbacks import CallbackManager
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

# Define the path to the data directory
data_path = "./test/regression/regression_test003"

# Load documents from the data directory
documents = SimpleDirectoryReader(
    data_path
).load_data()

# Initialize the OpenAIFineTuningHandler and CallbackManager
finetuning_handler = OpenAIFineTuningHandler()
callback_manager = CallbackManager([finetuning_handler])

# Create a ServiceContext for GPT-4 model with a limited context window and callback manager
gpt_4_context = ServiceContext.from_defaults(
    llm=OpenAI(model="gpt-4", temperature=0.3),
    context_window=2048,  # limit the context window artifically to test refine process
    callback_manager=callback_manager,
)

# Load training questions from a file
questions = []
with open(f'{data_path}/generated_data/train_questions.txt', "r") as f:
    for line in f:
        questions.append(line.strip())

from llama_index import VectorStoreIndex

try:
    # Create a VectorStoreIndex with the provided documents and service context
    index = VectorStoreIndex.from_documents(
        documents, service_context=gpt_4_context
    )

    # Create a query engine for the index with a specified top-k similarity threshold
    query_engine = index.as_query_engine(similarity_top_k=2)

    # Query the index for each training question to initiate fine-tuning
    for question in questions:
        response = query_engine.query(question)

# Handle any occurring exceptions
except Exception as e:
    # Handle the exception here, you might want to log the error or take appropriate action
    print(f"An error occurred: {e}")

# Finally, save the fine-tuning events to a JSONL file
finally:
    finetuning_handler.save_finetuning_events(f'{data_path}/generated_data/finetuning_events.jsonl')
