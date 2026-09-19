from .models import RouteDecision


def route_static(task: str) -> RouteDecision | None:
    """Return an obvious route without model inference, otherwise None."""
    normalized = task.strip().lower()

    low_patterns = (
        "git status",
        "create a branch",
        "create branch",
        "make a commit",
        "create a commit",
        "git log",
    )

    if any(pattern in normalized for pattern in low_patterns):
        return RouteDecision(
            task_type="mechanical",
            effort="low",
            confidence=1.0,
            source="static",
            reason="Matched deterministic low-effort rule.",
        )

    return None
