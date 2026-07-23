# AI Knowledge Assistant

## A Production-Ready RAG-Based Document Question Answering System

The AI Knowledge Assistant is a Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask natural language questions.

The system combines:

- Document processing
- Semantic search
- Vector embeddings
- Retrieval-Augmented Generation
- Large Language Models (LLMs)

to generate accurate answers grounded in uploaded documents.

The goal of this project is to build an intelligent knowledge retrieval system that helps users quickly access information from internal documentation such as:

- Company policies
- Technical manuals
- Onboarding documents
- Internal guidelines
- Knowledge bases

---

# Project Overview

Traditional document search relies on keyword matching, making it difficult to find relevant information when users do not know the exact wording.

This project solves this problem by using semantic search.

Instead of searching for exact keywords, the system understands the meaning behind a question and retrieves the most relevant document sections before generating an answer.

Example:

```
User Question:

"What operating system is recommended?"

        |

Question Embedding

        |

Vector Similarity Search

        |

Relevant Document Chunks

        |

LLM Answer Generation

        |

Answer + Sources
```

---

# Key Features

## Document Management

Users can:

- Upload PDF documents
- Store documents using configurable storage providers
- Retrieve uploaded files
- Delete documents
- Track document processing status

---

## Automated Document Processing

Uploaded documents are processed asynchronously.

The pipeline includes:

- PDF text extraction
- Text chunking
- Embedding generation
- Vector storage

Workflow:

```
PDF Upload

    |

Text Extraction

    |

Chunk Creation

    |

Embedding Generation

    |

Vector Database Storage
```

---

## Semantic Search

The system uses vector embeddings to find relevant information.

Instead of traditional keyword search:

```
keyword matching
```

the system performs:

```
meaning-based similarity search
```

using:

- Sentence Transformers
- PostgreSQL pgvector
- Cosine similarity search

---

## Retrieval-Augmented Generation (RAG)

The answer generation pipeline follows:

```
User Question

        |

Retrieve Relevant Chunks

        |

Build Context

        |

Send Context + Question to LLM

        |

Generate Grounded Response

        |

Return Answer + Sources
```

The system is designed to reduce hallucination by instructing the LLM to only use retrieved document information.

---

## Source References

Responses include supporting document information:

Example:

```json
{
  "answer": "The recommended operating system is Linux.",
  "sources": [
    {
      "document": "technical_manual.pdf",
      "page": 4,
      "relevance": 92
    }
  ]
}
```

---

# System Architecture

```mermaid
flowchart TD

    User[User]

    User --> Frontend[Streamlit Frontend]

    Frontend --> API[FastAPI Backend]

    API --> Upload[Document Upload]

    API --> Search[Question Search]


    Upload --> Storage[Storage Layer]

    Storage --> Local[Local Storage]

    Storage --> Cloud[Google Cloud Storage]


    Upload --> Processor[Document Processing]


    Processor --> Extract[PDF Extraction]

    Extract --> Chunk[Text Chunking]

    Chunk --> Embedding[Embedding Generation]

    Embedding --> Database[(PostgreSQL + pgvector)]


    Search --> Retrieval[Similarity Retrieval]

    Retrieval --> Database

    Retrieval --> LLM[Large Language Model]

    LLM --> Response[Answer + Sources]
```

---

# Application Architecture

The backend follows a modular layered architecture:

```
                API Layer
                    |
                    |
             Service Layer
                    |
                    |
          Repository / Data Access
                    |
                    |
       Database + External Services
```

Main components:

## FastAPI Backend

Responsible for:

- API endpoints
- Request validation
- Application coordination


## Document Processing Service

Responsible for:

- PDF processing
- Chunk creation
- Embedding generation
- Processing status updates


## Retrieval Service

Responsible for:

- Question embedding generation
- Similarity search
- Relevant chunk retrieval


## RAG Service

Responsible for:

- Context construction
- Prompt creation
- LLM response generation
- Source formatting


## Storage Layer

Uses an abstraction layer:

```
BaseStorage

      |

+-------------+
|             |

LocalStorage  GCSStorage
```

This allows storage providers to change without modifying business logic.

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic Settings
- Uvicorn

## AI / Machine Learning

- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- Groq LLM API

## Database

- PostgreSQL
- pgvector

## Frontend

- Streamlit

## Infrastructure

- Docker
- Docker Compose

## Testing

- Pytest
- FastAPI TestClient

---

# Project Structure

The repository is organized into separate backend, frontend, and documentation components.

