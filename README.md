# SmartCodeReview

A lightweight web app that lets you upload code and custom coding standards to get AI‐powered reviews and suggested fixes instantly.

---

## 🚀 Project Overview

* **What it does:**

  1. You upload a code file (any language).
  2. You upload a “coding standards” document ( .docx or .txt ).
  3. The app uses FAISS to pick the most relevant rules, then sends both code + rules to a pre‐trained LLM.
  4. The LLM returns a Markdown‐formatted review (with severity labels) and a suggested fix.
  5. Your browser renders the results—no more copy/pasting or manual formatting.

* **Why it matters:**

  * Enforces **your team’s real coding rules**, not generic AI heuristics.
  * Delivers **consistent, explainable** feedback on every PR.
  * Saves hours of manual code reviewing and reduces merge‐conflict churn.

---

## 🖼️ Example Results

<details>
<summary>Click to expand a sample output (Markdown → HTML)</summary>

````markdown
⭐ **Review Comments**  
• **High:** Missing docstrings for `add_numbers` and `greet`—docstrings are required by guideline 3.  
• **Medium:** `greet` uses string concatenation; use f-strings for readability.  
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

_In your browser, it renders as neatly styled HTML, complete with colored severity badges and a “Code Quality Score” box at the top._

</details>

---

## 🛠️ Getting Started

### Prerequisites

1. **Python 3.9+** (for local run)  
2. **Docker (optional)**  
3. **GEMINI_API_KEY** (or any LLM key stored in `.env`)  
4. **`python‐multipart`** installed (FastAPI needs it to parse file uploads)  

---

### 1. Clone & Install

```bash
git clone https://github.com/emereshub/llm-code-review-service.git
cd llm-code-review-service
````

#### a) Local (without Docker)

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

* Update `.env` in the project root with:

  ```bash
  GEMINI_API_KEY=your_actual_key_here
  ```

---

### 2. Run Locally

```bash
uvicorn app.main:app --reload --port 8000
```

* Open your browser and navigate to `http://localhost:8000/`.
* You’ll see two dropzones and a **Review My Code** button.

---

### 4. Run with Docker (recommended)

```bash
# Build or pull the latest image
docker pull ghcr.io/emereshub/llm-code-review-service:v2.0.0
# (or locally)
docker build -t ghcr.io/emereshub/llm-code-review-service:v2.0.0 .

# Run the container (mounts current folder as /app inside container)
docker run --rm -it -p 8000:8000 \
  -e GEMINI_API_KEY=your_actual_key \
  -v "$PWD:/app" \
  ghcr.io/emereshub/llm-code-review-service:v2.0.0
```

* In your host’s working directory, place any sample code and `standards.docx`.
* The web UI is now available at `http://localhost:8000/`.

---

## ⚙️ Framework & Architecture

```
Browser UI 
  └─(upload files)─▶ FastAPI (Uvicorn)
                       ├─ Parse multipart: extract code + standards
                       ├─ Build FAISS index on standards
                       ├─ Call pre-trained LLM with (code + top-k guideline chunks)
                       └─ Return JSON { review, fix, score }
                             ▲
                             │
                  Render Markdown→HTML via Marked.js
                             │
                         Browser UI
```
---

## 🤝 Contributions

We welcome bug reports, feature requests, and pull requests:

1. Fork the repo
2. Create your feature branch:

   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. Commit your changes
4. Push to your fork and open a PR
---

## 📚 Author & Portfolio

**Emere Ejor**
AI/ML Engineer & Full-Stack Developer
[Portfolio](https://ai-ml-portfolio-h7hv.vercel.app/) • [GitHub](https://github.com/emereshub)

Feel free to connect or raise issues/suggestions!

---

> © 2025 Emere Ejor. All rights reserved.
