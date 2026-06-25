"""
app/ai/guardrails.py — Input & Output safety validation layer

Detects:
  - Prompt injection / jailbreak attempts
  - PII (email, phone, SSN, credit card)
  - Malicious content patterns
  - Output toxicity (keyword-based, extensible)
  - JSON schema enforcement
"""
import re
from dataclasses import dataclass
from typing import Optional

import structlog

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Compiled patterns
# ---------------------------------------------------------------------------

_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
    re.compile(r"you\s+are\s+now\s+(a\s+)?(\w+\s+)?AI\s+without", re.I),
    re.compile(r"disregard\s+(all\s+)?(your\s+)?(prior|previous|above)", re.I),
    re.compile(r"(act|pretend|roleplay)\s+as\s+if\s+you\s+(have\s+no|are\s+not)", re.I),
    re.compile(r"DAN\s+mode", re.I),
    re.compile(r"jailbreak", re.I),
    re.compile(r"<\|im_start\|>|<\|im_end\|>|<\|system\|>", re.I),  # Token injection
]

_PII_PATTERNS = {
    "email": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
    "phone": re.compile(r"\b(\+\d{1,3}[\s.-])?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]?){13,16}\b"),
}

_TOXICITY_KEYWORDS = {
    "violence", "kill", "murder", "bomb", "terrorist",
    "suicide", "self-harm", "hack", "malware", "exploit",
}


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class GuardrailResult:
    passed: bool
    violations: list[str]
    sanitized_content: Optional[str] = None


# ---------------------------------------------------------------------------
# Input guardrails
# ---------------------------------------------------------------------------

def check_input(content: str) -> GuardrailResult:
    """
    Run all input guardrail checks.
    Returns GuardrailResult — .passed=False means block execution.
    """
    violations: list[str] = []

    # 1. Prompt injection / jailbreak
    for pattern in _INJECTION_PATTERNS:
        if pattern.search(content):
            violations.append(f"prompt_injection: matched pattern '{pattern.pattern[:40]}'")

    # 2. PII detection
    for pii_type, pattern in _PII_PATTERNS.items():
        if pattern.search(content):
            violations.append(f"pii_detected:{pii_type}")

    # 3. Toxicity keywords
    lower = content.lower()
    for kw in _TOXICITY_KEYWORDS:
        if kw in lower:
            violations.append(f"toxic_keyword:{kw}")

    passed = len(violations) == 0
    if not passed:
        logger.warning("Input guardrail violation", violations=violations)

    return GuardrailResult(passed=passed, violations=violations)


# ---------------------------------------------------------------------------
# Output guardrails
# ---------------------------------------------------------------------------

def check_output(content: str) -> GuardrailResult:
    """
    Run output safety checks on LLM response content.
    Less strict than input — no PII block (LLMs may legitimately reference data).
    """
    violations: list[str] = []

    lower = content.lower()
    for kw in _TOXICITY_KEYWORDS:
        if kw in lower:
            violations.append(f"output_toxic_keyword:{kw}")

    # Check for dangerous code patterns in output
    dangerous_code = [
        re.compile(r"import\s+os.*system\(", re.I | re.S),
        re.compile(r"subprocess\.call\(", re.I),
        re.compile(r"eval\(.*\)", re.I),
        re.compile(r"exec\(.*\)", re.I),
    ]
    for pattern in dangerous_code:
        if pattern.search(content):
            violations.append(f"dangerous_code_pattern: {pattern.pattern[:40]}")

    passed = len(violations) == 0
    if not passed:
        logger.warning("Output guardrail violation", violations=violations)

    return GuardrailResult(passed=passed, violations=violations)


# ---------------------------------------------------------------------------
# Sanitize content (strip PII for logging)
# ---------------------------------------------------------------------------

def sanitize_for_logging(content: str) -> str:
    """Replace PII with redacted placeholders for safe logging."""
    result = content
    for pii_type, pattern in _PII_PATTERNS.items():
        result = pattern.sub(f"[REDACTED:{pii_type.upper()}]", result)
    return result
