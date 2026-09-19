import json
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "route_task.py"


def test_script_emits_profile_and_effort_resolved_json() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--task", "Run git status"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    with (ROOT / "config" / "model_profiles.toml").open("rb") as profile_file:
        model_profiles = tomllib.load(profile_file)

    assert result.returncode == 0
    assert result.stderr == ""
    assert json.loads(result.stdout) == {
        "agent_role": "mechanical",
        "model": model_profiles["fast"]["model"],
        "model_profile": "fast",
        "reason": "A deterministic mechanical rule matched.",
        "reasoning_effort": "low",
        "source": "deterministic",
    }


def test_script_supports_general_low_combination() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--task", "Explain this localized function"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    decision = json.loads(result.stdout)
    assert decision["model_profile"] == "general"
    assert decision["reasoning_effort"] == "low"


def test_script_preserves_shell_metacharacters_as_task_data(tmp_path: Path) -> None:
    marker = tmp_path / "router-must-not-run"
    task = f'Update docs for "$(touch {marker})"\nwith spacing'
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--task", task],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    decision = json.loads(result.stdout)
    assert decision["model_profile"] == "general"
    assert decision["reasoning_effort"] == "medium"
    assert not marker.exists()


def test_script_rejects_blank_task_without_json() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--task", "  \n"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert "task must not be blank" in result.stderr
