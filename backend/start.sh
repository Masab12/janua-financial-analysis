#!/bin/sh
# Startup script for Railway deployment

echo "==================================="
echo "Starting JANUA Financial API"
echo "==================================="
echo "PORT environment variable: ${PORT}"
echo "Python version: $(python --version)"
echo "==================================="

# Use the PORT environment variable, default to 8000 if not set
PORT=${PORT:-8000}

echo "Starting uvicorn on port: $PORT"

# Start uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --log-level info
