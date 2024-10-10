#!/usr/bin/env bash

set -e  # Exit the script on any error
set -x  # Print commands before running them

# Wait for the DB to be ready before running migrations
python app/backend_pre_start.py

# Apply Alembic migrations
alembic upgrade head

# Run the main process
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload