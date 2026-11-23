import os
from langchain_community.vectorstores import FAISS
from embeddings_5 import embedding_model, generate_embeddings

INDEX_PATH = "faiss_index"

def build_and_save_vector_store():
    print("Building new FAISS index from PDF (extracting text & diagrams)...")
    texts, vectors, metadatas = generate_embeddings()
    text_embeddings = list(zip(texts, vectors))

    vs = FAISS.from_embeddings(
        text_embeddings=text_embeddings,
        embedding=embedding_model,
        metadatas=metadatas
    )
    vs.save_local(INDEX_PATH)
    print("FAISS index saved locally.")
    return vs

if os.path.exists(INDEX_PATH):
    vector_store = FAISS.load_local(
        INDEX_PATH,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )
else:
    vector_store = build_and_save_vector_store()