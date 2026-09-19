# Codex Effort Router Design

## Purpose

`$codex-effort-router <task>` is an interactive Codex skill. It classifies the task semantically, applies local routing policy, resolves an execution role plus an independent model profile and reasoning effort, delegates the original task once, and returns that worker's result.

The internal `scripts/route_task.py` adapter is testable infrastructure, not a standalone user-facing CLI.

## Flow

```text
task
  -> DecisionProvider / future Jev semantic Classification
  -> local routing policy
  -> agent_role + model_profile + reasoning_effort
  -> model_profiles.toml resolves model_profile to model
  -> one Codex subagent
```

Classification contains task kind, complexity, ambiguity, breadth, security, reason, and source. It contains no model profile, model ID, or reasoning-effort choice. A future `JevDecisionProvider` implements the same protocol and reads `JEV_API_KEY` from the process environment only; this iteration uses deterministic classification and does not make a network call.

## Independent routing dimensions

The V1 model profiles are:

| Model profile | Model |
|---|---|
| `fast` | `gpt-5.6-luna` |
| `general` | `gpt-5.6-sol` |

Reasoning effort is independently selected from `low`, `medium`, or `high`. The policy currently produces these supported combinations:

| Task family | Agent role | Model profile | Effort |
|---|---|---|---|
| Mechanical Git/search work | `mechanical` | `fast` | `low` |
| Localized explanation | `general` | `general` | `low` |
| Bounded docs/implementation/review | `general` | `general` | `medium` |
| Ambiguous debugging, architecture, root cause, security | `general` | `general` | `high` |

The policy returns a model-agnostic `RoutingSelection`. Profile loading resolves only the selected model profile to a model ID. Therefore changing a TOML model changes the final model without changing semantic classification or policy.

## Execution roles

`agents/mechanical.toml` and `agents/general.toml` define role names, descriptions, and developer instructions. They do not contain model IDs or reasoning-effort fields. The skill supplies the route decision's `agent_role`, `model`, and `reasoning_effort` when creating the Codex subagent.

Codex loads project roles from `.codex/agents/`. The repository keeps `agents/` as the distributable source:

```bash
mkdir -p .codex/agents
cp agents/{mechanical,general}.toml .codex/agents/
```

## Domain model

```python
AgentRole = Literal["mechanical", "general"]
ModelProfileName = Literal["fast", "general"]
ReasoningEffort = Literal["low", "medium", "high"]

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
class RouteDecision:
    agent_role: AgentRole
    model_profile: ModelProfileName
    model: str
    reasoning_effort: ReasoningEffort
    source: Source
    reason: str
```

## Policy and configuration boundaries

`policy.py` exposes `select_route(classification) -> RoutingSelection` and contains no model strings. `profiles.py` loads and validates `[fast]` and `[general]` from `config/model_profiles.toml`. `roles.py` loads and validates execution-role TOML files and rejects model/effort fields there. `router.py` composes provider, policy, model profiles, and roles into `RouteDecision`.

The adapter loads both configuration boundaries, rejects blank tasks and invalid configuration visibly, and emits one JSON decision. It never executes the task.

## Guarantees

- The original task reaches the provider and delegated subagent unchanged.
- Shell metacharacters, quotes, newlines, and spacing remain task data.
- Semantic provider code has no concrete model IDs.
- `.env` is ignored; future Jev credentials are environment-only and never logged or stored.
- Deterministic classification remains the current provider and future fallback.
- Missing/invalid profiles and roles fail nonzero with an explicit error.
- No standalone console entry point is added.

## Acceptance criteria

1. The skill documents and performs the route-and-delegate flow.
2. The provider boundary remains model-agnostic.
3. Policy can produce `fast+low`, `general+low`, `general+medium`, and `general+high`.
4. Model IDs are configurable only in `config/model_profiles.toml`; canonical config contains no Astra model.
5. Role TOMLs contain execution instructions without model or effort coupling.
6. Model-profile changes alter only resolved model values.
7. Existing unchanged-task and hostile-input guarantees pass.
8. `.env` remains ignored and no Jev network call is implemented.
9. The complete test suite passes without warnings, and no commit or push is performed.
