# AnonQA API

A FastAPI-based REST API for an anonymous Q&A platform where users can ask and answer questions anonymously.

![image](https://github.com/user-attachments/assets/0c58050a-5447-480f-9917-d99ab1d6b0d1)


## Features

- User authentication with JWT tokens
- User registration and login
- Ask questions anonymously (soon: as a registered user )
- Answer questions directed to you
- View questions and their answers
- PostgreSQL database integration
- Alembic migrations for database versioning

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Alembic (Database migrations)
- Pydantic (Data validation)
- JWT (Authentication)
- Bcrypt (Password hashing)

## Prerequisites

- Python 3.8 - 3.12 (psycopg2 does not currently work with python13)
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/2wons/anonqa-api.git
cd anonqa-api
```

2. make and activate virtual env

```bash
python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```

3. install depss

```bash
pip install -r requirements.txt
```

4. create and fill up .env file

```bash
# .env file
SECRET_KEY=your_secret_key

POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=anonqa_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
```

5. Run db migrations

```bash
alembic upgrade head
```

6. run

```bash
fastapi dev main.py
# fastapi run main.py (prod)
```

The API will be available at `http://localhost:8000`
swagger docs @ `http://localhost:8000/docs#`
