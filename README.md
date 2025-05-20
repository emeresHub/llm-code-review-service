# 🔍 SmartCodeReview – AI-Powered Code Review with Gemini and LangChain

**SmartCodeReview** automatically checks your Python code against **custom team coding standards** using Google Gemini, LangChain, and FAISS. It produces precise, contextual review reports and suggested fixes based on your real coding rules — not generic AI feedback.

---

## 📌 Overview

* **Input:** Raw code
* **Process:** Semantic chunking of your coding standards document + vector search using FAISS
* **LLM:** Google Gemini generates custom review feedback and code fixes
* **Output:** Detailed review saved as a `.txt` file in a local `reviews` folder for easy inspection

Ideal for teams wanting **automated, consistent, and explainable code reviews** that integrate your own rules.

---

## 🚀 Quick Start Using Docker (Recommended)

### Prerequisites

* Have a valid **GEMINI\_API\_KEY** from Google Gemini
* Docker installed and running on your system
* A local directory containing your Python code files to review

---

### Step 1: Pull the Docker Image

```bash
docker pull ghcr.io/emereshub/llm-code-review-service:v1.0.0
```

---

### Step 2: Create the `reviews` folder (if it doesn't exist)

The container will save code review output files here.

```bash
mkdir -p reviews
```

---

### Step 3: Run the Docker Container to Review Your Code File

Replace `your_gemini_api_key` with your actual API key, and adjust the path to your Python script:

```bash
docker run --rm \
  -v "$PWD/reviews:/app/reviews" \
  -v "$PWD:/app" \
  -e GEMINI_API_KEY=your_gemini_api_key \
  ghcr.io/emereshub/llm-code-review-service:v1.0.0 review /app/path_to_your_script.py
```

* `$PWD` mounts your current working directory inside the container at `/app`
* The reviews folder is mounted inside as `/app/reviews` to persist output
* The service reads your code file and saves the review as `/app/reviews/<script_name>-review.txt`

---

### Step 4: Inspect the Review Output

Open the review file inside your local `reviews` folder to see detailed issues, suggestions, and severity levels.

---

## 💡 Why Use This Tool?

* **Automates** coding standard enforcement — no more manual, inconsistent reviews
* Produces **customized feedback** directly aligned to your team’s coding rules
* Saves **time** and **improves code quality** across the team with instant results
* Easy to integrate into dev workflows, CI pipelines, or pre-commit hooks

---

## ⚙️ Additional Notes

* Make sure Docker daemon is running before executing the `docker run` command
* The `reviews` folder must exist on your host for outputs to be saved correctly
* Only one file can be reviewed per run; repeat for multiple files
* For advanced usage or to run the API server, refer to the full repository and local run instructions

---

## Support & Feedback

Please test the tool with your code files and share your feedback. This will help us refine the system and improve our team’s coding standards enforcement.

---

**Thank you!**

