# Photophinder

An AI-powered personal photo search application with FastAPI, Celery background workers, PostgreSQL with pgvector, and a React + Vite frontend.

## Project structure
- `backend/`: FastAPI app, Celery worker, database models, migrations, and ML stubs.
- `frontend/`: React + TypeScript single-page app built with Vite.
- `docker-compose.yml`: Local development stack (backend API, worker, Postgres + pgvector, Redis, MinIO).

## Backend setup (local)
1. Create a virtual environment and install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Set environment variables as needed (defaults target the docker-compose services).
3. Run database migrations:
   ```bash
   alembic upgrade head
   ```
4. Start the API:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Start the Celery worker (in another shell):
   ```bash
   celery -A app.tasks.celery_app worker --loglevel=info
   ```

## Frontend setup (local)
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run the dev server:
   ```bash
   npm run dev
   ```
3. Configure env vars (optional) in a `.env` file with `VITE_API_BASE_URL` and `VITE_STORAGE_BASE`.

## Running with Docker Compose
```bash
# from repo root
STORAGE_BUCKET=photophinder docker-compose up --build
```
The stack starts the API on `http://localhost:8000`, Redis, Postgres with pgvector, and MinIO at `http://localhost:9000` (console at `:9001`).

## API highlights
- `POST /photos/upload`: upload an image, store resized variants, enqueue background indexing.
- `GET /search?query=...`: text-to-image semantic search (model stubs in place).
- `POST /faces/{face_id}/label`: label a detected face and propagate to similar unlabeled faces.

## Notes
- ML model loaders are stubbed; replace implementations in `backend/app/models/*.py` with real models for production use.
- Storage is abstracted through S3-compatible endpoints; swap MinIO for AWS S3 by updating env vars.
