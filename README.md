# Posts API

A REST API for creating and managing posts. Built with FastAPI, SQLAlchemy, and PostgreSQL, it includes JWT authentication, ownership checks, voting, database migrations, automated tests, and Docker-based development and deployment configuration.

## Features

- Register users and authenticate with JWT bearer tokens.
- Create, read, update, and delete posts.
- Restrict post updates and deletion to the post owner.
- Search and paginate posts, with vote counts in post responses.
- Add or remove a vote on a post.
- Manage database schema changes with Alembic.
- Run tests with a separate PostgreSQL test database.

## Tech stack

- Python 3.9
- FastAPI and Uvicorn
- PostgreSQL and SQLAlchemy
- Alembic
- Pytest
- Docker and Docker Compose

## Getting started

### Prerequisites

- Docker and Docker Compose, or Python 3.9 and PostgreSQL.
- A PostgreSQL database for the application.

### Configure environment variables

Create a `.env` file in the project root. For Docker Compose, use `postgres` as the database hostname; when running the API directly on your machine, use the hostname where PostgreSQL is available, commonly `localhost`.

```dotenv
DATABASE_HOSTNAME=postgres
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PSW=change-this-password
DATABASE_NAME=posts

SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use a unique, securely generated `SECRET_KEY` outside local development. Do not commit `.env` or production credentials.

### Run with Docker Compose

```bash
docker compose up --build
```

The API is available at `http://localhost:8001`. The compose configuration starts PostgreSQL and the API; the API container listens on port `8000`. Apply the database migrations from another terminal:

```bash
docker compose exec api alembic upgrade head
```

To stop the services:

```bash
docker compose down
```

### Run locally

1. Create and activate a Python 3.9 virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure `.env` with a reachable PostgreSQL instance and create the database named by `DATABASE_NAME`.
4. Apply migrations and start the API:

   ```bash
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

The API is available at `http://localhost:8000`. Interactive API documentation is available at `/docs`; the alternative documentation UI is at `/redoc`.

## API overview

Unless noted otherwise, routes below require a bearer access token obtained from `POST /login`.

| Method | Path | Description | Authentication |
|---|---|---|---|
| `POST` | `/users/` | Register a user | No |
| `GET` | `/users/{id}` | Get a user by ID | No |
| `POST` | `/login` | Log in and receive an access token | No |
| `GET` | `/posts/` | List posts; supports `limit`, `skip`, and `search` query parameters | Yes |
| `POST` | `/posts/` | Create a post | Yes |
| `GET` | `/posts/{id}` | Get a post and its vote count | Yes |
| `PUT` | `/posts/{id}` | Update a post you own | Yes |
| `DELETE` | `/posts/{id}` | Delete a post you own | Yes |
| `POST` | `/vote/` | Add or remove your vote on a post | Yes |

Log in using form fields named `username` (your email address) and `password`. For voting, send JSON containing `post_id` and `dir`: use `1` to add a vote and `0` to remove it. A user can have at most one vote per post.

Example registration:

```bash
curl -X POST http://localhost:8001/users/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"user@example.com\",\"password\":\"your-password\"}"
```

Use port `8000` instead of `8001` when running the API directly rather than through Docker Compose.

## Database migrations

Apply existing migrations with:

```bash
alembic upgrade head
```

To create a migration after changing the SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the schema change"
```

Review generated migration files before applying them.

## Tests

Tests use a PostgreSQL database whose name is `DATABASE_NAME` with `_test` appended. Configure the test database and its connection settings before running:

```bash
pytest
```

The test fixtures drop and recreate database tables. **Never point the test configuration at a database containing data you need to keep.**

## Deployment

The repository includes a production-oriented Compose configuration in `docker-compose-prod.yml`, a Heroku `Procfile`, and Gunicorn/Nginx/systemd configuration files. The GitHub Actions workflow in `.github/workflows/build-deploy.yml` runs tests and contains deployment steps for Heroku and an Ubuntu server. Configure deployment credentials and environment variables as secrets in the relevant hosting and GitHub environments; do not store them in the repository.
