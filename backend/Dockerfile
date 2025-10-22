# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Create logs directory
RUN mkdir -p logs

# Set environment variable for unbuffered Python output
ENV PYTHONUNBUFFERED=1

# Default port (Railway will override with PORT env var)
ENV PORT=8000

# Expose port
EXPOSE 8000

# Start command using shell to properly expand variables
CMD sh -c "echo 'Starting on port: $PORT' && uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level info"