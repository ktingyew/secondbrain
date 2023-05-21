"""Script for querying."""

from pathlib import Path

from langchain import OpenAI
from llama_index import LLMPredictor, ResponseSynthesizer, ServiceContext, StorageContext
from llama_index import load_index_from_storage
from llama_index.indices.keyword_table.retrievers import KeywordTableGPTRetriever
from llama_index.query_engine import RetrieverQueryEngine

storage_dirpath = Path("/index-storage")

llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.1, model_name="gpt-3.5-turbo"))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=256)

# Load storage context into memory
storage_context = StorageContext.from_defaults(persist_dir=storage_dirpath)
# Load index from storage context
index = load_index_from_storage(storage_context)

# Configure retriever
retriever = KeywordTableGPTRetriever(
    index=index
)

# Configure response synthesizer
response_synthesizer = ResponseSynthesizer.from_args()

# Assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)

def send_query(query):
    response = query_engine.query(query)
    return response
