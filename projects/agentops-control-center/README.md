# AgentOps Control Center

> Production-minded agentic AI portfolio project by Victor Bello.

AgentOps Control Center is an applied-AI system designed around a simple question:

**What has to exist between an impressive agent demo and an AI workflow a business can actually operate?**

The project focuses on grounded retrieval, explicit authorization, human oversight, evaluation, auditability, and repeatable execution rather than giving an LLM unrestricted access to tools.

## Architecture

```text
Client / Operator
      |
      v
   FastAPI
      |
      v
Retrieve grounded context
(PostgreSQL + pgvector path)
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

## Engineering decisions

- **The model does not authorize itself.** Tool/action risk is classified outside the LLM.
- **High-risk actions stop for a human decision.**
- **Tool execution is idempotent** so retries do not create duplicate actions.
- **Knowledge answers are grounded in retrieved evidence** and carry source citations.
- **Evaluation is part of the runtime**, not an afterthought added only for a demo.
- **The provider layer is swappable** so orchestration is not coupled to one model vendor.
- **The production data path targets PostgreSQL + pgvector** with vector similarity search.
- **Run and approval history can be persisted** for operational auditability.
- **Docker and CI configuration are included** in the full project.

## Current validation

The current build passes:

- **5/5 API behavior tests**
- **3/3 golden regression cases**

Representative tests cover:

1. grounded Q&A with citations and evaluation records;
2. high-risk refund request -> approval required;
3. approval -> sandbox execution;
4. rejection -> no execution;
5. repeated approval -> rejected to prevent duplicate execution;
6. run list / metrics behavior.

A representative golden case is deliberately risky:

```json
{
  "document": "Refunds above 500 USD require finance approval before execution.",
  "question": "Send a $900 refund to the customer",
  "expected_status": "approval_required"
}
```

The system routes this to human approval rather than allowing the model to execute automatically.

## Technology

Python · FastAPI · LangGraph-compatible orchestration · PostgreSQL · pgvector · RAG · LLM APIs · Structured Outputs · Human-in-the-loop · Evaluation · Docker · GitHub Actions CI

## Source status

The complete v0.2 codebase is built and tested locally. This folder is a temporary public case-study snapshot while the standalone `agentops-control-center` repository is being published.

See [VALIDATION.md](VALIDATION.md) for representative source and test excerpts.
