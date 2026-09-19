---
name: codex-effort-router
description: Route engineering tasks to the minimum sufficient Codex reasoning effort and escalate only when runtime complexity requires it.
---

# Codex Effort Router

Before executing an engineering task:

1. Check whether a deterministic routing rule applies.
2. If the task is ambiguous, invoke the router implementation.
3. Route to exactly one reasoning tier: `low`, `medium`, or `high`.
4. Preserve the user's original intent when delegating.
5. Prefer the minimum sufficient effort.
6. Escalate if execution discovers materially greater complexity.
7. Record the route and escalation outcome when instrumentation is available.

Do not use `high` merely because it is available.
