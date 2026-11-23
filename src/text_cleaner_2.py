import re
import unicodedata

_BULLET_RE = re.compile(r"^([•●▪◦‣\-*–—]|\d+[\.\)])\s+")
_NUMBERED_HEADING_RE = re.compile(r"^\d+(?:\.\d+)+\.?\s+")
_CAPTION_RE = re.compile(r"^(?:Fig\.?|Figure|Table|Eq\.?)\s*\d+", re.IGNORECASE)
_SLIDE_NOISE_RE = re.compile(r"^(?:slide\s*\d+|\d+\s*/\s*\d+|\d+)$", re.IGNORECASE)
_HYPHEN_BREAK_RE = re.compile(r"(?<=[A-Za-z])-\s*\n\s*(?=[a-z])")
_WHITESPACE_RE = re.compile(r"[ \t\xa0]+")


def clean_text(text: str) -> str:
    """Self-contained cleaner for academic PPT/PDF text extracted for RAG."""
    if not text:
        return ""

    def _classify_line(line: str) -> str:
        if _SLIDE_NOISE_RE.match(line):
            return "noise"
        if _BULLET_RE.match(line):
            return "bullet"
        if _NUMBERED_HEADING_RE.match(line):
            return "heading"
        if _CAPTION_RE.match(line):
            return "caption"

        # Refined Slide Title Heuristic:
        # Kam se kam 2 words hon, number/unit se start na ho, aur end mein punctuation/percentage na ho
        words = line.split()
        if 2 <= len(words) <= 10 and line[-1] not in ".!?,:;%" and not line[0].isdigit():
            if line.istitle() or line.isupper():
                return "heading"

        return "text"

    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
    text = _HYPHEN_BREAK_RE.sub("", text)

    cleaned_blocks = []
    in_paragraph = False

    for raw_line in text.split("\n"):
        line = _WHITESPACE_RE.sub(" ", raw_line).strip()

        if not line:
            if cleaned_blocks and cleaned_blocks[-1] != "":
                cleaned_blocks.append("")
            in_paragraph = False
            continue

        line_type = _classify_line(line)

        if line_type == "noise":
            continue

        elif line_type == "heading":
            if cleaned_blocks and cleaned_blocks[-1] != "":
                cleaned_blocks.append("")
            cleaned_blocks.append(f"## {line}")
            in_paragraph = False

        elif line_type == "bullet":
            standardized_bullet = _BULLET_RE.sub("- ", line, count=1)
            cleaned_blocks.append(standardized_bullet)
            in_paragraph = True

        elif line_type == "caption":
            cleaned_blocks.append(f"[{line}]")
            in_paragraph = False

        else:
            if in_paragraph and cleaned_blocks:
                prev_char = cleaned_blocks[-1][-1]
                if line[0].islower() or prev_char not in ".!?:":
                    cleaned_blocks[-1] += " " + line
                else:
                    cleaned_blocks.append(line)
            else:
                cleaned_blocks.append(line)
                in_paragraph = True

    return "\n".join(cleaned_blocks).strip()