"""Script for querying."""

from pathlib import Path
import sys

from langchain import OpenAI
from llama_index import (
    LLMPredictor,
    ResponseSynthesizer,
    ServiceContext,
    StorageContext,
)
from llama_index import load_index_from_storage
from llama_index.indices.keyword_table.retrievers import (
    KeywordTableGPTRetriever,
    KeywordTableRAKERetriever,
)
from llama_index.indices.response import ResponseMode
from llama_index.query_engine import (
    RetrieverQueryEngine,
    RouterQueryEngine,
    SubQuestionQueryEngine,
)
from llama_index.tools.query_engine import QueryEngineTool
from llama_index.selectors.llm_selectors import LLMSingleSelector

storage_dirpath = Path("/index-storage")

llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.1, model_name="gpt-3.5-turbo"))
service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor, chunk_size_limit=256
)

# Rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir=storage_dirpath)
# Load index
index = load_index_from_storage(storage_context, service_context=service_context)

# Configure retrievers
# 1. Retrieves nodes using keywords extracted from query using GPT
retriever_gpt = KeywordTableGPTRetriever(
    index=index, num_chunks_per_query=6, max_keywords_per_query=6
)
# 2. Retrieves nodes using keywords extracted from query using RAKE
retriever_rake = KeywordTableRAKERetriever(
    index=index, num_chunks_per_query=5, max_keywords_per_query=5
)

# Configure response synthesizers
# Default response synthesizer
response_synthesizer_default = ResponseSynthesizer.from_args()
response_synthesizer_summarizer = ResponseSynthesizer.from_args(
    response_mode=ResponseMode.TREE_SUMMARIZE
)

# Create query engines
qe_standard = RetrieverQueryEngine(
    retriever=retriever_gpt,
    response_synthesizer=response_synthesizer_default,
)
qe_simple = RetrieverQueryEngine(
    retriever=retriever_rake,
    response_synthesizer=response_synthesizer_default,
)
qe_summarizer = RetrieverQueryEngine(
    retriever=retriever_gpt,
    response_synthesizer=response_synthesizer_summarizer,
)

# Create query engine tools. Needed to assemble Router Query Engine.
tool_standard = QueryEngineTool.from_defaults(
    query_engine=qe_standard,
    description="Useful for standard queries that are more than 7 words. And not asking it to summarize.",
)
tool_simple = QueryEngineTool.from_defaults(
    query_engine=qe_simple,
    description="Useful for short and simple queries fewer than 7 words.",
)
tool_summarizer = QueryEngineTool.from_defaults(
    query_engine=qe_summarizer,
    description="Useful for queries asking to summarize text.",
)
# tool_complex = QueryEngineTool.from_defaults(
#     query_engine=SubQuestionQueryEngine.from_defaults(
#         query_engine_tools=[
#             QueryEngineTool.from_defaults(
#                 query_engine=qe_standard, description="Useful for complex queries."
#             )
#         ]
#     ),
#     description="Useful for extremely complex queries involving multiple distinct topics."
#     + " Such as to compare and contrast between two or more topics.",
# )

# Create Router Query Engine
query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[
        tool_standard, 
        tool_simple, 
        tool_summarizer, 
        # tool_complex
    ],
)

def send_query(query):
    response = query_engine.query(query)
    return response
