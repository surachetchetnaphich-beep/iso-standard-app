#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- STEP 1: Upgrading pip ---"
pip install --upgrade pip

echo "--- STEP 2: Installing requirements ---"
pip install -r requirements.txt

echo "--- STEP 3: Collecting static files ---"
# We set a dummy DATABASE_URL if it's not present during build to prevent failures
export DATABASE_URL=${DATABASE_URL:-"postgres://user:pass@localhost:5432/dbname"}
python manage.py collectstatic --no-input

echo "--- STEP 4: Running database migrations ---"
python manage.py migrate

echo "--- BUILD SUCCESSFUL ---"
