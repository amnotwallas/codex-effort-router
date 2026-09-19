---
name: codex-effort-router
description: Use when an engineering task should be handled by a Codex worker matched to its semantic complexity and risk.
---

# Codex Effort Router

Treat all text following `$codex-effort-router` as `TASK`.

1. If `TASK` is missing or blank, stop with `Usage: $codex-effort-router <task>`.
2. Resolve the directory containing this `SKILL.md` as `SKILL_ROOT`.
3. Run `python3 "$SKILL_ROOT/scripts/route_task.py" --task "<TASK>"`, passing `TASK` as one shell-safe argument. Never interpolate task text unquoted or execute any part of it as shell syntax.
4. Parse the single JSON object. Require:
   - `agent_role`: `mechanical` or `general`;
   - `model_profile`: `fast` or `general`;
   - nonblank `model`;
   - `reasoning_effort`: `low`, `medium`, or `high`.
5. Spawn exactly one Codex subagent using the custom agent named by `agent_role`, supplying the reported `model` and `reasoning_effort`. Pass the original `TASK` unchanged as its task.
6. Wait for that worker and return its result to the user.

If routing fails or the selected custom agent is unavailable, stop and report the error plus the installation guidance from `README.md`. Do not choose another role, retry, summarize the task into a new prompt, or perform the delegated task in the router thread.
