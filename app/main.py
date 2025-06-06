import os
from dotenv import load_dotenv

# 1. Load environment variables from .env (so GEMINI_API_KEY is available)
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import router

app = FastAPI(
    title="LLM Code Review Web UI",
    description="Drag-and-drop code review with custom coding standards",
    version="2.0.0"
)

# 2. (Same as before) Allow cross-origin requests if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount the "static" directory so CSS/JS can be served
#    – any request to /static/... will load files from app/static/...
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 4. Configure Jinja2 templates directory (for index.html)
templates = Jinja2Templates(directory="app/templates")

@app.get("/", include_in_schema=False)
async def root(request: Request):
    """
    Serve the main drag-and-drop web page (index.html).
    """
    return templates.TemplateResponse("index.html", {"request": request})

# 5. Register all API routes (the /review endpoint is in app/routes.py)
app.include_router(router)
