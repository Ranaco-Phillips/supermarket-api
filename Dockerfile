# Use official Python base image (slim to keep image small)
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (helps with Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code into container
COPY . .

# Expose FastAPI’s default port
EXPOSE 8000

# Command to run API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
