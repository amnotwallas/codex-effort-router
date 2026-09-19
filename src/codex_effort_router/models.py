from dataclasses import dataclass
from typing import Literal

AgentRole = Literal["mechanical", "general"]
ModelProfileName = Literal["fast", "general"]
TaskKind = Literal[
    "mechanical",
    "explanation",
    "implementation",
    "documentation",
    "review",
    "debugging",
    "architecture",
    "security",
    "unknown",
]
Complexity = Literal["low", "medium", "high"]
Source = Literal["deterministic", "jev", "deterministic-fallback"]
ReasoningEffort = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class Classification:
    task_kind: TaskKind
    complexity: Complexity
    ambiguous: bool = False
    cross_cutting: bool = False
    security_sensitive: bool = False
    reason: str = ""
    source: Source = "deterministic"


@dataclass(frozen=True)
class RoutingSelection:
    agent_role: AgentRole
    model_profile: ModelProfileName
    reasoning_effort: ReasoningEffort


@dataclass(frozen=True)
class ModelProfile:
    model_profile: ModelProfileName
    model: str


@dataclass(frozen=True)
class AgentRoleProfile:
    agent_role: AgentRole
    description: str
    developer_instructions: str


@dataclass(frozen=True)
class RouteDecision:
    agent_role: AgentRole
    model_profile: ModelProfileName
    model: str
    reasoning_effort: ReasoningEffort
    source: Source
    reason: str
