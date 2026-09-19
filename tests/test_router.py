from codex_effort_router.models import (
    AgentRoleProfile,
    Classification,
    ModelProfile,
    RouteDecision,
)
from codex_effort_router.router import route_task


class FixedProvider:
    def __init__(self, classification: Classification) -> None:
        self.classification = classification
        self.received_task: str | None = None

    def classify(self, task: str) -> Classification:
        self.received_task = task
        return self.classification


MODEL_PROFILES = {
    "fast": ModelProfile("fast", "fast-model"),
    "general": ModelProfile("general", "general-model"),
}
AGENT_ROLES = {
    "mechanical": AgentRoleProfile("mechanical", "Mechanical role.", "Execute directly."),
    "general": AgentRoleProfile("general", "General role.", "Reason carefully."),
}


def test_router_preserves_task_and_resolves_independent_dimensions() -> None:
    task = '  Explain the literal "$(not-shell)"\nwithout changing spacing  '
    provider = FixedProvider(Classification("explanation", "low", source="jev"))

    decision = route_task(task, provider, MODEL_PROFILES, AGENT_ROLES)

    assert provider.received_task == task
    assert decision == RouteDecision(
        agent_role="general",
        model_profile="general",
        model="general-model",
        reasoning_effort="low",
        source="jev",
        reason="",
    )


def test_model_mapping_changes_resolved_model_only() -> None:
    task = "Explain this localized function"
    provider = FixedProvider(Classification("explanation", "low"))
    changed_profiles = {
        **MODEL_PROFILES,
        "general": ModelProfile("general", "changed-general-model"),
    }

    original = route_task(task, provider, MODEL_PROFILES, AGENT_ROLES)
    changed = route_task(task, provider, changed_profiles, AGENT_ROLES)

    assert original.model == "general-model"
    assert changed.model == "changed-general-model"
    assert changed.model_profile == original.model_profile == "general"
    assert changed.reasoning_effort == original.reasoning_effort == "low"


def test_router_rejects_blank_task_before_calling_provider() -> None:
    provider = FixedProvider(Classification("unknown", "medium"))

    try:
        route_task("   \n", provider, MODEL_PROFILES, AGENT_ROLES)
    except ValueError as error:
        assert str(error) == "task must not be blank"
    else:
        raise AssertionError("blank task was accepted")

    assert provider.received_task is None


def test_router_rejects_missing_selected_model_profile() -> None:
    provider = FixedProvider(Classification("explanation", "low"))

    try:
        route_task("Explain this code", provider, {}, AGENT_ROLES)
    except ValueError as error:
        assert str(error) == "missing model profile: general"
    else:
        raise AssertionError("missing model profile was accepted")
