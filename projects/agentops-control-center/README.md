# AgentOps Control Center

**Production-minded agentic AI portfolio system for grounded retrieval, policy-controlled actions, human approval, evaluation, guardrails, and auditability.**

AgentOps Control Center is deliberately built around the gap between a compelling AI demo and a system an operations team could responsibly run. It treats retrieval quality, permissions, prompt injection, retries, audit state, evaluation, and failure modes as first-class engineering concerns.

## Current validation - v0.3

- **9/9 API and behavior tests passing**
- **5/5 isolated golden regression cases passing (100%)**
- Covered behavior includes grounded Q&A, read-only vs action intent, high-risk approval, rejection with no execution, duplicate-approval prevention, direct prompt-injection blocking, indirect prompt-injection filtering, upload ingestion, request IDs, and runtime metrics.

## Why this project exists

Many agent demos let the model retrieve data and call tools, then stop at "it works." AgentOps asks harder questions:

- What evidence was used, and can the answer be traced back to it?
- Can an LLM accidentally authorize its own consequential action?
- What happens when retrieved content contains malicious instructions?
- Can a repeated approval or retry cause a duplicate side effect?
- Can behavior be measured with regression cases instead of a good-looking demo?
- Can an operator inspect what happened after the fact?

## Architecture

```text
Client
  |
FastAPI + request ID
  |
Input guardrails  ---> blocked requests stop + audit
  |
Hybrid retrieval (vector candidates + lexical rerank)
  |
Evidence guard (filter indirect prompt injection)
  |
Deterministic risk policy
  |                         |
read-only / low             high-risk side effect
  |                         |
LLM / reasoner              Human approval
  |                         | reject -> no execution
  |                         | approve
  |                         v
  |                    Idempotent tool boundary
  +-------------+-----------+
                |
          Eval + audit state
```

## Engineering decisions

### Authorization is outside the model
The reasoner can propose or explain. It cannot grant itself permission. High-risk actions stop at a deterministic policy layer and explicit human approval.

### Knowledge questions are not actions
A regression case protects a subtle failure mode: **"What is the refund policy?"** remains read-only even though it contains the word "refund." **"Send a $900 refund"** is a high-risk action.

### Retrieved documents are untrusted
RAG content can contain hostile instructions. Suspicious evidence chunks are filtered before reasoning and recorded as guardrail events.

### Retrieval is hybrid
The retriever pulls a wider vector candidate set and combines vector similarity with lexical overlap before selecting final evidence.

### Evals are a release gate
Every golden case runs with fresh state so an earlier document cannot accidentally make a later case pass.

## Stack

Python · FastAPI · LangGraph-compatible orchestration · PostgreSQL · pgvector · HNSW cosine search · hybrid RAG · OpenAI provider adapter · human-in-the-loop · evals · Docker · CI/CD concepts

## Public source snapshot

- [Core implementation excerpts](CORE_IMPLEMENTATION.md)
- [Validation and failure modes](VALIDATION.md)
- [Guardrails](app/guardrails.py)
- [Action policy](app/tools.py)
- [API tests](tests/test_api.py)
- [Golden eval dataset](evals/golden.jsonl)
- [Case study](CASE_STUDY.md)

The complete v0.3 source bundle is being prepared for a standalone repository. This snapshot exposes the engineering decisions and tested behavior now rather than waiting for the repo migration.

## What this project does not claim

This is a portfolio engineering system, not a claim of live enterprise adoption. The public tool executor is intentionally sandboxed. Production deployment would still need organization-specific identity/RBAC, document ACLs, managed secrets, rate limiting, monitoring/alerting, retention policy, and tool-specific authorization scopes.

Built by **Victor Bello** - Applied AI / Forward-Deployed AI portfolio work.
