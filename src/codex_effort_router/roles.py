from pathlib import Path
import tomllib
from typing import cast

from .models import AgentRole, AgentRoleProfile

AGENT_ROLES: tuple[AgentRole, ...] = ("mechanical", "general")


def load_agent_roles(agents_dir: Path) -> dict[AgentRole, AgentRoleProfile]:
    roles: dict[AgentRole, AgentRoleProfile] = {}
    for agent_role in AGENT_ROLES:
        path = agents_dir / f"{agent_role}.toml"
        if not path.is_file():
            raise ValueError(f"missing agent role: {agent_role}")
        with path.open("rb") as role_file:
            data = tomllib.load(role_file)

        if data.get("name") != agent_role:
            raise ValueError(f"{path.name} must declare name = '{agent_role}'")
        if "model" in data or "model_reasoning_effort" in data:
            raise ValueError(f"{path.name} must not configure model or reasoning effort")
        description = data.get("description")
        instructions = data.get("developer_instructions")
        if not isinstance(description, str) or not description.strip():
            raise ValueError(f"{path.name} must declare a nonblank description")
        if not isinstance(instructions, str) or not instructions.strip():
            raise ValueError(
                f"{path.name} must declare nonblank developer_instructions"
            )

        roles[agent_role] = AgentRoleProfile(
            agent_role=cast(AgentRole, agent_role),
            description=description,
            developer_instructions=instructions,
        )
    return roles
