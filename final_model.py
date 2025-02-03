import PyPDF2
import llama_parse
from datetime import datetime
from llama_parse import LlamaParse
from all_imports import *
import nest_asyncio
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage

nest_asyncio.apply()

parser = LlamaParse(
    api_key=os.environ["LLAMA_INDEX_API_KEY"],
    result_type="text",
    chunk_size="paragraph",
    num_workers=4,
    verbose=True,
)

# sync
documents = parser.load_data("beige_book_pdfs/BeigeBook_20240117.pdf")

# Create a vector index with no chunking
vector_index = VectorStoreIndex.from_documents(
    documents,
    transformations=[]
)

# Save the index to disk
vector_index.storage_context.persist(persist_dir="storage/vector")

# Load the index from disk
vector_storage = StorageContext.from_defaults(persist_dir="storage/vector")
vector_index = load_index_from_storage(vector_storage)

# Create query engine
vector_query_engine = vector_index.as_retriever()

# Example query
vector_response = vector_query_engine.retrieve("What moved a lot?")
print("Vector Query Response:", vector_response)
import pdb; pdb.set_trace()