Langlearn is a Flask-powered language tutor foundation that pairs user-driven chat with vectorized memory stored in PostgreSQL.

## Stack

- Backend: Flask (session + blueprint-based)
- Database: PostgreSQL (vector-friendly concept embeddings)
- Orchestration: `uv` for Python dependency management
- Logic: placeholders for LangGraph, LangChain, and Lagsmith agents to grow the conversational behaviors

## Getting started

1. Install dependencies via `uv install` or `uv sync`.
2. Copy `.env.example` to `.env` and set `DATABASE_URL` (Postgres + pgvector enabled) and `FLASK_SECRET_KEY`.
3. Initialize the migrations scaffold (only once) and sync the schema:
   - set `FLASK_APP=app` and `FLASK_ENV=development`, then run `uv run flask db init` if a `migrations/` folder does not exist yet.
   - run `uv run flask db migrate -m "init"` to capture the base models, then `uv run flask db upgrade` to apply them.
4. Launch with `uv run flask run` (after ensuring `FLASK_APP=app` and `FLASK_ENV=development`).

## Directory highlights

- `app/models.py`: Users, lessons, concepts, and vector embeddings.
- `app/routes.py`: Auth + chat experience (login/register + lesson-aware chat).
- `app/agents.py`: Skeleton functions for review/explain/correct/evaluate/create agents.
- `app/templates/*`: Responsive chat layout with lesson selector and gradient styling.
- `app/static/css/style.css`: Purposeful typography + tone for the interface.

## Review the db
- Run the command `psql -U postgres -d langlearn_db` inside of the docker container where the db is running.

## Schema updates
- After editing `app/models.py`, set `FLASK_APP=app` and run `uv run flask db migrate -m "describe the change"` to generate a new Alembic revision.
- Apply the migration with `uv run flask db upgrade` to keep the PostgreSQL schema in sync with SQLAlchemy.
- If you have not already created the migrations folder, start with `uv run flask db init`; revisit `uv run flask db --help` for more commands.

## Create default db values
1. Run `uv run flask seed-db` to load the defaults
2. Inspect languages/levels (e.g., via psql or uv run flask shell) to confirm the records are
present.

This first iteration wires up the data models, auth flows, lesson selector, and chat surface; future commits should connect the LangGraph/LangChain agents and vector search behaviors.
