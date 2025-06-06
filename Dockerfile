# Use a lightweight Python 3.10 image
FROM python:3.10-slim

# 1. Set working directory
WORKDIR /app

# 2. Install system libraries needed by FAISS and sentence-transformers
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 3. Create a writable temp folder for pip under Buildx
RUN mkdir -p /app/tmp && chmod 777 /app/tmp
ENV TMPDIR=/app/tmp
ENV PIP_CACHE_DIR=/app/tmp/pip-cache

# 4. Copy requirements and install all Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy everything (including app/templates and app/static)
COPY . .

# 6. Expose port 8000 for Uvicorn
EXPOSE 8000

# 7. Ensure Python logs flush immediately
ENV PYTHONUNBUFFERED=1

# 8. Start Uvicorn to serve FastAPI (web UI + API)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
