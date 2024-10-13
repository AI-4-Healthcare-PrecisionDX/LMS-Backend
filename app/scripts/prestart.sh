#!/usr/bin/env bash

set -e  # Exit the script on any error
set -x  # Print commands before running them

echo "Waiting for the database to be ready..."
python app/backend_pre_start.py

echo "Applying Alembic migrations..."
alembic upgrade head

echo "Starting the FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
