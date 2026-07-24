# AI Knowledge Assistant - End-to-End RAG Application

> A production-ready Retrieval-Augmented Generation (RAG) application for intelligent document question answering using semantic search, vector embeddings, and Large Language Models.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791)
![RAG](https://img.shields.io/badge/AI-RAG-purple)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![License](https://img.shields.io/badge/License-Portfolio-lightgrey)

---

# Table of Contents

- [Project Overview](#project-overview)
- [Live Demo](#live-demo)
- [System Architecture](#system-architecture)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Application Architecture](#application-architecture)
- [Repository Structure](#repository-structure)
- [Local Development Setup](#local-development-setup)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Database Migrations](#database-migrations)
- [Deployment Architecture](#deployment-architecture)
- [Current Production Limitations](#current-production-limitations)
- [Future Improvements](#future-improvements)
- [Project Status](#project-status)
- [License](#license)

---

# Project Overview

The **AI Knowledge Assistant** is a Retrieval-Augmented Generation (RAG) application that transforms unstructured documents into an intelligent, searchable knowledge base.

Users can upload PDF documents, ask natural language questions, and receive AI-generated answers grounded in the uploaded content.

Unlike traditional keyword search, the application performs **semantic retrieval**, enabling it to understand the meaning behind a user's question before generating an answer.

The system combines:

- Document processing
- Semantic search
- Vector embeddings
- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Cloud deployment architecture

Typical use cases include:

- Company policies
- Technical documentation
- Knowledge bases
- Internal guidelines
- Employee onboarding documents
- Training materials

---

# Screenshots

## Home Page
The Streamlit interface provides document management and AI-powered question answering.

![Home](docs/images/homepage.png)

## Upload Documents
Users can upload PDF documents which are processed through the RAG pipeline.

![Upload](docs/images/upload.png)



## Document Proceesing Status
![Processing](docs/images/processing.png)
![Ready](docs/images/ready.png)

## Ask Questions

![Search](docs/images/search.png)

---

# Demo GIF
![Demo](docs/images/rag-demo-gif.gif)

- Upload a PDF
- Wait for processing
- Ask a question
- Receive an answer with sources

# Live Demo

## Frontend

Streamlit application:

```text
https://ai-knowledge-assistant-cgakggkjibixqea8dt8bzw.streamlit.app/
```

## Backend API

FastAPI backend:

```text
https://ai-knowledge-assistant-nu4e.onrender.com
```

Interactive Swagger documentation:

```text
https://ai-knowledge-assistant-nu4e.onrender.com/docs
```

---

# How It Works

Instead of searching for exact keywords, the system retrieves document sections that are **semantically similar** to the user's question before asking the language model to generate a response.

```text
User Question

"What operating system is recommended?"

        │

Question Embedding

        │

Vector Similarity Search

        │

Relevant Document Chunks

        │

LLM Answer Generation

        │

Answer + Source References
```

This retrieval-first approach helps reduce hallucinations by grounding responses in the uploaded documents.

---

# System Architecture

The application follows a separated frontend/backend architecture deployed in the cloud.

```mermaid
flowchart TD

    User[User]

    User --> Frontend[Streamlit Community Cloud]

    Frontend --> Backend[FastAPI Backend - Render]

    Backend --> Database[(PostgreSQL + pgvector)]

    Backend --> Storage[Google Cloud Storage]

    Backend --> Retrieval[Semantic Retrieval]

    Retrieval --> LLM[Groq LLM]

    LLM --> Response[Answer + Sources]
```

---

# Key Features

## Document Management

Users can:

- Upload PDF documents
- View document processing status
- Retrieve uploaded documents
- Download original files
- Delete uploaded documents

---

## Automated Document Processing

Documents are processed asynchronously after upload.

Processing pipeline:

```text
PDF Upload

      │

Text Extraction

      │

Text Chunking

      │

Embedding Generation

      │

Vector Storage

      │

Ready for Retrieval
```

Document lifecycle:

```text
UPLOADED

    │

PROCESSING

    │

COMPLETED
```

If processing fails:

```text
PROCESSING

    │

FAILED
```

---

## Semantic Search

Traditional search relies on keyword matching.

```text
keyword matching
```

The AI Knowledge Assistant instead performs:

```text
meaning-based similarity search
```

using:

- Sentence Transformers
- PostgreSQL pgvector
- Cosine similarity retrieval

---

## Retrieval-Augmented Generation (RAG)

The answer generation workflow follows:

```text
User Question

        │

Generate Question Embedding

        │

Retrieve Similar Document Chunks

        │

Build Context

        │

Send Context + Question to LLM

        │

Generate Grounded Answer

        │

Return Answer + Sources
```

The language model only receives retrieved document context, significantly reducing hallucinations compared to standalone prompting.

---

## Source References

Every generated answer includes supporting evidence from the uploaded documents.

Example response:

```json
{
  "answer": "The recommended operating system is Ubuntu Linux.",
  "sources": [
    {
      "document": "technical_manual.pdf",
      "page": 4,
      "relevance": 92,
      "preview": "The application is supported on Ubuntu Linux..."
    }
  ]
}
```

Providing source references improves transparency by allowing users to verify where each answer originated.

---

# Technology Stack

The project is built using a modern AI engineering stack designed for scalable Retrieval-Augmented Generation (RAG) applications.

| Layer | Technologies |
|--------|--------------|
| **Backend** | Python, FastAPI, SQLAlchemy, Pydantic Settings, Uvicorn |
| **AI / Machine Learning** | Retrieval-Augmented Generation (RAG), Sentence Transformers (`all-MiniLM-L6-v2`), Groq LLM API |
| **Database** | PostgreSQL, pgvector |
| **Frontend** | Streamlit |
| **Storage** | Local Storage, Google Cloud Storage |
| **Infrastructure** | Docker, Docker Compose, Render, Streamlit Community Cloud |

---

# Application Architecture

The backend follows a modular layered architecture that separates business logic, API endpoints, database access, and external integrations.

```text
                API Layer

                    │

             Service Layer

                    │

          Data Access Layer

                    │

      Database + External Services
```

Each layer has a single responsibility, making the application easier to maintain, extend, and test.

---

## FastAPI Backend

The FastAPI application acts as the central orchestration layer.

Responsibilities include:

- API endpoint definitions
- Request validation
- Response serialization
- Document operations
- Background processing coordination
- AI service integration
- Error handling

---

## Document Processing Service

Responsible for transforming uploaded PDF documents into searchable knowledge.

Processing includes:

- PDF text extraction
- Text cleaning
- Chunk generation
- Embedding creation
- Vector database storage
- Processing status updates

Workflow:

```text
PDF Upload

      │

Extract Text

      │

Split Into Chunks

      │

Generate Embeddings

      │

Store in pgvector
```

---

## Retrieval Service

The retrieval service performs semantic search against the vector database.

Responsibilities:

- Generate question embeddings
- Perform cosine similarity search
- Rank document chunks
- Return the most relevant context

This allows the system to retrieve information based on meaning rather than exact wording.

---

## RAG Service

The Retrieval-Augmented Generation service prepares prompts for the language model.

Responsibilities:

- Build contextual prompts
- Combine retrieved chunks
- Communicate with the Groq API
- Generate grounded answers
- Format source references

The service ensures that responses remain closely aligned with the retrieved document context.

---

## Storage Layer

Document storage is abstracted behind a common interface.

```text
BaseStorage

      │

+----------------------+
|                      |

LocalStorage     GCSStorage
```

This abstraction allows storage providers to be replaced without modifying application logic.

Current implementations include:

- Local filesystem storage
- Google Cloud Storage (GCS)

Future storage providers can be added with minimal code changes.

---

# Repository Structure

The repository is organized into backend, frontend, infrastructure, and documentation components.

```text
ai-knowledge-assistant/

├── backend/
│
│   ├── app/
│   │
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── middleware/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   │
│   ├── tests/
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│
│   ├── app.py
│   ├── api/
│   ├── components/
│   └── requirements.txt
│
├── docs/
│
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

## Backend Directory

The backend contains the FastAPI application and supporting services.

| Directory | Purpose |
|-----------|---------|
| `api/` | API configuration and dependencies |
| `core/` | Application configuration and settings |
| `db/` | Database connection and session management |
| `middleware/` | Custom middleware |
| `models/` | SQLAlchemy database models |
| `routers/` | API endpoint definitions |
| `schemas/` | Pydantic request and response models |
| `services/` | Business logic, document processing, retrieval, and AI integration |
| `tests/` | Automated unit and integration tests |

---

## Frontend Directory

The Streamlit frontend provides an intuitive interface for interacting with the backend.

Components include:

- Document upload interface
- Processing status display
- Question-answer interface
- Source reference display
- API client utilities

---

## Documentation

The `docs/` directory contains detailed technical documentation beyond this README.

Recommended documents include:

| Document | Description |
|----------|-------------|
| `architecture.md` | High-level system architecture |
| `system_design.md` | End-to-end system design walkthrough |
| `database_design.md` | Database schema and relationships |
| `api_design.md` | API design and endpoint documentation |
| `deployment.md` | Production deployment guide |
| `decisions.md` | Architecture decisions and trade-offs |

These documents provide additional implementation details and design rationale.

---

# Local Development Setup

The project is designed for local development using **Docker Compose** for backend services and a Python virtual environment for the Streamlit frontend.

---

## Prerequisites

Before running the application, ensure the following tools are installed:

- Python **3.12+**
- Docker Desktop
- Git

You should also have a valid **Groq API Key** for LLM inference.

---

# 1. Clone the Repository

Clone the repository from GitHub:

```bash
git clone https://github.com/<username>/ai-knowledge-assistant.git

cd ai-knowledge-assistant
```

Replace `<username>` with your GitHub username.

---

# 2. Configure Environment Variables

Create an environment configuration file inside the backend directory.

```text
backend/.env
```

Example configuration:

```env
APP_NAME=AI Knowledge Assistant API
API_VERSION=1.0.0
ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/ai_assistant

GROQ_API_KEY=your_groq_api_key

STORAGE_PROVIDER=local

RETRIEVAL_TOP_K=5
SIMILARITY_THRESHOLD=0.7
```

If available, copy the template:

```bash
cp backend/.env.example backend/.env
```

Update the required values before starting the application.

> **Important**
>
> Never commit API keys, credentials, or secrets to version control.

---

# 3. Start the Backend Infrastructure

From the project root, start the backend services using Docker Compose.

```bash
docker compose up --build
```

This command builds and starts:

```text
FastAPI Backend

        +

PostgreSQL Database
with pgvector
```

The first build may take several minutes depending on your internet connection.

---

## Backend API

After the containers have started successfully, the FastAPI server will be available at:

```text
http://localhost:8000
```

Interactive Swagger documentation:

```text
http://localhost:8000/docs
```

Alternative ReDoc documentation:

```text
http://localhost:8000/redoc
```

FastAPI automatically generates interactive API documentation from the application's OpenAPI schema.

---

# 4. Start the Frontend

Navigate to the frontend directory.

```bash
cd frontend
```

Create a virtual environment.

**Windows**

```bash
python -m venv venv
```

Activate the environment.

**Windows (PowerShell)**

```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**

```cmd
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the Streamlit application.

```bash
streamlit run app.py
```

The frontend will automatically open in your default web browser.

If it does not, navigate to:

```text
http://localhost:8501
```

---

# Running the Application

After both services are running, the workflow is straightforward.

```text
Upload PDF

      │

Background Processing

      │

Embedding Generation

      │

Vector Database Storage

      │

Ask Questions

      │

Retrieve Relevant Chunks

      │

LLM Generates Answer

      │

Answer + Source References
```

---

# Configuration

Several application settings can be customized through environment variables.

| Variable | Description |
|-----------|-------------|
| `APP_NAME` | FastAPI application name |
| `API_VERSION` | API version |
| `DATABASE_URL` | PostgreSQL connection string |
| `GROQ_API_KEY` | API key for Groq LLM |
| `STORAGE_PROVIDER` | Storage backend (`local` or `gcs`) |
| `RETRIEVAL_TOP_K` | Number of document chunks retrieved |
| `SIMILARITY_THRESHOLD` | Minimum similarity score for retrieval |

These settings allow the application to be configured without modifying source code.

---

# Storage Providers

The application supports interchangeable storage backends through a storage abstraction layer.

Current implementations include:

- Local filesystem storage
- Google Cloud Storage (GCS)

Switching providers only requires updating the configuration:

```env
STORAGE_PROVIDER=local
```

or

```env
STORAGE_PROVIDER=gcs
```

No application code changes are required.

---

# Development Workflow

A typical development workflow is:

1. Start Docker services.
2. Upload one or more PDF documents.
3. Wait for document processing to complete.
4. Ask natural language questions.
5. Review generated answers and supporting sources.
6. Make code changes as needed.
7. Restart affected services when required.

This workflow closely mirrors the production deployment architecture, making it easier to transition between development and deployment environments.

---

# API Endpoints

The backend exposes a RESTful API for document management and Retrieval-Augmented Generation (RAG).

Once the backend is running, interactive API documentation is available at:

```text
http://localhost:8000/docs
```

The OpenAPI specification is automatically generated by FastAPI.

---

## Upload Document

Uploads a PDF document and starts the asynchronous processing pipeline.

### Endpoint

```http
POST /documents/upload
```

### Content Type

```text
multipart/form-data
```

### Request

| Field | Type | Description |
|--------|------|-------------|
| `file` | PDF | Document to upload |

### Response

```json
{
  "id": "2c8f6f87-5e72-4c75-b9f3-9f2f9afbbd28",
  "filename": "technical_manual.pdf",
  "status": "UPLOADED"
}
```

Processing begins immediately after upload.

---

## Retrieve Documents

Returns all uploaded documents and their processing status.

### Endpoint

```http
GET /documents
```

### Response

```json
[
  {
    "id": "2c8f6f87-5e72-4c75-b9f3-9f2f9afbbd28",
    "filename": "technical_manual.pdf",
    "status": "COMPLETED"
  }
]
```

---

## Retrieve Document Metadata

Returns metadata for a specific uploaded document.

### Endpoint

```http
GET /documents/{document_id}
```

### Path Parameters

| Parameter | Description |
|-----------|-------------|
| `document_id` | Unique document identifier |

### Example Response

```json
{
  "id": "2c8f6f87-5e72-4c75-b9f3-9f2f9afbbd28",
  "filename": "technical_manual.pdf",
  "status": "COMPLETED",
  "uploaded_at": "2026-07-20T10:42:15Z"
}
```

---

## Download Original Document

Downloads the original uploaded PDF.

### Endpoint

```http
GET /documents/{document_id}/file
```

### Response

Returns the original PDF file.

---

## Delete Document

Deletes both the uploaded file and its associated database records.

### Endpoint

```http
DELETE /documents/{document_id}
```

### Deletes

- Stored PDF document
- Vector embeddings
- Database metadata

### Example Response

```json
{
  "message": "Document deleted successfully."
}
```

---

## Ask Questions

Queries the uploaded knowledge base using Retrieval-Augmented Generation.

### Endpoint

```http
POST /documents/search
```

### Request Body

```json
{
  "question": "What operating system is recommended?"
}
```

---

### Retrieval Workflow

```text
User Question

        │

Generate Question Embedding

        │

Similarity Search

        │

Retrieve Relevant Chunks

        │

Construct Context

        │

Generate LLM Response

        │

Return Answer + Sources
```

---

### Example Response

```json
{
  "answer": "Ubuntu Linux is the recommended operating system.",
  "sources": [
    {
      "document": "technical_manual.pdf",
      "page": 4,
      "relevance": 92,
      "preview": "The application is supported on Ubuntu Linux..."
    }
  ]
}
```

Each response includes supporting document references to improve transparency and traceability.

---

# Testing

Automated tests are implemented using:

- Pytest
- FastAPI TestClient

Current test coverage includes:

- Health endpoint
- Document upload workflow
- PDF processing
- Retrieval endpoint
- RAG response structure

---

## Running Tests

If running inside Docker:

```bash
docker exec -it ai_assistant_backend pytest
```

Or locally:

```bash
pytest
```

Example output:

```text
=============================

5 passed

=============================
```

As additional features are implemented, test coverage can be expanded to include integration, performance, and end-to-end testing.

---

# Database Migrations

Database schema changes are managed using Alembic.

Create a migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback one migration:

```bash
alembic downgrade -1
```

Keeping schema changes under version control ensures consistent deployments across development and production environments.

---

# Deployment Architecture

The application is designed using a cloud-native deployment architecture.

```text
                     GitHub Repository

                             │

               ┌─────────────┴─────────────┐

               │                           │

        Streamlit Community          Render

             Frontend               FastAPI Backend

                                           │

                                  PostgreSQL + pgvector

                                           │

                               Google Cloud Storage
```

---

## Production Components

| Component | Service |
|-----------|---------|
| Frontend | Streamlit Community Cloud |
| Backend | Render |
| Database | PostgreSQL with pgvector |
| File Storage | Google Cloud Storage |
| LLM Provider | Groq API |

This architecture separates presentation, application logic, persistence, and AI services, making the system easier to scale and maintain.

---

# Current Production Limitations

The current implementation is intended as a **portfolio demonstration** of a modern Retrieval-Augmented Generation (RAG) application and follows a **single-tenant architecture**.

Current limitations include:

- No user authentication
- No authorization or role management
- Documents are shared across the application instance
- No user-specific document isolation
- Background processing uses FastAPI background tasks rather than a distributed task queue

To reduce risk during demonstrations, uploaded documents can be deleted directly through the application.

---

# Future Improvements

The project has been intentionally designed with extensibility in mind. Several production-oriented enhancements can be implemented with minimal architectural changes.

---

## Authentication & Authorization

Introduce a secure multi-user architecture with:

- User registration
- Login and authentication
- JWT-based authorization
- User-owned documents
- Role-based access control (RBAC)
- Tenant isolation

---

## Scalable Processing Pipeline

Replace FastAPI background tasks with a distributed processing system.

Potential technologies:

- Celery
- Redis Queue (RQ)
- RabbitMQ
- Google Cloud Tasks

Benefits include:

- Retry mechanisms
- Improved reliability
- Parallel document processing
- Horizontal scalability

---

## Expanded Document Support

Extend document ingestion beyond PDF files.

Potential formats include:

- Microsoft Word (`.docx`)
- Microsoft PowerPoint (`.pptx`)
- Markdown (`.md`)
- Plain text (`.txt`)
- HTML
- Web pages
- CSV files

---

## Advanced Retrieval

Improve retrieval quality through more advanced techniques.

Potential enhancements:

- Hybrid search (vector + keyword)
- Metadata filtering
- Parent-child chunk retrieval
- Query expansion
- Multi-query retrieval
- Cross-encoder reranking

---

## Improved RAG Evaluation

Introduce automated evaluation pipelines for measuring retrieval and generation quality.

Metrics may include:

- Retrieval precision
- Recall
- Context relevance
- Answer faithfulness
- Hallucination detection
- Answer completeness

Benchmark datasets can also be incorporated for repeatable evaluation.

---

## Production Monitoring

Add observability across the application stack.

Potential additions:

- Structured logging
- Metrics dashboards
- Error tracking
- Performance monitoring
- Request tracing
- Health dashboards

Recommended tools include:

- Prometheus
- Grafana
- OpenTelemetry
- Sentry

---

## CI/CD Pipeline

Automate testing and deployment.

Potential workflow:

```text
GitHub Push

      │

Run Tests

      │

Build Docker Images

      │

Deploy Backend

      │

Deploy Frontend

      │

Production
```

This enables reliable deployments and continuous integration.

---

# Project Status

The current implementation includes the following completed features:

### Backend

- ✅ FastAPI REST API
- ✅ SQLAlchemy ORM
- ✅ PostgreSQL integration
- ✅ pgvector support
- ✅ Modular service architecture
- ✅ Storage abstraction layer
- ✅ Background document processing

---

### AI / Machine Learning

- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Sentence Transformer embeddings
- ✅ Semantic similarity search
- ✅ Context-aware prompt generation
- ✅ Groq LLM integration
- ✅ Source attribution

---

### Document Processing

- ✅ PDF upload
- ✅ PDF text extraction
- ✅ Text chunking
- ✅ Embedding generation
- ✅ Vector database storage
- ✅ Processing status tracking
- ✅ Document deletion

---

### Frontend

- ✅ Streamlit interface
- ✅ Document upload
- ✅ Processing status display
- ✅ Question-answer interface
- ✅ Source reference display

---

### Infrastructure

- ✅ Docker development environment
- ✅ Docker Compose
- ✅ Render backend deployment
- ✅ Streamlit Community Cloud deployment
- ✅ Google Cloud Storage integration

---

### Documentation

- ✅ Comprehensive README
- ✅ API documentation
- ✅ Architecture documentation
- ✅ Deployment guide
- ✅ Production-ready project structure

---

# Learning Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation (RAG)
- Large Language Model integration
- Vector databases
- Semantic search
- Backend engineering with FastAPI
- Cloud-native application architecture
- Database design
- Docker containerization
- Production deployment
- Modular software architecture

---

# Acknowledgements

This project leverages several outstanding open-source technologies.

Special thanks to the communities behind:

- FastAPI
- Streamlit
- PostgreSQL
- pgvector
- Sentence Transformers
- SQLAlchemy
- Docker

Their tools make modern AI application development significantly more accessible.

---

# License

This project is developed as a **portfolio engineering project** demonstrating modern AI application architecture, Retrieval-Augmented Generation (RAG), backend engineering, cloud deployment, and software engineering best practices.

It is intended for educational, demonstration, and portfolio purposes.

---

## Contact

If you'd like to discuss the project, provide feedback, or connect professionally, feel free to reach out through GitHub or LinkedIn.

If you found this project useful, consider giving the repository a ⭐.