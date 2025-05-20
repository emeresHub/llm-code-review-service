from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(
    title="LLM Code Review API",
    description="Review source code using Google Gemini + custom coding standards.",
    version="1.0.0"
)

# Optional: Allow cross-origin requests if accessed from a frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "LLM Code Review API is running"}
