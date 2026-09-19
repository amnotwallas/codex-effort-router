# Codex Effort Router

Adaptive routing layer for Codex tasks. The goal is to select the minimum sufficient reasoning effort (`low`, `medium`, or `high`) for each engineering task, using deterministic rules first and Jev for ambiguous cases.

## Problem

Coding-agent workflows often waste higher reasoning effort on mechanical tasks such as creating branches, checking git status, or making straightforward commits. Other tasks—debugging, architecture, cross-cutting refactors, or complex PR synthesis—benefit from deeper reasoning.

This project routes tasks to the cheapest sufficient effort and allows escalation when unexpected complexity appears.

## Core idea

```text
User task
   |
   v
Static rules
   | obvious
   +----------> low/medium/high
   |
   | ambiguous
   v
Jev classifier
   |
   v
Policy engine
   |
   +--> low
   +--> medium
   +--> high

Selected worker can escalate when needed.
```

## Initial principles

1. Rules before model calls for obvious tasks.
2. Jev judges ambiguous tasks; application code owns the final policy.
3. Prefer the minimum sufficient reasoning effort.
4. Escalation is allowed; unnecessary de-escalation during execution is not.
5. Log routing decisions so the policy can be evaluated with real usage.

## Examples

| Task | Default route |
|---|---|
| `git status` | low |
| create branch | low |
| straightforward commit | low |
| mechanical rename/move | low |
| localized implementation | medium |
| generate `PR.md` from a small clear diff | medium |
| complex PR synthesis across many subsystems | high |
| ambiguous debugging / root-cause analysis | high |
| architecture / cross-cutting refactor | high |

## Status

Design/bootstrap stage. Next milestone: implement a deterministic router and define the Jev decision contract.
