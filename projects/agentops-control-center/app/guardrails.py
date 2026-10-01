from __future__ import annotations

import re

_PATTERNS = (
    re.compile(r"\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions?\b", re.I),
    re.compile(r"\bsystem\s+prompt\b", re.I),
    re.compile(r"\b(?:reveal|print|show|expose)\b.{0,60}\b(?:secret|credential|api\s*key|password)\b", re.I),
)


def detect_untrusted_instructions(text: str) -> list[str]:
    warnings: list[str] = []
    if any(pattern.search(text) for pattern in _PATTERNS):
        warnings.append("possible_prompt_injection")
    return warnings
