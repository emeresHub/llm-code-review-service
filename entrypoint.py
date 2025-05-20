import sys
import os
from dotenv import load_dotenv
from app.services.review_engine import generate_code_review

load_dotenv()

def check_api_key():
    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY is not set. Please provide it in .env or as an environment variable.")
        sys.exit(1)

def run_cli(file_path: str):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    print(f"\nReviewing file: {file_path}")
    review = generate_code_review(code)

    # Create reviews folder if not exists
    os.makedirs("reviews", exist_ok=True)

    base_name = os.path.basename(file_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join("reviews", f"{name_without_ext}-review.txt")

    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write(review)

    print(f"\nCode Review saved to: {output_path}")
    print("\nDone.\n")

def run_api():
    import uvicorn
    print("Starting FastAPI server on http://localhost:8000")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    check_api_key()

    if len(sys.argv) == 3 and sys.argv[1] == "review":
        run_cli(sys.argv[2])
    else:
        run_api()
