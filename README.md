# fastapi-auth-starter
Simple OAuth2 Password Flow starter in fastAPI with SQLAlchemy and Postgres

# How to Use
1. clone the repository
2. Set up `DATABASE_URL` environment variable in the format 'postgresql+psycopg2://<username>:<password>@<hostname>:<port>/<db-name>'
3. Run alembic migrations (`cd app && alembic upgrade head && cd ..`)
4. Create and activate virtualenv (`python3 -m venv venv && source venv/bin/activate`)
5. Install dependencies (`poetry install`)
6. Run the app (`python3 main.py`)

# Why
I just needed a quick starter template for setting up auth in my fastapi projects. The code here is mostly lifted from the wonderful [FastAPI Docs](https://fastapi.tiangolo.com/tutorial/security/first-steps/). I just refactored it a bit to suit my general project structure.

# Frameworks/Libraries
1. sqlalchemy 2.0 - ORM
2. uvicorn - ASGI server
3. alembic - Database Migrations
4. psycopg2 - Postgres DB Driver
5. python-jose - Handling JWT
6. passlib - Password hashing
7. poetry - Dependency management
