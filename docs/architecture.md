# Architecture

## Objective

Route Codex engineering tasks to the minimum reasoning effort that can complete them reliably.

## Components

### 1. Static Router

Handles deterministic cases without calling Jev.

Examples:
- git status
- branch creation
- simple commits
- mechanical file operations

### 2. Jev Decision Layer

Used only when the task is ambiguous enough that static routing is insufficient.

Proposed decision contract:

```json
{
  "task_type": "git | file_operation | repository_search | documentation | coding | debugging | architecture | review",
  "complexity": "trivial | moderate | complex",
  "requires_reasoning": true,
  "requires_repo_understanding": true,
  "requires_tradeoffs": false,
  "risk": "low | medium | high",
  "confidence": 0.91
}
```

### 3. Policy Engine

The policy engine—not Jev—selects the final effort.

Initial rules:
- `git` and mechanical `file_operation` -> low
- `architecture` -> high
- `debugging` with ambiguity -> high
- `requires_tradeoffs=true` -> high
- `complexity=moderate` -> medium
- low-confidence classifications floor to medium

### 4. Codex Workers

Target execution tiers:
- `low`
- `medium`
- `high`

Implementation can use Codex subagents with dedicated `model_reasoning_effort` values.

### 5. Escalation

Workers may escalate when runtime discoveries invalidate the initial route.

```text
LOW -> MEDIUM -> HIGH
```

Examples:
- supposedly mechanical change crosses API boundaries
- hidden test failures reveal broader behavior
- implementation requires architectural trade-offs

## Observability

Every routing decision should eventually record:

```json
{
  "task": "...",
  "source": "static | jev",
  "selected_effort": "medium",
  "confidence": 0.91,
  "escalated": false,
  "success": true,
  "duration_ms": 12000
}
```

Useful metrics:
- route distribution
- escalation rate
- incorrect-route rate
- success rate per tier
- latency per tier
- token/reasoning usage where observable
