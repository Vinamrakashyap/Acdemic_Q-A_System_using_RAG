import base64
import pymupdf
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def _extract_diagram_details(page, page_number: int) -> str:
    """Agar slide par koi diagram/image hai toh Vision model se uske labels aur flow nikale."""
    images = page.get_images(full=True)
    if not images:
        return ""

    # Slide ko high-res image mein render karein taaki diagram ke arrows aur text labels clear dikhein
    pix = page.get_pixmap(dpi=150)
    img_b64 = base64.b64encode(pix.tobytes("png")).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze this presentation slide image. If there is a technical diagram, "
                            "flowchart, or schematic, extract ONLY the exact component names, "
                            "temperatures, pressures, efficiencies, and step-by-step flow shown in the diagram. "
                            "Do NOT add any outside textbook knowledge. If there is no diagram, reply strictly with 'NONE'."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_b64}"},
                    },
                ],
            }
        ],
    )

    diagram_text = response.choices[0].message.content.strip()
    if diagram_text.upper() == "NONE":
        return ""
    return f"\n[Diagram Components & Flow - Slide {page_number}]:\n{diagram_text}\n"


def extracted_text_from_pdf(pdf_path: str, extract_diagrams: bool = True) -> list:
    doc = pymupdf.open(pdf_path)
    extracted_pages = []

    for page_number, page in enumerate(doc, start=1):
        # sort=True se multi-column aur PPT boxes sahi reading order mein extract hote hain
        text = page.get_text("text", sort=True)

        if extract_diagrams:
            text += _extract_diagram_details(page, page_number)

        extracted_pages.append({
            "page_number": page_number,
            "content": text
        })

    doc.close()
    return extracted_pages