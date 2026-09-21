FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system dependencies (required for ML libraries and OCR)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libgomp1 \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the rest of the application code
COPY . .

# Use Render's default port 10000 or allow PORT environment variable
ENV PORT=10000
EXPOSE $PORT

# Start the server using uvicorn
CMD uvicorn backend.run_server:app --host 0.0.0.0 --port $PORT --workers 1
