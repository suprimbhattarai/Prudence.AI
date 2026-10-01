
# Prudence AI

Prudence AI is an AI-native customer-support and field-service operations platform focused first on Internet Service Providers (ISPs).

It is designed to handle the full support lifecycle:

complaint → issue understanding → troubleshooting → knowledge retrieval → allowed actions → human escalation → technician scheduling → geographically valid assignment → field visit → resolution → service report → feedback

Prudence is not intended to be only a chatbot. The long-term goal is to build a complete AI-assisted support and operations system.

---

## Current Focus

The current development focus is the ISP vertical.

The project is being built as a clean modular monolith first, with architecture that can grow without turning into large tightly-coupled files.

Current backend work includes:

- User account models
- Customer profiles
- Technician profiles
- Admin profiles
- Technician skills
- Technician teams
- Service zones
- Team-to-service-zone relationships
- PostgreSQL integration
- SQLAlchemy ORM models

Authentication, authorization, ticketing, appointments, technician scheduling, AI workflows, and the frontend will be added gradually.

---

## Core Product Flow

```text
Customer issue
    ↓
Prudence understands the complaint
    ↓
Troubleshooting
    ↓
Retrieve organization knowledge
    ↓
Take allowed actions
    ↓
Escalate to human when required
    ↓
Create ticket / appointment
    ↓
Find geographically valid technicians
    ↓
Filter by availability and required skills
    ↓
Assign technician
    ↓
Track field visit
    ↓
Resolve issue
    ↓
Generate service report
    ↓
Customer feedback
```

---

## Technician Assignment Principle

Location is a hard filter before skill ranking.

A technician should not be assigned simply because they have better skills if they are outside the correct service area.

The intended order is:

```text
same organization
    ↓
correct service region
    ↓
travel feasible
    ↓
on duty
    ↓
available
    ↓
required skills
    ↓
appointment / SLA compatible
    ↓
candidate ranking
```

Future ranking may consider:

- ETA
- Skill proficiency
- Workload
- SLA urgency
- Fairness

Initial geographic assignment uses service zones.

Later stages may introduce:

- Coordinates
- Haversine distance
- PostGIS
- Routing
- Real ETA estimation

---

## Multilingual Support

Prudence is intended to support real-world ISP customer language, including:

- English
- Nepali
- Nepali Unicode
- Romanized Nepali
- Nepali-English mixed text
- Slang
- Misspellings
- Informal grammar

Examples:

```text
mero internet chalena
wifi ekdam slow xa
router ma red light balirako cha k garne
aja bihana dekhi net chaina
restart gare tara still chalena
technician kahile aaucha?
```

Multilingual AI support will be introduced gradually when the AI pipeline reaches that stage.

---

## Architecture

Clean architecture is a core requirement of this project.

The project avoids large god files and keeps responsibilities separated.

Example backend structure:

```text
backend/
├── api/
├── core/
├── dependencies/
├── models/
│   ├── base.py
│   ├── users/
│   │   ├── user.py
│   │   ├── customer_profile.py
│   │   ├── technician_profile.py
│   │   ├── admin_profile.py
│   │   ├── skill.py
│   │   └── technician_skill.py
│   └── workforce/
│       ├── team.py
│       ├── service_zone.py
│       └── team_service_zone.py
├── repositories/
├── schemas/
├── services/
├── tests/
├── database.py
└── main.py
```

The same clean separation will be followed in frontend, AI, RAG, retrieval, agents, evaluations, infrastructure, and testing.

---

## Technology Stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- PWA

### Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

### Caching and State

- Redis

Redis may later be used for:

- caching
- rate limiting
- session/state support
- temporary workflow state
- background-task coordination

### AI / Machine Learning

Planned technologies include:

- NumPy
- Pandas
- scikit-learn
- PyTorch
- Hugging Face
- sentence-transformers

### Retrieval / RAG

Planned topics and technologies:

- Document processing
- Chunking strategies
- Embedding strategies
- Embeddings
- Cosine similarity
- Full database/vector scans
- Approximate Nearest Neighbor search
- HNSW
- Qdrant
- BM25
- Dense retrieval
- Sparse retrieval
- Hybrid retrieval
- Reranking
- Full RAG pipelines

### Agents and Tool Use

Planned technologies:

- LangChain
- LangGraph
- Agentic AI
- MCP

Agentic workflows will only be introduced after normal backend workflows and tool functions exist.

### Infrastructure

Planned gradually as needed:

- Docker
- Docker Compose
- Celery
- MinIO / S3
- CI/CD

Possible much-later additions:

- Kafka
- Microservices
- Kubernetes

---

## AI Engineering Learning Goals

Prudence is also being built as an AI engineering learning project.

Topics to be explored gradually include:

- Naive Bayes
- Neural Networks
- Artificial Neural Networks
- Deep Learning
- Gradient Descent
- Forward pass
- Backpropagation
- Loss functions
- Activation functions
- CNN
- RNN
- LSTM
- Self-attention
- Transformers
- BERT
- LLMs
- Token masking
- Attention masks
- Fine-tuning
- Embeddings
- Cosine similarity
- Vector databases
- BM25
- Approximate Nearest Neighbor search
- RAG
- LangChain
- LangGraph
- Agentic AI
- MCP
- Context vs harness

The goal is not to force every technique into production. Some technologies will be used for experiments and comparisons before deciding whether they are useful for Prudence.

---

## RAG Learning Path

Prudence will not jump directly into framework-based RAG.

The intended progression is:

```text
documents
    ↓
cleaning
    ↓
chunking
    ↓
embeddings
    ↓
vectors
    ↓
cosine similarity
    ↓
brute-force / full scan retrieval
    ↓
ANN / indexed retrieval
    ↓
Qdrant
    ↓
BM25
    ↓
dense + sparse retrieval
    ↓
hybrid retrieval
    ↓
reranking
    ↓
full RAG pipeline
```

This makes it possible to understand what frameworks such as LangChain actually abstract.

---

## Human-in-the-Loop

Not every decision should be automated.

Human review will remain important for cases involving:

- Low confidence
- Sensitive issues
- Security concerns
- Financial issues
- Legal concerns
- Explicit customer requests for a human

Routine low-risk tasks may be automated where appropriate.

---

## Security Goals

Security will be added progressively, including:

- Password hashing
- JWT authentication
- OAuth / OIDC where appropriate
- RBAC
- Tenant isolation
- Secret management
- Input validation
- PII protection
- Audit logs
- Rate limiting
- Tool authorization

---

## Forward Deployed Engineer Goal

Prudence is also intended to develop Forward Deployed Engineer-style skills:

- Understanding customer workflows
- Translating business problems into software systems
- AI integration
- API integration
- Deployment
- Observability
- Evaluation
- Failure handling
- Measuring business impact

---

## Project Status

Prudence is currently in early development.

The project is intentionally being built step-by-step with emphasis on:

- clean architecture
- correct relational modeling
- production-style code organization
- strong AI engineering fundamentals
- practical ISP workflows
- multilingual support
- explainable system design

---
