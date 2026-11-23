from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from cleaned_text_3 import preprocess_pdf

pdf_path = "data/demo_files/unit-3RER..pdf"

def chunk_documents(parsed_doc: list, chunk_size: int = 1000, overlap_size: int = 200) -> list[Document]:
    if chunk_size <= overlap_size:
        raise ValueError("chunk_size must be greater than overlap_size")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap_size,
        separators=["\n## ", "\n\n", "\n", " ", ""]
    )

    all_docs = []
    for page in parsed_doc:
        text = page["content"]
        if not text.strip():
            continue

        chunks = splitter.split_text(text)
        for chunk in chunks:
            all_docs.append(
                Document(
                    page_content=f"[Slide {page['page_number']}]\n{chunk}",
                    metadata={"page_number": page["page_number"]}
                )
            )
    return all_docs

def get_all_chunks() -> list[Document]:
    parsed_doc = preprocess_pdf(pdf_path)
    return chunk_documents(parsed_doc)