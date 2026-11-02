from pdf_parser_1 import extracted_text_from_pdf
from text_cleaner_2 import clean_text

def preprocess_pdf(pdf_path):

    #step 1 :- extract raw text from pdf
    pages = extracted_text_from_pdf(pdf_path)

    #step 2:- create an empty list to append pagenumber and content
    parsed_doc = []

    for page in pages:
        raw_text = page["content"]

        #clean the extracted text
        cleaned_content = clean_text(raw_text)

        #store cleaned_text with page metadata
        parsed_doc.append({
            "page_number": page['page_number'],
            "content" : cleaned_content
        })

    return parsed_doc

