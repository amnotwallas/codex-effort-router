from codex_effort_router.router import route_static


def test_git_status_routes_low() -> None:
    decision = route_static("Run git status")
    assert decision is not None
    assert decision.effort == "low"
    assert decision.source == "static"


def test_ambiguous_task_defers() -> None:
    assert route_static("Investigate why the API occasionally loses sessions") is None
