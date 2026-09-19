# Independent Model/Effort Routing Refactor

## Goal

Replace coupled `low`/`medium`/`high` worker profiles with independent execution roles, model profiles, and reasoning effort while preserving the semantic provider boundary and unchanged-task delegation.

## Minimal implementation sequence

1. RED: replace policy tests with `RoutingSelection` expectations for `fast+low`, `general+low`, `general+medium`, and `general+high`.
2. RED: replace profile tests with model-profile TOML and role-only agent TOML contracts, including configurable model mappings and no Astra configuration.
3. RED: update router tests for `agent_role`, `model_profile`, resolved model, independent effort, model mapping changes, blank tasks, and unchanged task text.
4. RED: update adapter tests for the new JSON shape, general-low routing, hostile input, and blank input.
5. GREEN: implement domain types, policy selection, model-profile loader, role loader, router composition, and adapter loading.
6. GREEN: add `config/model_profiles.toml`, replace the three tiered agent templates with `agents/mechanical.toml` and `agents/general.toml`, and update skill/docs/spec.
7. Verify: run the full pytest suite, skill validation, adapter route matrix, TOML parsing, model-ID audit, `.env` audit, and `git diff --check`.

## File changes

Keep `providers.py` and its deterministic semantic rules model-agnostic. Modify `models.py`, `policy.py`, `profiles.py`, `router.py`, `scripts/route_task.py`, tests, `SKILL.md`, `README.md`, and this spec/plan. Add `roles.py`, `config/model_profiles.toml`, and role templates. Remove `agents/low.toml`, `agents/medium.toml`, and `agents/high.toml`.

## Interfaces

```python
def select_route(classification: Classification) -> RoutingSelection: ...
def load_model_profiles(path: Path) -> dict[ModelProfileName, ModelProfile]: ...
def load_agent_roles(path: Path) -> dict[AgentRole, AgentRoleProfile]: ...
def route_task(task, provider, model_profiles, agent_roles) -> RouteDecision: ...
```

`Classification` contains no model or effort selection. `RoutingSelection` contains role, model profile, and effort. `ModelProfile` maps only profile name to model. `RouteDecision` combines the selected role, profile, resolved model, effort, source, and reason.

## Configuration

```toml
[fast]
model = "gpt-5.6-luna"

[general]
model = "gpt-5.6-sol"
```

Agent TOMLs contain `name`, `description`, and `developer_instructions` only. No Astra model is used.

## Acceptance

- Semantic provider remains model-agnostic and deterministic fallback remains available.
- Policy produces all four supported combinations: `fast+low`, `general+low`, `general+medium`, `general+high`.
- Changing the model-profile TOML changes only the resolved model.
- Role configuration remains independent of model and effort.
- Original tasks, shell-hostile data, visible errors, `.env` protection, and no-Jev-network behavior remain intact.
- Tests pass, docs match the architecture, and no commit or push occurs.
