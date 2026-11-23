from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from text_chunker_4 import get_all_chunks

load_dotenv()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

def generate_embeddings():
    all_docs = get_all_chunks()
    texts = [doc.page_content for doc in all_docs]
    metadatas = [doc.metadata for doc in all_docs]
    vectors = embedding_model.embed_documents(texts)
    return texts, vectors, metadatas