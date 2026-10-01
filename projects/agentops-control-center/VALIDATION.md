# Validation - AgentOps Control Center v0.3

## Release gate

**API / behavior tests:** 9/9 passing  
**Golden regression cases:** 5/5 passing (100%)

The golden runner creates a fresh service and vector store for every case. This prevents cross-case evidence contamination from making an evaluation pass accidentally.

## Cases currently protected

| Case | Expected behavior |
| --- | --- |
| Priority-1 incident question | completed, low risk, expected source |
| "What is the refund policy?" | completed, low risk, no approval |
| "Send a $900 refund..." | high risk, approval required |
| API-key rotation question | grounded answer with expected source |
| malicious retrieved instruction | unsafe evidence filtered before reasoning |

## Behavior tests also verify

- source citations and eval breakdown are returned;
- audit events record retrieval, policy and evaluation stages;
- human approval reaches only the sandbox tool boundary;
- human rejection executes nothing;
- the same approval cannot execute twice;
- direct prompt-injection attempts are blocked before retrieval;
- text/Markdown file ingestion works;
- caller-supplied request IDs are returned for trace correlation;
- runtime metrics expose status counts and p95 latency.

## Bug found by the suite

An early classifier treated the noun "refund" as if it always meant "perform a refund." The query:

> What is the refund policy?

was incorrectly escalated.

The policy layer was redesigned around action patterns plus read-only/interrogative precedence, and the failure became a permanent golden regression case.

## Retrieval failure found by the suite

After fixing action intent, the first v0.3 golden run exposed a second issue: the lexical fallback did not normalize **refund** vs **refunds**. Instead of lowering the evaluation threshold, the retriever was fixed with lightweight term normalization and the full suite was rerun.

That sequence is intentional: the tests are a release gate, not a marketing number.
