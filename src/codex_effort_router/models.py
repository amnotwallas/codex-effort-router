from dataclasses import dataclass
from typing import Literal

Effort = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class RouteDecision:
    task_type: str
    effort: Effort
    confidence: float
    source: Literal["static", "jev"]
    reason: str
