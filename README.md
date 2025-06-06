# 🔍 AuditLens – AI-Powered Code Review

A lightweight web app where you upload your code and custom coding-standards document (DOCX/TXT) to get instant, AI-powered review comments, suggested fixes, and a quality score. It uses FAISS to retrieve only the most relevant rules and a pre-trained LLM to generate feedback that matches your team’s standards.

---

## 📌 Overview

1. Upload a code file (any extension).
2. Upload a “coding standards” document (`.docx` or `.txt`).
3. FAISS indexes your standards and selects the top-k rules for the code.
4. A pre-trained LLM receives (code + top-k rules) and returns:
   - Markdown review (bullet list with Low/Medium/High severity)
   - Markdown suggested fix
   - Numeric score (0.00–1.00)
5. Browser renders the Markdown as styled HTML via Marked.js.

---

## 🖼️ Example Output

```markdown
- **High:** Missing docstrings for `add_numbers` and `greet` (guideline 3)
- **Medium:** `greet` uses string concatenation; use f-strings
- **Low:** No blank line between functions (guideline 8)

Score: 0.75

```

```python
# Suggested Fix:
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.
    """
    return a + b

def greet(name: str) -> None:
    """
    Print a greeting message.
    """
    print(f"Hello, {name}")

```

*(In your browser, this appears with colored severity badges and a “Code Quality Score” box.)*

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+ (for local run)
- Docker (optional, recommended)
- `GEMINI_API_KEY` (or any LLM key) in a `.env` at project root
- `python-multipart` (FastAPI needs it)

### 1. Clone & Prepare

```bash
git clone --branch v2.0.0 --single-branch \
  https://github.com/emereshub/llm-code-review-service.git
cd llm-code-review-service
echo "GEMINI_API_KEY=your_actual_key" > .env

```

### 2. Local Run (no Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt python-multipart
uvicorn app.main:app --reload --port 8000

```

Open [http://localhost:8000](http://localhost:8000/), then upload your code and standards, click **Review My Code**, and view the results.

### 3. Run with Docker (recommended)

```bash
docker pull ghcr.io/emereshub/llm-code-review-service:v2.0.0
# (Or build locally)
# docker build -t ghcr.io/emereshub/llm-code-review-service:v2.0.0 .
docker run --rm -it -p 8000:8000 \
  -e GEMINI_API_KEY=your_actual_key \
  -v "$PWD:/app" \
  ghcr.io/emereshub/llm-code-review-service:v2.0.0

```

Visit [http://localhost:8000](http://localhost:8000/) to use the UI.

---

## ⚙️ Architecture

```
Browser UI
  └─(upload)─▶ FastAPI (Uvicorn)
                   ├─ Extract code + standards
                   ├─ Build FAISS index on standards
                   ├─ Call pre-trained LLM with (code + top-k rules)
                   └─ Return { review (MD), suggested_fix (MD), score }
                         ▲
                         │
       Render Markdown → HTML (Marked.js)
                         │
                     Browser UI

```

- **Front End** (`app/templates/`, `app/static/`): HTML/CSS layout + Vanilla JS (file selection, `fetch("/review")`, Markdown→HTML).
- **Back End** (FastAPI + Uvicorn): Serves UI and `/review` API, parses `.docx`/`.txt` standards, builds FAISS index, queries LLM, returns `ReviewOutput`:
    
    ```json
    {
      "review": "…Markdown…",
      "suggested_fix": "…Markdown code…",
      "score": 0.85
    }
    
    ```
    

---

## 📚 Author & Portfolio

**Emere Ejor** – AI/ML Engineer & Full-Stack Developer

[Portfolio](https://ai-ml-portfolio-h7hv.vercel.app/) • [GitHub](https://github.com/emereshub)

© 2025 Emere Ejor