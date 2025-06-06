# app/services/review_engine.py

import os
import re
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

_model = None

def get_llm():
    """
    Lazily initialize (and cache) the Google Gemini client.
    """
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")
        genai.configure(api_key=api_key)
        _model = ChatGoogleGenerativeAI(
            model="models/gemini-1.5-flash-latest",
            google_api_key=api_key
        )
    return _model

def build_faiss_index(standards_text: str):
    """
    Split the given standards_text into overlapping chunks,
    embed them with HuggingFace, and build a FAISS index in memory.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    chunks = splitter.split_text(standards_text)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_texts(chunks, embeddings)

def get_top_guidelines(code: str, standards_text: str, top_k: int = 3) -> str:
    """
    Build a FAISS index on-the-fly from the provided standards_text
    (instead of loading a single docx), then similarity search on code.
    Returns the top_k chunks joined by newline.
    """
    db = build_faiss_index(standards_text)
    docs = db.similarity_search(code, k=top_k)
    return "\n".join(doc.page_content for doc in docs)

def generate_code_review_with_standards(code: str, standards_text: str) -> tuple[str, float | None]:
    """
    1. Call get_top_guidelines(code, standards_text) to get relevant snippets.
    2. Craft a Gemini prompt that asks Gemini to:
       - Produce a Markdown bullet list of issues + suggestions + severity.
       - Append a final line “Score: X.YZ” (where X.YZ ∈ [0.00, 1.00]).
    3. Invoke Gemini via get_llm().invoke(prompt).content → a single string.
    4. Parse out “Score: <number>” from the end via regex.
    5. Return (full_markdown_review, parsed_score_value_or_None).
    """
    guidelines = get_top_guidelines(code, standards_text)
    prompt = f"""You are a senior code reviewer.

Here are the relevant code review guidelines:
{guidelines}

Please review the following code and produce output in this format:

1. Start with a Markdown bullet‐list of all issues and suggestions, indicating severity (Low/Medium/High).
2. At the very end, on its own line, write: "Score: X.YZ", where X.YZ is a decimal between 0.00 and 1.00 representing the overall code quality (higher is better).

Code:
{code}
"""
    response = get_llm().invoke(prompt).content

    # Extract “Score: <number>” from the final lines (if present)
    score_match = re.search(r"^Score:\s*([0-1](?:\.\d{1,2})?)\s*$", response, flags=re.MULTILINE)
    if score_match:
        try:
            score_value = float(score_match.group(1))
        except ValueError:
            score_value = None
    else:
        score_value = None

    return response, score_value

def generate_suggested_fix_with_standards(code: str, standards_text: str) -> str:
    """
    1. Call get_top_guidelines(code, standards_text) to get relevant snippets.
    2. Craft a Gemini prompt that instructs Gemini to rewrite the code so it fully
       complies with those standards. Return only the code block (no commentary).
    3. Invoke Gemini via get_llm().invoke(...) and return the content.
    """
    guidelines = get_top_guidelines(code, standards_text)
    prompt = f"""You are a senior software engineer.

You must rewrite the code below to fully comply with the following coding standards:

{guidelines}

Instructions:
- Apply every rule listed above
- Fix all naming, formatting, structural, and stylistic issues as described
- Ensure the corrected code is clean, complete, and consistent with the rules
- Only return the fixed code — do not include explanations or commentary

Code:
{code}
"""
    return get_llm().invoke(prompt).content
