from pathlib import Path

import pytest

from codex_effort_router.providers import DeterministicDecisionProvider


@pytest.mark.parametrize(
    ("task", "task_kind", "complexity"),
    [
        ("Run git status", "mechanical", "low"),
        ("Create a branch", "mechanical", "low"),
        ("Do a simple commit", "mechanical", "low"),
        ("Format these Python files", "mechanical", "low"),
        ("Apply these mechanical edits", "mechanical", "low"),
        ("Search for references", "mechanical", "low"),
        ("Explain this localized code", "explanation", "low"),
        ("Update the README architecture section", "documentation", "medium"),
        ("Write a PR description", "documentation", "medium"),
        ("Implement a localized validation change", "implementation", "medium"),
        ("Perform a moderate refactor", "implementation", "medium"),
        ("Write a straightforward code review", "review", "medium"),
        ("Design the service architecture", "architecture", "high"),
    ],
)
def test_deterministic_provider_classifies_semantics(
    task: str, task_kind: str, complexity: str
) -> None:
    result = DeterministicDecisionProvider().classify(task)

    assert result.task_kind == task_kind
    assert result.complexity == complexity
    assert result.source == "deterministic"


def test_ambiguous_debugging_is_marked_high_and_ambiguous() -> None:
    result = DeterministicDecisionProvider().classify(
        "Investigate why sessions occasionally disappear"
    )

    assert result.task_kind == "debugging"
    assert result.complexity == "high"
    assert result.ambiguous is True


def test_security_signal_wins_over_simple_search_signal() -> None:
    result = DeterministicDecisionProvider().classify(
        "Search for authentication vulnerabilities"
    )

    assert result.task_kind == "security"
    assert result.security_sensitive is True


def test_plural_vulnerability_search_is_security_sensitive() -> None:
    result = DeterministicDecisionProvider().classify("Search for vulnerabilities")

    assert result.task_kind == "security"
    assert result.security_sensitive is True


@pytest.mark.parametrize(
    ("task", "task_kind", "complexity"),
    [
        (
            "Investigate intermittent session loss and update the README",
            "debugging",
            "high",
        ),
        ("Run git status and implement pagination", "implementation", "medium"),
        ("Review the rename logic", "review", "medium"),
    ],
)
def test_stronger_signals_win_over_mechanical_or_documentation_phrases(
    task: str, task_kind: str, complexity: str
) -> None:
    result = DeterministicDecisionProvider().classify(task)

    assert result.task_kind == task_kind
    assert result.complexity == complexity


def test_semantic_provider_contains_no_concrete_model_ids() -> None:
    source = Path(__file__).resolve().parents[1] / "src" / "codex_effort_router" / "providers.py"

    assert "gpt-" not in source.read_text(encoding="utf-8")
