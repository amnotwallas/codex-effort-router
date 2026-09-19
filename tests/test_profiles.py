from pathlib import Path
import tomllib

import pytest

from codex_effort_router.profiles import load_model_profiles
from codex_effort_router.roles import load_agent_roles

ROOT = Path(__file__).resolve().parents[1]


def _write_model_profiles(directory: Path, fast: str, general: str) -> None:
    (directory / "model_profiles.toml").write_text(
        f'''[fast]
model = "{fast}"

[general]
model = "{general}"
''',
        encoding="utf-8",
    )


def test_model_profiles_are_complete_and_do_not_use_astra() -> None:
    profiles = load_model_profiles(ROOT / "config" / "model_profiles.toml")

    assert set(profiles) == {"fast", "general"}
    assert profiles["fast"].model == "gpt-5.6-luna"
    assert profiles["general"].model == "gpt-5.6-sol"
    assert all("astra" not in profile.model.lower() for profile in profiles.values())


def test_model_mapping_is_configurable_without_policy_changes(tmp_path: Path) -> None:
    _write_model_profiles(tmp_path, "local-fast-model", "local-general-model")

    profiles = load_model_profiles(tmp_path / "model_profiles.toml")

    assert profiles["fast"].model == "local-fast-model"
    assert profiles["general"].model == "local-general-model"


def test_missing_model_profile_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "model_profiles.toml").write_text(
        '[fast]\nmodel = "fast"\n', encoding="utf-8"
    )

    with pytest.raises(ValueError, match="missing model profile: general"):
        load_model_profiles(tmp_path / "model_profiles.toml")


def test_blank_model_is_rejected(tmp_path: Path) -> None:
    _write_model_profiles(tmp_path, "", "general")

    with pytest.raises(ValueError, match="fast model profile must declare a nonblank model"):
        load_model_profiles(tmp_path / "model_profiles.toml")


def test_execution_roles_are_separate_from_model_profiles() -> None:
    roles = load_agent_roles(ROOT / "agents")

    assert set(roles) == {"mechanical", "general"}
    assert all(role.developer_instructions for role in roles.values())
    for path in (ROOT / "agents").glob("*.toml"):
        with path.open("rb") as role_file:
            fields = tomllib.load(role_file)
        assert "model" not in fields
        assert "model_reasoning_effort" not in fields
