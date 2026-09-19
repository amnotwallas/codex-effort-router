from typing import Protocol

from .models import Classification


class DecisionProvider(Protocol):
    def classify(self, task: str) -> Classification: ...


class DeterministicDecisionProvider:
    def classify(self, task: str) -> Classification:
        normalized = " ".join(task.lower().split())

        # ponytail: phrase matching is the V1 fallback; Jev becomes the primary classifier when available.
        if any(
            phrase in normalized
            for phrase in (
                "security",
                "vulnerability",
                "vulnerabilities",
                "authentication",
                "authorization",
                "permission",
                "secret",
            )
        ):
            return Classification(
                "security",
                "high",
                security_sensitive=True,
                reason="Security-sensitive work requires the high worker.",
            )
        if any(phrase in normalized for phrase in ("root cause", "root-cause")):
            return Classification(
                "debugging",
                "high",
                ambiguous=True,
                reason="Root-cause analysis requires the high worker.",
            )
        if any(
            phrase in normalized
            for phrase in (
                "investigate",
                "debug",
                "occasionally",
                "intermittent",
                "race condition",
            )
        ):
            return Classification(
                "debugging",
                "high",
                ambiguous=True,
                reason="Ambiguous debugging requires the high worker.",
            )
        if any(
            phrase in normalized
            for phrase in (
                "documentation",
                "readme",
                "pr description",
                "pull request description",
            )
        ):
            return Classification(
                "documentation",
                "medium",
                reason="Bounded documentation work requires the medium worker.",
            )
        if any(phrase in normalized for phrase in ("explain ", "explanation")):
            return Classification(
                "explanation",
                "low",
                reason="Localized explanation work requires general capability at low effort.",
            )
        if any(
            phrase in normalized
            for phrase in ("architecture", "architect", "cross-cutting", "cross cutting")
        ):
            return Classification(
                "architecture",
                "high",
                cross_cutting=True,
                reason="Architectural or cross-cutting work requires the high worker.",
            )
        if any(phrase in normalized for phrase in ("code review", "review")):
            return Classification(
                "review",
                "medium",
                reason="A straightforward review requires the medium worker.",
            )
        if any(phrase in normalized for phrase in ("implement", "add ", "fix ", "refactor")):
            return Classification(
                "implementation",
                "medium",
                reason="Localized implementation requires the medium worker.",
            )
        if any(
            phrase in normalized
            for phrase in (
                "git status",
                "git log",
                "create a branch",
                "create branch",
                "switch branch",
                "make a commit",
                "create a commit",
                "simple commit",
                "commit ",
                "format ",
                "rename ",
                "move file",
                "mechanical edit",
                "search for",
                "simple search",
                "find references",
                "find file",
            )
        ):
            return Classification(
                "mechanical",
                "low",
                reason="A deterministic mechanical rule matched.",
            )
        return Classification(
            "unknown",
            "medium",
            reason="Unknown work defaults to the medium worker.",
        )
