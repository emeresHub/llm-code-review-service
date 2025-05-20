import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

CODING_STANDARDS_PATH = "standards/coding_standards.docx"

def load_coding_standards_text():
    import docx
    doc = docx.Document(CODING_STANDARDS_PATH)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

def initialize_faiss_db():
    standards_text = load_coding_standards_text()
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    chunks = splitter.split_text(standards_text)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_texts(chunks, embeddings)

# Delay creating db, model, and Gemini config to runtime, after env loaded
db = None
model = None

def initialize():
    global db, model
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY env variable not set")

    genai.configure(api_key=API_KEY)
    model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=API_KEY)
    db = initialize_faiss_db()

def llm(prompt: str) -> str:
    global model
    if model is None:
        initialize()
    return model.invoke(prompt).content

def get_relevant_guidelines(code_snippet: str, top_k: int = 3) -> str:
    global db
    if db is None:
        initialize()
    docs = db.similarity_search(code_snippet, k=top_k)
    return "\n".join([doc.page_content if hasattr(doc, "page_content") else doc for doc in docs])

def generate_code_review(code: str) -> str:
    standards = get_relevant_guidelines(code)
    prompt = f"""You are a senior code reviewer.

Here are the relevant code review guidelines:
{standards}

Please review the following code and:
- List all issues as bullet points
- Provide suggestions for improvements
- Indicate severity (Low, Medium, High)

Code:
{code}
"""
    return llm(prompt)

def generate_suggested_fix(code: str) -> str:
    standards = get_relevant_guidelines(code)
    prompt = f"""You are a senior software engineer.

You must rewrite the code below to fully comply with the following coding standards:

{standards}

Instructions:
- Apply every rule listed above
- Fix all naming, formatting, structural, and stylistic issues as described
- Ensure the corrected code is clean, complete, and consistent with the rules
- Only return the fixed code — do not include explanations or commentary

Code:
{code}
"""
    return llm(prompt)
