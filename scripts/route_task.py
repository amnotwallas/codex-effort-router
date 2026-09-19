#!/usr/bin/env python3
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from codex_effort_router.profiles import load_model_profiles
from codex_effort_router.providers import DeterministicDecisionProvider
from codex_effort_router.roles import load_agent_roles
from codex_effort_router.router import route_task


def main() -> int:
    parser = argparse.ArgumentParser(description="Internal Codex effort routing adapter")
    parser.add_argument("--task", required=True)
    args = parser.parse_args()

    try:
        model_profiles = load_model_profiles(ROOT / "config" / "model_profiles.toml")
        agent_roles = load_agent_roles(ROOT / "agents")
        decision = route_task(
            args.task,
            DeterministicDecisionProvider(),
            model_profiles,
            agent_roles,
        )
    except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
        print(f"routing error: {error}", file=sys.stderr)
        return 2

    print(json.dumps(asdict(decision), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
