# syntax=docker/dockerfile:1.10

# Use Python as the base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ ./app/
COPY download_model.py .

# Download the latest model from DagsHub securely
RUN --mount=type=secret,id=dagshub_token,env=DAGSHUB_TOKEN,required=true \
    python download_model.py

# Start FastAPI
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
