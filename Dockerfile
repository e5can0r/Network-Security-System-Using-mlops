# Use newer, more secure Debian base
FROM python:3.10-slim-bookworm

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    awscli \
    build-essential \
    gcc \
    curl \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy everything else into container
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI using Uvicorn (recommended for production)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
