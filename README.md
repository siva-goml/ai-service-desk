# AI Service Desk

An asynchronous REST API for creating, tracking, and resolving support tickets, with an AI-assisted ticket summarization feature powered by Amazon Bedrock.

## Features

- Full CRUD operations for support tickets (create, list, retrieve, update, delete)
- Business rule enforcement (e.g., closed tickets cannot be updated)
- AI-generated ticket summaries and suggested responses via Amazon Bedrock
- Async database access with SQLAlchemy and PostgreSQL
- Database schema versioning with Alembic
- Health and readiness endpoints for monitoring
- Automated unit and integration test suite
- Dockerized for containerized deployment

## Tech Stack

- **Language / Runtime:** Python (>=3.13)
- **Web Framework:** FastAPI, served by Uvicorn
- **Database:** PostgreSQL, accessed via SQLAlchemy (async) and asyncpg
- **Migrations:** Alembic
- **Validation / Config:** Pydantic and pydantic-settings
- **AI Integration:** Amazon Bedrock Runtime (Converse API) via boto3
- **Testing:** pytest, pytest-asyncio, httpx
- **Load Testing:** Locust
- **Containerization:** Docker

## Project Structure

```
app/
├── main.py                        # FastAPI app, middleware, health/ready endpoints
├── api/
│   ├── tickets.py                 # Ticket CRUD endpoints
│   └── ai.py                      # AI summarization endpoint
├── core/
│   ├── config.py                  # Application settings
│   └── deps.py                    # Database session dependency
├── db/
│   ├── database.py                # Async engine and session factory
│   └── base.py                    # Declarative base
├── models/
│   └── ticket.py                  # Ticket ORM model, Priority/Status enums
├── schemas/
│   └── ticket.py                  # Pydantic request/response schemas
├── repositories/
│   └── ticket_repository.py       # Database access layer
└── services/
    ├── ticket_service.py          # Ticket business logic
    └── aws_service/
        ├── bedrock.py             # Amazon Bedrock service wrapper
        └── prompt_templates.py    # Summarization prompt templates

alembic/                           # Database migration environment and scripts
tests/
├── unit/                          # Schema validation tests
└── integration/                   # End-to-end API tests

locust.py                          # Load testing scenario
profile_test.py                    # cProfile-based performance profiling script
Dockerfile                         # Container image definition
```

## Prerequisites

- Python 3.13+
- PostgreSQL database
- AWS credentials with access to Amazon Bedrock (for the AI summarization feature)

## Installation

1. Clone the repository and navigate into the project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application reads configuration from environment variables (or a `.env` file). The following variables are required:

| Variable | Description |
|---|---|
| `DEBUG` | Debug flag |
| `DATABASE_URL` | SQLAlchemy async database connection string |
| `SECRET_KEY` | Application secret key |
| `AWS_ACCESS_KEY_ID` | AWS credential for the Bedrock client |
| `AWS_SECRET_ACCESS_KEY` | AWS credential for the Bedrock client |
| `AWS_REGION` | AWS region for the Bedrock client |
| `BEDROCK_MODEL_ID` | Bedrock model ID used for ticket summarization |
| `AWS_DEMO_MODE` | Demo mode flag |
| `DATABASE_READY` | Database readiness flag |

Optional settings with defaults: `APP_NAME`, `API_VERSION`, `ACCESS_TOKEN_EXPIRE_MINUTES`.

## Database Setup

Apply migrations before starting the application:

```bash
alembic upgrade head
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Running Tests

```bash
pytest
```

## Load Testing

```bash
locust -f locust.py
```

## API Overview

| Endpoint | Method | Description |
|---|---|---|
| `/tickets/` | POST | Create a new ticket |
| `/tickets/` | GET | List all tickets |
| `/tickets/{ticket_id}` | GET | Retrieve a ticket by ID |
| `/tickets/{ticket_id}` | PUT | Update a ticket |
| `/tickets/{ticket_id}` | DELETE | Delete a ticket |
| `/ai/summarize` | POST | Generate an AI summary and suggested response for a ticket |
| `/health` | GET | Liveness check |
| `/ready` | GET | Readiness check (verifies database connectivity) |

Interactive API documentation is available at `/docs` (Swagger UI) once the application is running.

## Docker

Build and run the containerized application:

```bash
docker build -t ai-service-desk .
docker run -p 8000:8000 --env-file .env ai-service-desk
```

The container exposes port `8000` and includes a health check against the `/health` endpoint.