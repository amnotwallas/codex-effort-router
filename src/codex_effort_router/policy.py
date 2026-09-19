from .models import Classification, RoutingSelection


def select_route(classification: Classification) -> RoutingSelection:
    if (
        classification.security_sensitive
        or classification.ambiguous
        or classification.cross_cutting
        or classification.complexity == "high"
        or classification.task_kind in {"architecture", "security"}
    ):
        return RoutingSelection("general", "general", "high")
    if classification.task_kind == "mechanical" and classification.complexity == "low":
        return RoutingSelection("mechanical", "fast", "low")
    if classification.task_kind == "explanation" and classification.complexity == "low":
        return RoutingSelection("general", "general", "low")
    return RoutingSelection("general", "general", "medium")