```text
ai-knowledge-assistant/

├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── tests/
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── docs/
│   ├── architecture.md
│   ├── api_design.md
│   ├── database_design.md
│   ├── deployment.md
│   ├── decisions.md
│   └── system_design.md
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# Local Installation

## Prerequisites

Before running the application, install:

- Python 3.12+
- Docker Desktop
- Git

---

# 1. Clone Repository

```bash
git clone https://github.com/your-username/ai-knowledge-assistant.git

cd ai-knowledge-assistant
```

---

# 2. Configure Environment Variables

Create a backend environment file:

```text
backend/.env
```

Example:

```env
APP_NAME=AI Knowledge Assistant API
API_VERSION=1.0.0
ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/ai_assistant

GROQ_API_KEY=your_api_key_here

STORAGE_PROVIDER=local

RETRIEVAL_TOP_K=5
SIMILARITY_THRESHOLD=0.7
```

A template is available:

```text
backend/.env.example
```

Sensitive information such as API keys should never be committed.

---

# Running the Application

The recommended development setup uses Docker Compose.

## Start Backend and Database

From the project root:

```bash
docker compose up --build
```

This starts:

```
FastAPI Backend

        +

PostgreSQL Database
with pgvector
```

---

# Backend API

The backend runs on:

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

FastAPI automatically generates Swagger documentation.

---

# Frontend Application

The frontend is built with Streamlit.

Navigate to:

```bash
cd frontend
```

Activate the frontend environment:

```bash
venv\Scripts\activate
```

Run Streamlit:

```bash
streamlit run app.py
```

The frontend will open in the browser.

---

# API Endpoints

## Upload Document

### Request

```
POST /documents/upload
```

Uploads a PDF document and starts background processing.

---

## Retrieve Documents

### Request

```
GET /documents
```

Returns uploaded documents and processing status.

---

## Retrieve Document Metadata

### Request

```
GET /documents/{document_id}
```

Returns information about a specific document.

---

## Download Original File

### Request

```
GET /documents/{document_id}/file
```

Retrieves the original uploaded document.

---

## Delete Document

### Request

```
DELETE /documents/{document_id}
```

Deletes:

- Database record
- Stored document file

---

## Ask Questions

### Request

```
POST /documents/search
```

Example:

```json
{
    "question": "What operating system is recommended?"
}
```

Response:

```json
{
    "answer": "Linux is the recommended operating system.",
    "sources": [
        {
            "document": "manual.pdf",
            "page": 4,
            "relevance": 92,
            "preview": "..."
        }
    ]
}
```

---

# Running Tests

Automated tests are included using Pytest.

Run tests inside the backend container:

```bash
docker exec -it ai_assistant_backend pytest
```

Current tests cover:

- Health endpoint
- Document upload workflow
- RAG search response structure

Example output:

```
========================

3 passed

========================
```

---

# Database Migrations

Database schema changes are managed using Alembic.

Apply migrations:

```bash
alembic upgrade head
```

Create a migration:

```bash
alembic revision --autogenerate -m "description"
```

---

# Documentation

Additional technical documentation is available in:

```
docs/
```

Including:

| Document | Description |
|---|---|
| architecture.md | System architecture overview |
| api_design.md | API structure and endpoints |
| database_design.md | Database schema and relationships |
| deployment.md | Deployment and setup guide |
| decisions.md | Architecture decisions and trade-offs |
| system_design.md | Interview-style system design explanation |

---

# Future Improvements

Potential future enhancements include:

## Authentication and Authorization

- User accounts
- Role-based permissions
- Document ownership

---

## Scalable Processing Pipeline

Replace FastAPI background tasks with:

- Celery
- Redis Queue
- Cloud task workers

for reliable large-scale processing.

---

## Advanced Document Support

Add support for:

- Word documents
- PowerPoint files
- Markdown files
- Web pages

---

## Production Infrastructure

Future deployment options:

- Kubernetes
- Cloud Run
- AWS ECS
- Azure Container Apps

---

## RAG Evaluation

Add automated evaluation for:

- Retrieval accuracy
- Answer relevance
- Hallucination detection

---

# Project Status

Current implementation includes:

✅ Document upload  
✅ Background document processing  
✅ PDF text extraction  
✅ Text chunking  
✅ Embedding generation  
✅ PostgreSQL vector storage  
✅ Semantic retrieval  
✅ LLM-based answer generation  
✅ Source references  
✅ Docker development environment  
✅ Automated tests  

---

# License

This project is currently developed as a portfolio and engineering project.