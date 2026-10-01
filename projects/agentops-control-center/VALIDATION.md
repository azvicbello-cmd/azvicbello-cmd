# AgentOps Control Center — Validation & Source Excerpts

This page exposes representative implementation details from the tested v0.2 build.

## Authorization is outside the model

```python
def _route_after_plan(self, state):
    return "approval" if state.get("risk") == RiskLevel.high else "answer"

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

The LLM can help reason about a request, but it does not grant itself permission to perform a consequential action.

## Idempotent sandbox execution

```python
def execute(self, run_id: str, action: str):
    key = hashlib.sha256(f"{run_id}:{action}".encode("utf-8")).hexdigest()[:24]
    if key in self._executions:
        return self._executions[key]

    result = ToolExecutionResult(
        action=action,
        status="simulated_success",
        idempotency_key=key,
        message="Human approval accepted. Sandbox execution recorded.",
    )
    self._executions[key] = result
    return result
```

## Evaluation is a runtime concern

The current evaluation record combines groundedness, citation coverage, and retrieval confidence. The goal is not to pretend a small heuristic is a universal AI-quality score; it is to make evaluation explicit, inspectable, and replaceable by stronger task-specific evals.

```python
overall = (
    groundedness * 0.5
    + citation_coverage * 0.3
    + retrieval_confidence * 0.2
)
```

## Representative API test

```python
def test_high_risk_action_requires_human_approval_then_sandbox_execution(client):
    response = client.post(
        "/query",
        json={"question": "Send a $900 refund to the customer"},
    )
    body = response.json()

    assert body["status"] == "approval_required"
    assert body["risk"] == "high"
    assert body["approval_id"]

    approved = client.post(f"/approvals/{body['approval_id']}/approve")
    assert approved.status_code == 200
    assert approved.json()["tool_execution"]["status"] == "simulated_success"

    duplicate = client.post(f"/approvals/{body['approval_id']}/approve")
    assert duplicate.status_code == 409
```

## Test checkpoint

- API suite: **5/5 passing**
- Golden regression set: **3/3 passing**

## Full-build components

The local full build additionally contains FastAPI endpoints, deterministic/provider-backed reasoning interfaces, embedding interfaces, retrieval abstraction, PostgreSQL stores, pgvector search, audit persistence, Docker/Compose configuration, CI, security notes, threat model, evaluation documentation, and a recruiter-facing case study.
