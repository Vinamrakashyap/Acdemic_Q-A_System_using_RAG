#Retriever ka kaam hai:
#- User query receive karna.
#- Query embedding generate karwana.
#- Vector database mein relevant documents search karna.
#- Relevant documents return karna.
#Notice karo, ye kaam tumhara similarity_search() bhi kar raha tha.
#Toh phir Retriever kyun?
#Because Retriever ek standardized interface provide karta hai, jise hum aage LangChain ke chains
#aur RAG pipeline ke saath easily integrate kar sakte hain.
from vector_store_6 import vector_store

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 8
    }
)