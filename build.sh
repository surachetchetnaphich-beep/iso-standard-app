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

echo "--- STEP 5: Verifying Structure ---"
ls -d config/

echo "--- STEP 6: Creating Superuser ---"
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
password = 'mn2@1234'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email='', password=password)
    print(f'Superuser "{username}" created.')
else:
    print(f'Superuser "{username}" already exists.')
EOF

echo "--- BUILD SUCCESSFUL ---"
