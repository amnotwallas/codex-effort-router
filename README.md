# Codex Effort Router

Route an engineering task from an interactive Codex session to an execution role, model profile, and reasoning effort. The project is a Codex skill; `scripts/route_task.py` is an internal JSON adapter, not the end-user interface.

## Flow

`$codex-effort-router <task>` → semantic `DecisionProvider` classification → local routing policy → `agent_role` + `model_profile` + `reasoning_effort` → configured model → one delegated subagent → worker result.

Jev remains model-agnostic. Concrete model IDs live only in `config/model_profiles.toml`.

## Model profiles

| Profile | Model |
|---|---|
| `fast` | `gpt-5.6-luna` |
| `general` | `gpt-5.6-sol` |

Edit `config/model_profiles.toml` to change model IDs; no provider or policy change is required.

## Execution roles

`agents/mechanical.toml` and `agents/general.toml` contain execution behavior and developer instructions only. They do not select a model or reasoning effort. The router supplies those values dynamically.

## Supported routes

| Work | Agent role | Model profile | Reasoning |
|---|---|---|---|
| Git operations, branches, commits, formatting, simple searches | `mechanical` | `fast` | `low` |
| Localized code explanation | `general` | `general` | `low` |
| PR description, localized implementation, straightforward review | `general` | `general` | `medium` |
| Ambiguous debugging, root-cause analysis, architecture, security | `general` | `general` | `high` |

## Install

Install or symlink this repository as a Codex skill at `.agents/skills/codex-effort-router` for one repository or `~/.agents/skills/codex-effort-router` globally.

Copy project-scoped execution roles:

```bash
mkdir -p .codex/agents
cp agents/{mechanical,general}.toml .codex/agents/
```

For global roles, copy the files to `~/.codex/agents/`. Symlinks are preferable during development; copied roles must be refreshed after instruction changes. Restart Codex if newly installed skills or roles are not detected.

## Use

```text
$codex-effort-router investigate why API sessions occasionally disappear
```

The skill passes the task unchanged to the selected role and supplies the resolved model and effort independently.

## Repository structure

- `SKILL.md`: interactive routing and delegation workflow.
- `agents/`: execution-role TOML files without model bindings.
- `config/model_profiles.toml`: configurable model-profile mapping.
- `scripts/route_task.py`: internal JSON routing adapter.
- `src/codex_effort_router/`: semantic models, provider boundary, policy, role loading, model-profile loading, and composition.
- `tests/`: policy, provider, role/profile, router, and adapter behavior.

## Jev integration remaining

Implement `JevDecisionProvider` against the existing protocol, read `JEV_API_KEY` from the process environment, validate Jev's semantic response into `Classification`, and use deterministic fallback for missing credentials, transport failure, or invalid responses. Never put model names in the Jev schema and never store or log the API key.

## Development

```bash
pytest -q
python3 scripts/route_task.py --task "Run git status"
```
