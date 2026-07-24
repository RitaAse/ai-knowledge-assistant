# AI Knowledge Assistant Deployment Guide

## 1. Overview

The AI Knowledge Assistant is deployed as a cloud-based application consisting of:

- FastAPI backend
- PostgreSQL database
- pgvector extension
- Streamlit frontend
- Cloud storage layer

The application separates frontend, backend, and infrastructure responsibilities to support independent deployment and future scaling.

---

# 2. Deployment Architecture

Current deployment architecture:

```mermaid
flowchart TD

    User[User]

    User --> Frontend[Streamlit Cloud]

    Frontend --> Backend[FastAPI Backend]

    Backend --> Database[(PostgreSQL + pgvector)]

    Backend --> Storage[Storage Layer]

    Storage --> Local[Local Storage]

    Storage --> Cloud[GCS Storage]
```

---

# 3. Deployment Components

## Frontend

Technology:

```
Streamlit
```

Deployment platform:

```
Streamlit Community Cloud
```

Responsibilities:

- User interface
- Document upload interface
- Chat interface
- Displaying answers and sources
- Communicating with backend API

---

## Backend

Technology:

```
FastAPI
```

Deployment platform:

```
Render
```

Responsibilities:

- API endpoints
- Document processing
- Retrieval pipeline
- LLM communication
- Database operations

---

## Database

Technology:

```
- Neon PostgreSQL
- pgvector
- SQLAlchemy ORM
- Alembic migrations
```

Responsibilities:

- Store document metadata
- Store processed chunks
- Store embeddings
- Support similarity search

---

# 4. Local Development Deployment

For local development, the application uses Docker Compose.

Architecture:

```text
Docker Compose

        |

        +----------------+

        |                |

   FastAPI          PostgreSQL

   Backend          + pgvector
```

---

# 5. Local Requirements

Required tools:

- Python 3.12+
- Docker Desktop
- Git

Recommended:

| Component | Version |
|---|---|
| Python | 3.12+ |
| PostgreSQL | 16 |
| Docker | Latest |

---

# 6. Environment Configuration

Environment variables are managed separately from source code.

Backend environment:

```
backend/.env
```

Template:

```
backend/.env.example
```

Example:

```env
APP_NAME=AI Knowledge Assistant API

API_VERSION=1.0.0

ENVIRONMENT=development


DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/ai_assistant


GROQ_API_KEY=your_key_here


STORAGE_PROVIDER=local


RETRIEVAL_TOP_K=5

SIMILARITY_THRESHOLD=0.7
```

Sensitive information should never be committed.

---

# 7. Backend Deployment

The backend runs as a web service.

Startup command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application exposes:

```
GET /
```

Health endpoint:

```
GET /health
```

API documentation:

```
/docs
```

---

# 8. Render Deployment

The backend is deployed using Render Web Services.

Deployment process:

```text
GitHub Repository

        |

        v

Render Build

        |

        v

Install Dependencies

        |

        v

Start FastAPI Application
```

---

## Required Render Configuration

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Environment Variables

Render stores production secrets separately.

Required variables:

```text
DATABASE_URL

GROQ_API_KEY

STORAGE_PROVIDER

ENVIRONMENT
```

---

# 9. Streamlit Deployment

The frontend is deployed using Streamlit Community Cloud.

Deployment workflow:

```text
GitHub Repository

        |

        v

Streamlit Cloud

        |

        v

Install Requirements

        |

        v

Launch Streamlit Application
```

---

## Streamlit Configuration

Required files:

```
frontend/

├── app.py

├── requirements.txt

└── config.py
```

---

## Backend Connection

The frontend communicates with the backend through:

```text
HTTP Requests

        |

        v

FastAPI API
```

The backend URL is configured through:

```env
API_URL=https://backend-url
```

---

# 10. Database Deployment

PostgreSQL stores:

- Documents
- Document chunks
- Embeddings

Database lifecycle:

```text
Database Created

        |

        v

Alembic Migrations Applied

        |

        v

Application Connects
```

---

# 11. Database Migrations

Schema changes use Alembic.

Apply migrations:

```bash
alembic upgrade head
```

Create migration:

```bash
alembic revision --autogenerate -m "description"
```

Migration status:

```bash
alembic current
```

---

# 12. Storage Deployment

The application supports multiple storage providers.

Architecture:

```text
BaseStorage

      |

+-------------+

|             |

Local       GCS

Storage     Storage
```

---

## Development

Current:

```
Local Storage
```

Used for:

- Testing
- Development
- Portfolio demonstration

---

## Production

Recommended:

```
Google Cloud Storage
```

Benefits:

- Persistent storage
- Better reliability
- Scalable file storage

---

# 13. Current Production Considerations

The current deployment is designed as a portfolio/demo application.

Current limitations:

## Authentication

Not yet implemented.

Future support:

- User accounts
- Document ownership
- Access control

---

## Multi-user Data Isolation

The current version stores documents globally.

Future version:

```text
User

 |

 +---- Documents

        |

        +---- Chunks
```

---

## Background Processing

Current:

```
FastAPI Background Tasks
```

Future:

```
API

 |

Message Queue

 |

Worker Processes
```

Possible technologies:

- Celery
- Redis Queue
- Cloud Tasks

---

# 14. Security Considerations

Production deployment should include:

## Secrets

Use:

- Environment variables
- Secret managers

Never commit:

- API keys
- Database credentials

---

## File Upload Security

Future improvements:

- File type validation
- File size limits
- Malware scanning

---

## API Protection

Future improvements:

- Authentication
- Authorization
- Rate limiting

---

# 15. Monitoring and Observability

Future production monitoring should include:

## Application Metrics

Examples:

- Request latency
- API errors
- Processing duration

---

## AI Metrics

Examples:

- Retrieval accuracy
- Answer quality
- Hallucination rate

---

## Infrastructure Metrics

Examples:

- CPU usage
- Memory usage
- Database performance

---

# 16. Deployment Summary

Current deployment:

```text
                    User

                      |

                      v

             Streamlit Cloud

                      |

                      v

              FastAPI Backend

                (Render)

                      |

        +-------------+-------------+

        |                           |

 PostgreSQL + pgvector        Storage Layer

                              |

                         Local / GCS
```

The current deployment provides a working cloud-hosted RAG application while maintaining a clear path toward production improvements such as authentication, scalable processing, and cloud-native infrastructure.