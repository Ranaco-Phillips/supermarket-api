# Use official Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies (Debian-based)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     build-essential \
     libpq-dev \
     gcc \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user and set ownership (UID/GID optional)
RUN useradd --create-home appuser
# Copy code and set ownership to appuser so the container won't run as root
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

# Use CMD so it can be overridden; add workers if you like (be careful with memory)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
