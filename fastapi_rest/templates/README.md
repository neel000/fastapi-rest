# Setup Process
    pip install -r app/requirements.txt
    ./run.sh

# Migrations
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head

# Run For All Platform
    uvicorn main:app --reload

# Run For Linux System
    ./run.sh