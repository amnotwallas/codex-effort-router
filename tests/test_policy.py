import pytest

from codex_effort_router.models import Classification, RoutingSelection
from codex_effort_router.policy import select_route


@pytest.mark.parametrize(
    ("classification", "expected"),
    [
        (Classification("mechanical", "low"), RoutingSelection("mechanical", "fast", "low")),
        (Classification("explanation", "low"), RoutingSelection("general", "general", "low")),
        (Classification("documentation", "medium"), RoutingSelection("general", "general", "medium")),
        (Classification("debugging", "high", ambiguous=True), RoutingSelection("general", "general", "high")),
        (Classification("architecture", "high"), RoutingSelection("general", "general", "high")),
    ],
)
def test_policy_selects_agent_model_profile_and_effort_independently(
    classification: Classification, expected: RoutingSelection
) -> None:
    assert select_route(classification) == expected


def test_general_model_can_use_low_effort() -> None:
    selection = select_route(Classification("explanation", "low"))

    assert selection.model_profile == "general"
    assert selection.reasoning_effort == "low"


def test_high_risk_signals_require_general_high() -> None:
    for classification in (
        Classification("security", "low", security_sensitive=True),
        Classification("implementation", "medium", cross_cutting=True),
        Classification("implementation", "high"),
    ):
        assert select_route(classification) == RoutingSelection("general", "general", "high")


def test_ambiguous_mechanical_work_is_not_sent_to_fast_worker() -> None:
    assert select_route(Classification("mechanical", "low", ambiguous=True)) == RoutingSelection(
        "general", "general", "high"
    )
