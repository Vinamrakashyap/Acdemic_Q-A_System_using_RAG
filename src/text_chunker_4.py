from cleaned_text_3 import preprocess_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

pdf_path = "data/demo_files/unit-3RER..pdf"
parsed_doc = preprocess_pdf(pdf_path)

#parsed_doc mein 2 cheejein hai:- 1) Page_Number 2)Content
#Ek baat yaad rakhna: chunk_size=500 aur overlap_size=100 abhi hamari starting configuration hai.
#Baad mein retrieval results dekhkar improve karenge.
def chunk_text_by_chars(text:str, chunk_size:int = 500, overlap_size:int = 100) -> list:

    if chunk_size <= overlap_size:
        raise ValueError("chunk size must be greater than overlap_size")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = overlap_size,
        separators=["\n\n","\n"," ",""]
    )

    chunks = splitter.split_text(text)
    return chunks
all_chunks = []

for page in parsed_doc:
    text = page["content"]
    chunks = chunk_text_by_chars(text)
    all_chunks.extend(chunks)

#testing
#print(len(all_chunks))
#print(all_chunks[3])

