# AgentOps Control Center — v0.3 public snapshot

> Production-minded agentic AI portfolio project by Victor Bello.

AgentOps Control Center asks a practical question:

**What has to exist between an impressive agent demo and an AI workflow a business can actually operate?**

The system focuses on grounded retrieval, document ingestion, explicit authorization, human oversight, retrieval guardrails, evaluation, auditability, and repeatable execution rather than giving an LLM unrestricted access to tools.

## Architecture

```text
Client / Operator
      |
      v
FastAPI + request ID / structured request log
      |
      v
Document ingestion / retrieval
(PostgreSQL + pgvector path)
      |
      v
Retrieval warning signals + bounded trusted context
      |
      v
Deterministic policy classification
      |
      +-------------------+
      | read / low risk   | high-risk action
      v                   v
LLM/provider reasoning   Human approval gate
      |                   |
      v                   +--> reject -> no side effect
Cited answer              |
      |                   +--> approve -> idempotent tool adapter
      v
Evaluation + audit record
```

## v0.3 engineering decisions

- **The model does not authorize itself.** Action risk is classified outside the LLM.
- **Read-only questions are distinguished from action requests.** “What is the refund policy?” is low risk; “Send a $900 refund” requires approval.
- **High-risk actions stop for a human decision.**
- **Tool execution is idempotent** so retries do not create duplicate actions.
- **Direct document ingestion** supports TXT, MD, LOG, CSV, JSON, PDF, XLSX, and XLSM.
- **Retrieved instruction-like content is marked untrusted** and excluded from trusted reasoning context.
- **Reasoning context is bounded** rather than growing without limit.
- **Request IDs and structured HTTP logs** improve trace correlation.
- **Knowledge answers are grounded in retrieved evidence** and carry source citations.
- **Evaluation is part of the runtime**, not an afterthought.
- **The production data path targets PostgreSQL + pgvector** with vector similarity search.
- **Run and approval history can be persisted** for operational auditability.

## Current validation

- **9/9 API behavior tests passing**
- **5/5 isolated golden regression cases passing (100%)**
- XLSX ingestion manually smoke-tested end-to-end
- high-risk action -> approval required before execution
- rejection -> no execution
- duplicate approval -> rejected
- prompt-injection-like retrieved text -> warning + excluded trusted context
- read-only refund-policy question -> no false approval gate

The golden evaluator runs each case with a fresh isolated store and checks expected source, run status, risk classification, optional answer behavior, and optional guardrail warning.

## Technology

Python · FastAPI · LangGraph-compatible orchestration · PostgreSQL · pgvector · RAG · LLM APIs · Human-in-the-loop · Evaluation · Docker · GitHub Actions CI

## Public source excerpts

Representative source files are included in this snapshot under `app/`. The complete v0.3 package contains the full backend, tests, Docker/Compose configuration, CI, docs, security notes, and recruiter-facing case study.

See [VALIDATION.md](VALIDATION.md) for the validation design.
