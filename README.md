# SmartCodeReview

AI-Powered web app for instant code reviews against **your** custom coding standards.

---

## 🚀 Overview

1. **Upload** your code file (any language).
2. **Upload** your “coding standards” document (`.docx` or `.txt`).
3. **FAISS** selects the most relevant rules.
4. A **pre-trained LLM** generates:

   * A **Markdown review** (bullet list + severity).
   * A **suggested fix** (code block).
   * A **quality score** (0–1).
5. **Browser** renders the results as HTML—no copying or formatting required.

**Why It Matters**

* Enforces your team’s actual rules, not generic AI tips.
* Delivers consistent, explainable feedback.
* Saves hours of manual reviewing and reduces errors.

---

## 🖼️ Example Output

<details>
<summary>Click to expand Markdown preview</summary>

````markdown
⭐ **Review Comments**  
• **High:** Missing docstrings for `add_numbers` and `greet` (guideline 3).  
• **Medium:** `greet` uses string concatenation; use f-strings instead.  
• **Low:** No blank line separating functions (guideline 8).

⭐ **Suggested Fix**
```python
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.
    :param a: first number
    :param b: second number
    :return: sum of a and b
    """
    return a + b

def greet(name: str) -> None:
    """
    Print a greeting message.
    :param name: The name to greet.
    """
    print(f"Hello, {name}")
````

**Code Quality Score:** 0.75 / 10

````

</details>

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.9+** (for local run)  
- **Docker** (optional, recommended)  
- **LLM API key** (stored in a `.env` as `GEMINI_API_KEY`)  
- `python-multipart` (FastAPI file uploads)

### 1. Clone & Install

```bash
git clone https://github.com/emereshub/llm-code-review-service.git
cd llm-code-review-service
````

#### Local

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt python-multipart
echo "GEMINI_API_KEY=your_key_here" > .env
```

#### Docker

```bash
# Pull or build v2.0.0
docker pull ghcr.io/emereshub/llm-code-review-service:v2.0.0
# or
docker build -t ghcr.io/emereshub/llm-code-review-service:v2.0.0 .

# Run (mount current directory)
docker run --rm -it -p 8000:8000 \
  -e GEMINI_API_KEY=your_key_here \
  -v "$PWD:/app" \
  ghcr.io/emereshub/llm-code-review-service:v2.0.0
```

### 2. Run Locally (no Docker)

```bash
uvicorn app.main:app --reload --port 8000
```

Open [http://localhost:8000](http://localhost:8000), upload your code and standards, then click **Review My Code**.

---

## ⚙️ Architecture

```
Browser UI 
  └─(upload files)─▶ FastAPI (Uvicorn)
                       ├─ Extract code + standards from multipart
                       ├─ Build FAISS index on standards
                       ├─ Call LLM with (code + top-k rules)
                       └─ Return JSON { review (MD), suggested_fix (MD), score }
                             ▲
                             │
                  Render Markdown→HTML via Marked.js
                             │
                         Browser UI
```

---

## 📚 Author

**Emere Ejor**
AI/ML Engineer & Full-Stack Developer
[Portfolio](https://ai-ml-portfolio-h7hv.vercel.app/) • [GitHub](https://github.com/emereshub)

---

© 2025 Emere Ejor. All rights reserved.
