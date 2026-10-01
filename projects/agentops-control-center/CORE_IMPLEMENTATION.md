# Core Implementation - v0.3

This page exposes the core control flow without hiding the engineering behind screenshots.

## Agent flow

```python
def _guard_input(self, state):
    assessment = assess_user_input(state["question"])
    if assessment.blocked:
        return {
            "status": RunStatus.blocked,
            "answer": assessment.reason,
            "guardrail_flags": assessment.flags,
            "retrieval_strategy": "not_run",
        }
    return {"guardrail_flags": assessment.flags}

def _retrieve(self, state):
    result = self.retriever.retrieve_with_diagnostics(state["question"])
    return {
        "citations": result.citations,
        "guardrail_flags": sorted(set(state.get("guardrail_flags", []) + result.guardrail_flags)),
        "filtered_evidence_count": result.filtered_evidence_count,
        "retrieval_strategy": result.strategy,
    }

def _plan(self, state):
    decision = classify_tool_intent(state["question"])
    return {"action": decision.action, "risk": decision.risk, "reason": decision.reason}

def _route_after_plan(self, state):
    return "approval" if state.get("risk") == RiskLevel.high else "answer"
```

## Hybrid retrieval

```python
candidates = self.store.search(
    self.embedder.embed(query),
    max(self.top_k * 3, self.top_k),
)

for chunk, vector_score in candidates:
    lexical_score = _lexical_overlap(query_terms, _meaningful_terms(chunk.content))
    combined = (max(0.0, vector_score) * 0.65) + (lexical_score * 0.35)
    ...
safe, flags, filtered = filter_untrusted_evidence(ranked[: self.top_k * 2])
```

The retrieval layer deliberately pulls a wider vector set before application-level reranking. The lightweight lexical component is transparent and useful for operational terminology; a larger production corpus could replace it with database/search-engine hybrid ranking and a learned reranker.

## Human approval

```python
def _approval_gate(self, state):
    record = self.approvals.create(
        run_id=state["run_id"],
        action=state.get("action") or "unknown_action",
        risk=state.get("risk", RiskLevel.high),
        reason=state.get("reason", "External side effect"),
    )
    return {
        "approval_id": record.id,
        "status": RunStatus.approval_required,
        "answer": "The proposed external action is blocked until a human explicitly approves it.",
    }
```

## Idempotent tool boundary

```python
key = hashlib.sha256(f"{run_id}:{action}".encode("utf-8")).hexdigest()[:24]
if key in self._executions:
    return self._executions[key]
```

The public adapter is a sandbox. The important engineering signal is that authorization and execution are separate boundaries and repeated approval cannot silently create a second side effect.

## Eval isolation

```python
def run_case(case):
    # Fresh state for every case.
    service, retriever = build_service()
    ...
```

This was added after identifying that a shared vector store could contaminate later regression cases.
