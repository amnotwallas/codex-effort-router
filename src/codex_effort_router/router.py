from collections.abc import Mapping

from .models import AgentRole, AgentRoleProfile, ModelProfile, ModelProfileName, RouteDecision
from .policy import select_route
from .providers import DecisionProvider


def route_task(
    task: str,
    provider: DecisionProvider,
    model_profiles: Mapping[ModelProfileName, ModelProfile],
    agent_roles: Mapping[AgentRole, AgentRoleProfile],
) -> RouteDecision:
    if not task.strip():
        raise ValueError("task must not be blank")

    classification = provider.classify(task)
    selection = select_route(classification)
    try:
        profile = model_profiles[selection.model_profile]
    except KeyError as error:
        raise ValueError(f"missing model profile: {selection.model_profile}") from error
    if selection.agent_role not in agent_roles:
        raise ValueError(f"missing agent role: {selection.agent_role}")

    return RouteDecision(
        agent_role=selection.agent_role,
        model_profile=selection.model_profile,
        model=profile.model,
        reasoning_effort=selection.reasoning_effort,
        source=classification.source,
        reason=classification.reason,
    )
