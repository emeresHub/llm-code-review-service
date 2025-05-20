from docx import Document
import os

def extract_standards_from_docx(path: str) -> str:
    """
    Extracts all non-empty paragraphs from a .docx file and joins them
    as a single string to be used in LLM prompts.

    Parameters:
        path (str): Path to the .docx file.

    Returns:
        str: Concatenated text from all non-empty paragraphs.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    try:
        doc = Document(path)
        paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)

    except Exception as e:
        raise RuntimeError(f"Failed to parse DOCX file '{path}': {str(e)}")
