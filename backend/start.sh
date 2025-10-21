#!/bin/bash
# Start script for Render deployment

# Run database migrations if needed (none for now)
# python -m alembic upgrade head

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port $PORT
