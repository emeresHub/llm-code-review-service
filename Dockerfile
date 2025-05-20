FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed by FAISS and sentence-transformers
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all other code files
COPY . .

# Optional: expose the port your app will run on
EXPOSE 8000

# Set environment variable for unbuffered stdout/stderr
ENV PYTHONUNBUFFERED=1

# Default entrypoint runs your CLI / API
ENTRYPOINT ["python", "entrypoint.py"]
