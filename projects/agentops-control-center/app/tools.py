import re
from dataclasses import dataclass

from app.models import RiskLevel


@dataclass(frozen=True)
class ToolDecision:
    action: str | None
    risk: RiskLevel
    reason: str


HIGH_RISK_VERBS = ("send", "email", "delete", "remove", "refund", "pay", "purchase", "publish")
MEDIUM_RISK_VERBS = ("update", "create", "change", "schedule", "book")


def _requested_action(question: str, verbs: tuple[str, ...]) -> str | None:
    """Detect an execution request without treating a discussed action as authorization."""
    text = " ".join(question.strip().lower().split())
    verb_group = "|".join(re.escape(v) for v in verbs)
    patterns = [
        rf"^(?:please\s+)?(?P<verb>{verb_group})\b",
        rf"^(?:can|could|would|will)\s+you\s+(?:please\s+)?(?P<verb>{verb_group})\b",
        rf"^i\s+(?:want|need|would\s+like)\s+you\s+to\s+(?P<verb>{verb_group})\b",
        rf"^(?:go\s+ahead\s+and|proceed\s+to)\s+(?P<verb>{verb_group})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group("verb")

    if "refund" in verbs:
        if re.search(r"^(?:please\s+)?(?:issue|process|approve)\b.{0,60}\brefund\b", text):
            return "refund"
    return None


def classify_tool_intent(question: str) -> ToolDecision:
    high = _requested_action(question, HIGH_RISK_VERBS)
    if high:
        return ToolDecision(
            action=f"{high}_external_action",
            risk=RiskLevel.high,
            reason="The request could cause an external side effect and requires human approval.",
        )

    medium = _requested_action(question, MEDIUM_RISK_VERBS)
    if medium:
        return ToolDecision(
            action=f"{medium}_workspace_action",
            risk=RiskLevel.medium,
            reason="The request proposes a state-changing workspace action.",
        )

    return ToolDecision(action=None, risk=RiskLevel.low, reason="Read-only knowledge request.")
