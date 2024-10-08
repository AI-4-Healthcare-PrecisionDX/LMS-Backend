# FastAPI Template

## Getting started

### Setting up the project

- Clone this repository: `git clone git@github.com:AI-4-Healthcare-PrecisionDX/LMS-Backend.git`
- Move the the project directory: `cd ~/lms-backend`
- Create the virtual environment and activate it: `python3 -m venv venv` & `source venv/bin/activate`
- Install the dependencies: `pip install -r requirements.txt`

### Project Dependencies

This project relies on several technologies and dependencies, including:

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance), web framework for building APIs with Python.
- [SQLAlchemy](https://www.sqlalchemy.org/): A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **PostgreSQL Database**: This project uses a PostgreSQL database to store and manage data.
- [Alembic](https://alembic.sqlalchemy.org/): A database migration tool for SQLAlchemy.
- ... (other project dependencies)

### Working on the project

- Move into the project directory: `cd ~/lms-backend`
- Run the development task:
  - Setup the [Databases](#databases)
  - Start the server: `fastapi dev app/main.py`
  - Starts a server running at http://127.0.0.1:8000
  - Automatically restarts when any of your files change
  - Testing the api endpoints at http://127.0.0.1:8000/docs

### Databases

- Create a Database name: `YOUR DATABASE`
- Run the following command to setup automatically the database:

```bash
alembic init alembic
```

- To generate a new Alembic migration:

```bash
alembic revision --autogenerate -m "YOUR MESSAGE"
```

- To apply the latest database migration:

```bash
alembic upgrade head
```
