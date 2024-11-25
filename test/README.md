
# Setup Process
    sudo apt install virtualenv
    virtualenv env
    source env/bin/activate
    pip install -r app/requirements.txt
    ./run.sh

# Migrations
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head

```bash
export PYTHONPATH=$(pwd)
```