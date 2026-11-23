from pdf_parser_1 import extracted_text_from_pdf
from text_cleaner_2 import clean_text

def preprocess_pdf(pdf_path: str) -> list:
    pages = extracted_text_from_pdf(pdf_path, extract_diagrams=True)
    parsed_doc = []

    for page in pages:
        raw_text = page["content"]
        cleaned_content = clean_text(raw_text)

        parsed_doc.append({
            "page_number": page["page_number"],
            "content": cleaned_content
        })

    return parsed_doc