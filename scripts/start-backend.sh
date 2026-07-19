#!/bin/bash
# Start the FastAPI backend server locally
# Prerequisites: PostgreSQL running, .env configured

cd "$(dirname "$0")/../backend"
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8100