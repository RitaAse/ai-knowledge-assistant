# AI Knowledge Assistant - API Design

## Overview

The AI Knowledge Assistant API provides the backend interface for document management and Retrieval-Augmented Generation (RAG) functionality.

The API is built using:

- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL

The API is responsible for:

- Receiving document uploads
- Managing document metadata
- Triggering document processing
- Retrieving stored documents
- Performing semantic search
- Returning grounded AI-generated answers with sources

---

# API Architecture

The API follows a layered architecture:

```text
Client

 |

 v

FastAPI Router Layer

 |

 v

Service Layer

 |

 +----------------+

 |                |

Database       Storage

 |

 v

AI Services
(Embeddings + LLM)
```

The API layer focuses on:

- Request handling
- Validation
- Response formatting

Business logic is implemented inside dedicated services.

---

# Deployment

## Local Development

Backend:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

OpenAPI specification:

```
http://localhost:8000/openapi.json
```

---

## Cloud Deployment

The backend is deployed using:

```
Render
```

The frontend communicates with the deployed API through HTTP requests.

Production URL:

```
<Render backend URL>
```

---

# API Endpoints Overview

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/documents/upload` | Upload a document |
| GET | `/documents` | Retrieve documents |
| GET | `/documents/{id}` | Retrieve document metadata |
| GET | `/documents/{id}/file` | Download original file |
| DELETE | `/documents/{id}` | Delete document |
| POST | `/documents/search` | Ask questions using RAG |

---

# Document Management API

---

# Upload Document

## Endpoint

```
POST /documents/upload
```

## Description

Uploads a PDF document and starts asynchronous processing.

The upload request performs:

1. Save document file
2. Create document metadata
3. Return upload response
4. Start background processing

Processing occurs asynchronously.

---

## Request

Content-Type:

```
multipart/form-data
```

Parameter:

| Field | Type | Required |
|---|---|---|
| file | PDF | Yes |

---

## Response

Status:

```
201 Created
```

Example:

```json
{
    "id": 1,
    "filename": "manual.pdf",
    "processing_status": "UPLOADED",
    "created_at": "2026-07-24T10:30:00"
}
```

---

# Document Processing Lifecycle

Documents move through:

```text
UPLOADED

    |

    v

PROCESSING

    |

    v

COMPLETED
```

Failed processing:

```text
PROCESSING

    |

    v

FAILED
```

---

# Retrieve Documents

## Endpoint

```
GET /documents
```

## Description

Returns uploaded documents and processing status.

---

## Response

Example:

```json
[
    {
        "id": 1,
        "filename": "manual.pdf",
        "processing_status": "COMPLETED"
    }
]
```

---

# Retrieve Document Details

## Endpoint

```
GET /documents/{document_id}
```

Returns metadata for one document.

---

## Example Response

```json
{
    "id": 1,
    "filename": "manual.pdf",
    "file_type": "application/pdf",
    "processing_status": "COMPLETED"
}
```

---

# Download Original Document

## Endpoint

```
GET /documents/{document_id}/file
```

## Description

Retrieves the original uploaded PDF.

Response:

```
Binary PDF file
```

Headers:

```http
Content-Type: application/pdf

Content-Disposition: attachment
```

---

# Delete Document

## Endpoint

```
DELETE /documents/{document_id}
```

## Description

Deletes:

- Document metadata
- Stored file
- Associated chunks

---

## Response

```json
{
    "message": "Document deleted successfully."
}
```

---

# Retrieval-Augmented Generation API

---

# Ask Question

## Endpoint

```
POST /documents/search
```

## Description

Answers questions using uploaded documents.

The pipeline:

```text
User Question

 |

Question Embedding

 |

Vector Similarity Search

 |

Relevant Document Chunks

 |

Context Construction

 |

LLM Generation

 |

Answer + Sources
```

---

# Request

Example:

```json
{
    "question": "What operating system is required?"
}
```

---

# Response

Example:

```json
{
    "answer": "The recommended operating system is Linux.",
    "sources": [
        {
            "document": "installation-guide.pdf",
            "page": 4,
            "relevance": 92,
            "preview": "Linux is supported..."
        }
    ]
}
```

---

# Source Response Design

Each source contains:

| Field | Description |
|---|---|
| document | Document filename |
| page | Source page number |
| relevance | Similarity score |
| preview | Supporting text |

Source references improve:

- Transparency
- Trust
- Answer verification

---

# Error Handling

The API uses standard HTTP status codes.

| Code | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 400 | Invalid request |
| 404 | Resource not found |
| 500 | Server error |

---

## Example Error Response

```json
{
    "detail": "Document not found."
}
```

---

# Current API Limitations

The current version is designed as a portfolio demonstration.

## Authentication

Currently:

```
Single application environment
```

Future versions will introduce:

- User accounts
- Authentication
- Authorization
- Document ownership

---

## Multi-user Support

Future architecture:

```text
User

 |

Documents

 |

Permissions

 |

RAG Pipeline
```

---

# Future API Improvements

Potential improvements:

## API Versioning

Example:

```
/api/v1/documents
```

---

## Pagination

For large document collections:

```
GET /documents?page=1&limit=20
```

---

## Authentication

Possible approaches:

- OAuth2
- JWT tokens
- Enterprise identity providers

---

## Streaming Responses

Future RAG responses could support:

- Token streaming
- Progressive answer generation
- Better user experience

---

## Rate Limiting

Production systems should include:

- Request limits
- Abuse prevention
- API monitoring

---

# API Summary

The AI Knowledge Assistant API provides:

✅ Document upload  
✅ Document lifecycle management  
✅ File retrieval  
✅ Document deletion  
✅ Semantic search  
✅ RAG-based question answering  
✅ Source-grounded responses  

The API design follows modern backend engineering practices:

- REST principles
- Layered architecture
- Service separation
- Structured responses
- Future scalability considerations