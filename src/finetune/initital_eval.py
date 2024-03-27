from llama_index import VectorStoreIndex, ServiceContext, SimpleDirectoryReader
from llama_index.llms import OpenAI

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

data_path = "./test/regression/regression_test003"

# Set the path to the data directory
documents = SimpleDirectoryReader(
    data_path
).load_data()

# Load questions for evaluation from a file
questions = []
with open(f'{data_path}/generated_data/eval_questions.txt', "r") as f:
    for line in f:
        questions.append(line.strip())

# limit the context window to 2048 tokens so that refine is used
gpt_35_context = ServiceContext.from_defaults(
    llm=OpenAI(model="gpt-3.5-turbo", temperature=0.3), context_window=2048
)

# Create a VectorStoreIndex from the loaded documents
index = VectorStoreIndex.from_documents(
    documents, service_context=gpt_35_context
)

# Create a query engine for the index with a specified top-k similarity threshold
query_engine = index.as_query_engine(similarity_top_k=2)

# Initialize lists to store contexts and answers for evaluation
contexts = []
answers = []

# Query the index for each question and gather the contexts and responses  
for question in questions:
    response = query_engine.query(question)
    contexts.append([x.node.get_content() for x in response.source_nodes])
    answers.append(str(response))

# Perform evaluation using Ragas framework
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness

# Create a dataset from the questions, answers, and corresponding contexts
ds = Dataset.from_dict(
    {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
    }
)

# Evaluate the dataset using specific metrics
result = evaluate(ds, [answer_relevancy, faithfulness])
print(result)