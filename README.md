Langlearn is a Flask-powered language tutor foundation that pairs user-driven chat with vectorized memory stored in PostgreSQL.

## Stack

- Backend: Flask (session + blueprint-based)
- Database: PostgreSQL (vector-friendly concept embeddings)
- Orchestration: `uv` for Python dependency management
- Logic: placeholders for LangGraph, LangChain, and Lagsmith agents to grow the conversational behaviors

## Getting started

1. Install dependencies via `uv install` or `uv sync`.
2. Copy `.env.example` to `.env` and set `DATABASE_URL` (Postgres + pgvector enabled) and `FLASK_SECRET_KEY`.
3. Initialize the database (`python -m app.db` will create tables).
4. Launch with `uv run flask run` or `uv run flask run` (after setting `FLASK_APP=app` and `FLASK_ENV=development`).

## Directory highlights

- `app/models.py`: Users, lessons, concepts, and vector embeddings.
- `app/routes.py`: Auth + chat experience (login/register + lesson-aware chat).
- `app/agents.py`: Skeleton functions for review/explain/correct/evaluate/create agents.
- `app/templates/*`: Responsive chat layout with lesson selector and gradient styling.
- `app/static/css/style.css`: Purposeful typography + tone for the interface.

## Review the db
- Run the command `psql -U postgres -d langlearn_db` inside of the docker container where the db is running.


This first iteration wires up the data models, auth flows, lesson selector, and chat surface; future commits should connect the LangGraph/LangChain agents and vector search behaviors.
