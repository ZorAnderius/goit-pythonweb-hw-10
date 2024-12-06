#!/bin/bash
echo "Waiting for postgres to be ready..."
./wait-for-it.sh postgres:5432 --timeout=10 --strict -- echo "PostgreSQL is ready!"

echo "Checking if migrations are needed..."
if alembic current | grep -q "No such table"; then
  echo "Generating initial migration files..."
  alembic revision --autogenerate -m "Init"
  if [ $? -eq 0 ]; then
    echo "Migration files generated successfully."
  else
    echo "Failed to generate migration files."
    exit 1
  fi
fi

echo "Running migrations..."
alembic upgrade head
if [ $? -eq 0 ]; then
  echo "Migrations applied successfully."
else
  echo "Migrations failed."
  exit 1
fi

echo "Starting the application..."
uvicorn main:app --host 0.0.0.0 --port 8000