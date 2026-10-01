from __future__ import annotations

import re
from dataclasses import dataclass

from app.models import RiskLevel


@dataclass(frozen=True)
class ToolDecision:
    action: str | None
    risk: RiskLevel
    reason: str


_READ_ONLY_PREFIX = re.compile(
    r"^\s*(what|why|how|when|where|who|which|explain|describe|summari[sz]e|tell me|show me|find|search|look up|can you explain|could you explain)\b",
    re.I,
)

_HIGH_RISK_PATTERNS = (
    ("send_external_action", re.compile(r"\b(send|email|message|notify)\b.{0,80}\b(customer|client|user|vendor|supplier|recipient|email|message|notification)\b", re.I)),
    ("refund_external_action", re.compile(r"\b(send|issue|process|execute|initiate|approve|refund)\b.{0,80}\b(refund|customer|client|account|usd|\$)\b", re.I)),
    ("delete_external_action", re.compile(r"\b(delete|remove|erase|purge)\b.{0,80}\b(record|account|user|customer|file|data|database|row)\b", re.I)),
    ("payment_external_action", re.compile(r"\b(pay|transfer|purchase|buy|charge)\b.{0,80}\b(invoice|vendor|supplier|account|card|usd|\$|money|funds?)\b", re.I)),
    ("publish_external_action", re.compile(r"\b(publish|post)\b.{0,80}\b(public|production|website|social|linkedin|twitter|x\b|announcement)\b", re.I)),
)

_MEDIUM_RISK_PATTERNS = (
    ("update_workspace_action", re.compile(r"\b(update|change|edit|modify)\b.{0,80}\b(record|field|document|ticket|task|status|workspace)\b", re.I)),
    ("create_workspace_action", re.compile(r"\b(create|add)\b.{0,80}\b(task|ticket|event|record|document|workspace|issue)\b", re.I)),
    ("schedule_workspace_action", re.compile(r"\b(schedule|book|reschedule)\b.{0,80}\b(meeting|call|appointment|event|interview)\b", re.I)),
)


def classify_tool_intent(question: str) -> ToolDecision:
    text = " ".join(question.strip().split())

    if _READ_ONLY_PREFIX.search(text) or text.endswith("?"):
        explicit_action = any(
            pattern.search(text)
            for _, pattern in _HIGH_RISK_PATTERNS + _MEDIUM_RISK_PATTERNS
        )
        if not explicit_action:
            return ToolDecision(action=None, risk=RiskLevel.low, reason="Read-only knowledge request.")

    for action, pattern in _HIGH_RISK_PATTERNS:
        if pattern.search(text):
            return ToolDecision(
                action=action,
                risk=RiskLevel.high,
                reason="The request could cause an external side effect and requires human approval.",
            )

    for action, pattern in _MEDIUM_RISK_PATTERNS:
        if pattern.search(text):
            return ToolDecision(
                action=action,
                risk=RiskLevel.medium,
                reason="The request proposes a state-changing workspace action.",
            )

    return ToolDecision(action=None, risk=RiskLevel.low, reason="Read-only knowledge request.")
