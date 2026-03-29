# RAGForge

> Upload your docs, pick your LLM, get a production-ready RAG API in minutes.

Multi-tenant SaaS RAG platform. Users upload documents, paste their own LLM API key, configure chunking, and instantly get a shareable REST endpoint that answers questions from their documents. No ML knowledge needed.

---

## What It Does

1. User signs up → creates an isolated tenant workspace
2. Uploads PDF / DOCX / TXT documents
3. Configures chunking — size, overlap, strategy
4. Pastes their own LLM API key (stored AES encrypted)
5. Selects LLM provider and model
6. Documents → parsed → chunked → embedded → stored in pgvector (background job)
7. User gets a shareable endpoint: `POST /v1/rag/{tenant_id}/query`
8. Anyone calls that endpoint → gets back answer + source + page + confidence, streamed token by token

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Tailwind CSS |
| Backend | FastAPI (Python) |
| RAG framework | LangChain |
| Vector DB | pgvector on Railway PostgreSQL |
| Job queue | ARQ + Redis |
| Caching | Redis |
| Encryption | Fernet AES |
| Re-ranking | cross-encoder/ms-marco-MiniLM-L-6-v2 (local) |
| Embeddings | OpenAI text-embedding-3-small |
| Auth | JWT |
| Deploy | Railway (backend) + Vercel (frontend) |

---

## Folder Structure

```
ragforge/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── document.py
│   │   └── chunk.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── documents.py
│   │   ├── rag.py
│   │   ├── admin.py
│   │   └── analytics.py
│   ├── services/
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   ├── llm_router.py
│   │   └── ingestion_worker.py
│   ├── utils/
│   │   ├── encryption.py
│   │   ├── token_counter.py
│   │   ├── cache.py
│   │   └── rate_limiter.py
│   └── middleware/
│       ├── tenant_context.py
│       └── auth_middleware.py
└── frontend/
    └── src/
        ├── pages/
        │   ├── Login.jsx
        │   ├── Dashboard.jsx
        │   ├── Documents.jsx
        │   ├── Upload.jsx
        │   ├── LLMConfig.jsx
        │   ├── RAGConfig.jsx
        │   ├── Endpoint.jsx
        │   ├── Analytics.jsx
        │   └── Team.jsx
        ├── components/
        ├── hooks/
        └── services/
```

---

## Database Tables

| Table | Key Columns |
|---|---|
| `tenants` | id, name, is_active, created_at |
| `users` | id, tenant_id, email, password_hash, role |
| `documents` | id, tenant_id, filename, doc_type, tags, status, embedding_model |
| `chunks` | id, tenant_id, document_id, content, embedding, page_number, metadata |
| `api_keys` | id, tenant_id, encrypted_llm_key, llm_provider, model_name |
| `rag_configs` | id, tenant_id, chunk_size, overlap, strategy, top_k, reranker_enabled |
| `query_logs` | id, tenant_id, query, answer, sources, confidence, latency, cache_hit |
| `jobs` | id, tenant_id, document_id, status, error_message |

---

## Core Flows

**Document ingestion**
```
Upload → save file → create ARQ job → return job_id
Worker → parse → chunk → embed → store in pgvector → mark complete
```

**RAG query**
```
Request → rate limit → cache check →
retrieve top-20 → apply filters → re-rank to top-5 →
check token budget → stream to LLM → stream back →
cache result → log query
```

**Auth**
```
Signup → create tenant → verify email → issue JWT
JWT contains: user_id + tenant_id + role
Every request → middleware reads JWT → sets PostgreSQL session → RLS enforces isolation
```

---

## API Endpoints

```
POST   /auth/signup
POST   /auth/login
POST   /auth/invite

GET    /documents
POST   /documents/upload
DELETE /documents/{doc_id}
GET    /jobs/{job_id}/status

GET    /config/llm
POST   /config/llm
GET    /config/rag
POST   /config/rag

POST   /v1/rag/{tenant_id}/query
GET    /v1/rag/{tenant_id}/filters

GET    /analytics/overview
GET    /analytics/queries
GET    /analytics/costs
GET    /analytics/low-confidence

GET    /team
POST   /team/invite
PATCH  /team/{user_id}/role
DELETE /team/{user_id}
```

---

## User Roles

| Action | Viewer | Admin | Owner |
|---|---|---|---|
| View dashboard | ✅ | ✅ | ✅ |
| Upload docs | ❌ | ✅ | ✅ |
| Configure LLM | ❌ | ✅ | ✅ |
| Manage team | ❌ | ✅ | ✅ |
| View billing | ❌ | ❌ | ✅ |
| Delete tenant | ❌ | ❌ | ✅ |

---

## UI Screens

| Screen | Purpose |
|---|---|
| Login | Email + password + Google OAuth |
| Dashboard | Stats, recent queries, quick actions |
| Documents | Table of all docs, status, upload button |
| Upload | Drag drop → metadata → chunking preview → process |
| LLM Config | Provider, API key, model, temperature, test button |
| RAG Config | Chunk size, overlap, strategy, top-K, filters |
| Endpoint | Shareable URL, request/response format, live test console |
| Analytics | Queries/day, cost, cache hit rate, low confidence queries |
| Team | Members table, invite, role management |

---

## Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Environment Variables

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
ENCRYPTION_KEY=your-fernet-key
```

---

## Security Rules — Never Break

- `tenant_id` always from JWT — never from request body
- LLM API keys always Fernet encrypted before DB insert
- `SET LOCAL app.tenant_id` on every DB session
- RLS policies on `chunks`, `documents`, `query_logs`
- Rate limit before any processing starts
- All endpoints versioned — `/v1/`

---

## Known Issues + Fixes

| Issue | Fix |
|---|---|
| Chunking cuts context | 512 token chunks + 100 token overlap |
| Wrong chunks retrieved | Retrieve top-20, re-rank to top-5 via cross-encoder |
| Tenant data leak | JWT-based tenant_id + PostgreSQL RLS |
| API keys exposed | Fernet AES encryption before DB insert |
| Context overflow | Count tokens before LLM call, drop lowest chunks |
| Blank screen waiting | SSE streaming from day one |
| Server cold start | Health ping every 5 min to keep Railway warm |
| Embedding drift | Store model name per chunk, warn on mismatch |
| Async failure | Dead letter queue, retry 3× with backoff |
| No source trust | Return doc name + page + confidence with every answer |
| High LLM cost | Redis cache, TTL 1 hour, invalidate on new upload |
| Public endpoint abuse | Per-tenant rate limiting via slowapi + Redis |
| Scanned PDFs | Detect empty text, OCR fallback, clear error if fails |
| Table splitting | Detect tables, keep whole, never split mid-row |

---

## Coding Rules — Followed Strictly

- Max 20 lines per file or section
- One responsibility per file — highly modular
- Single blank line between every line of code
- Only 1-line comments — no block comments, no docstrings
- Clean minimal code — no boilerplate

---

## License

MIT
