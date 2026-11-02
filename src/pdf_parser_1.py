import pymupdf

def extracted_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    extracted_pages = []
    for page_number, page in enumerate(doc, start=1):

        text = page.get_text("text")
        extracted_pages.append({
            "page_number" : page_number,
            "content" : text
        })

    doc.close()

    return extracted_pages





