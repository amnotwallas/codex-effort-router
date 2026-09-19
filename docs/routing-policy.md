# Routing Policy v0

## Low

Use for narrow, deterministic, reversible tasks with little or no ambiguity.

Typical cases:
- git status/log/diff inspection
- create/switch branch
- stage files
- straightforward commit
- rename or move files
- formatting
- simple repository lookup
- execute already-decided mechanical changes

## Medium

Use for bounded engineering tasks that require local reasoning or synthesis.

Typical cases:
- localized feature implementation
- straightforward bug fix with known root cause
- code explanation across a few files
- documentation synthesis
- small/medium `PR.md`
- routine code review
- test creation for understood behavior

## High

Use when ambiguity, system-wide consequences, or substantial trade-offs are present.

Typical cases:
- root-cause analysis
- architecture
- cross-cutting refactors
- concurrency/state consistency issues
- security-sensitive changes
- complex performance investigations
- large PR synthesis spanning multiple subsystems
- unclear failures requiring repository-wide investigation

## Confidence policy

Proposed initial thresholds:
- >= 0.85: accept Jev classification
- 0.60-0.84: floor result to at least medium
- < 0.60: route to high until enough data exists to tune this behavior

These thresholds are hypotheses and must be validated empirically.
