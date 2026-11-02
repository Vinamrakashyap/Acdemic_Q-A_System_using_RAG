from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from text_chunker_4 import all_chunks
load_dotenv()

llm = OpenAIEmbeddings(
    model = "text-embedding-3-small"
)

#generate embeddings for all chunks
vectors = llm.embed_documents(all_chunks)
