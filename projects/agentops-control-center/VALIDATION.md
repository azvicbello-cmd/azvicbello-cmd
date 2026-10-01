# AgentOps Control Center — v0.3 Validation

The current local v0.3 build is validated against both API behavior and an isolated golden regression set.

## Checkpoint

- API suite: **9/9 passing**
- Golden regression set: **5/5 passing (100%)**
- XLSX ingestion: **end-to-end smoke test passed**

## What the API suite covers

1. health/runtime configuration;
2. grounded query with citations, eval breakdown, and audit events;
3. high-risk action -> human approval -> sandbox execution;
4. rejection -> no tool execution;
5. metrics and run listing;
6. direct text-file upload plus request-ID propagation;
7. CSV upload + retrieval;
8. prompt-injection-like retrieved content is flagged and excluded from trusted answer context;
9. “What is the refund policy?” remains read-only instead of triggering an approval false positive.

## Stronger golden regression design

Every case gets a **fresh vector store and service instance**. That prevents an earlier document from accidentally making a later case pass.

The runner can assert:

- expected source;
- expected run status;
- expected risk level;
- optional answer substring;
- optional retrieval warning.

Current cases cover Priority-1 incident knowledge, a consequential refund action, security-key rotation, a read-only refund-policy question, and untrusted retrieved instructions.

## Authorization is outside the model

```python
def _route_after_plan(self, state):
    return "approval" if state.get("risk") == RiskLevel.high else "answer"
```

The LLM can reason about evidence, but it does not grant itself permission to perform a consequential action.

## Guardrail boundary

Retrieved text that resembles an instruction to override policy or expose secrets receives warning metadata. The reasoner excludes warned citations from its trusted evidence context.

This is deliberately described as **defense-in-depth**, not as a claim that prompt injection is solved.

## Honest limitations

The project does not claim production SSO/RBAC, tenant isolation, managed secrets, real payment/email connectors, full semantic prompt-injection defense, an OpenTelemetry exporter, or OCR for scanned PDFs.
