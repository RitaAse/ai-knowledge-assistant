# AI Knowledge Assistant Deployment Guide

## 1. Overview

The AI Knowledge Assistant is designed to run as a containerized application using Docker.

The deployment setup separates application components:

- FastAPI backend
- PostgreSQL database
- pgvector extension
- Streamlit frontend

Docker Compose is used to manage local development services.

---

# 2. Deployment Architecture

```mermaid
flowchart TD

    User[User]

    User --> Frontend[Streamlit Frontend]

    Frontend --> Backend[FastAPI Backend]

    Backend --> Database[(PostgreSQL + pgvector)]

    Backend --> Storage[Storage Layer]

    Storage --> Local[Local File Storage]

    Storage --> GCS[Google Cloud Storage]
```

---

# 3. Local Development Environment

The application requires:

- Python
- Docker Desktop
- PostgreSQL
- Git

Recommended versions:

| Component | Version |
|---|---|
| Python | 3.12+ |
| PostgreSQL | 16 |
| Docker | Latest |
| FastAPI | Latest |

---

# 4. Repository Structure

```text
ai-knowledge-assistant

├── backend
│   ├── app
│   ├── tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic
│
├── frontend
│   ├── app.py
│   ├── requirements.txt
│   └── venv
│
├── docker-compose.yml
│
└── docs
```

---

# 5. Environment Configuration

The application uses environment variables for configuration.

Environment variables are stored locally in:

```text
backend/.env
```

A template is provided:

```text
backend/.env.example
```

Example configuration:

```env
APP_NAME=AI Knowledge Assistant API
API_VERSION=1.0.0
ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/ai_assistant

STORAGE_PROVIDER=local

RETRIEVAL_TOP_K=5
SIMILARITY_THRESHOLD=0.7
```

Sensitive values such as API keys are not committed to Git.

---

# 6. Docker Deployment

The backend and database services are managed using Docker Compose.

Start services:

```bash
docker compose up --build
```

This starts:

```text
FastAPI Backend
        |
        |
PostgreSQL + pgvector
```

Stop services:

```bash
docker compose down
```

---

# 7. Backend Container

The backend container runs the FastAPI application.

Responsibilities:

- Handle API requests
- Process documents
- Generate embeddings
- Perform retrieval
- Generate answers

The application starts using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API documentation is available through:

```text
http://localhost:8000/docs
```

---

# 8. Database Deployment

PostgreSQL runs as a Docker service.

The database provides:

- Relational storage
- Document metadata storage
- Vector storage through pgvector

Database initialization:

```text
Docker Container Starts

        |

PostgreSQL Available

        |

Alembic Migrations Applied

        |

Application Connects
```

---

# 9. Database Migrations

Schema changes are managed using Alembic.

Create a migration:

```bash
alembic revision --autogenerate -m "migration description"
```

Apply migrations:

```bash
alembic upgrade head
```

Check current migration:

```bash
alembic current
```

---

# 10. Running Tests

Automated tests are executed inside the backend container.

Run:

```bash
docker exec -it ai_assistant_backend pytest
```

The test suite covers:

- Health endpoints
- Document upload workflow
- RAG search response structure

Example successful output:

```text
3 passed
```

---

# 11. Frontend Deployment

The frontend is built using Streamlit.

Local startup:

```bash
streamlit run app.py
```

The frontend communicates with the FastAPI backend through HTTP requests.

Architecture:

```text
Streamlit UI

      |

HTTP Requests

      |

FastAPI API
```

---

# 12. Production Deployment Considerations

For production deployment, the following improvements are recommended:

## Authentication

Add:

- User accounts
- Role-based permissions
- Document ownership

---

## Background Processing

Replace FastAPI background tasks with a dedicated task queue:

Examples:

- Celery
- Redis Queue
- Cloud Tasks

Benefits:

- Reliable processing
- Retry support
- Better scalability

---

## Cloud Storage

Move uploaded documents from local storage to:

- Google Cloud Storage
- Amazon S3
- Azure Blob Storage

---

## Monitoring

Add:

- Application metrics
- Error tracking
- Logging dashboards
- Performance monitoring

---

## Container Orchestration

For larger deployments:

- Kubernetes
- Cloud Run
- ECS
- Azure Container Apps

---

# 13. Security Considerations

Production deployment should include:

- Secret management
- API authentication
- Input validation
- File upload restrictions
- Network security
- Database access controls

---

# 14. Deployment Summary

Current deployment approach:

```text
Docker Compose

    |

    +----------------+
    |                |
FastAPI        PostgreSQL
Backend        + pgvector

    |

Streamlit Frontend
```

The current setup provides a reproducible development environment while keeping the architecture ready for future cloud deployment.