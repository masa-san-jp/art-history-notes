"""Deterministic task selection and dependency resolution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .github import GitHubClient, Issue
from .task_contract import ContractValidationError, parse_contract


ACTIVE_LABELS = frozenset({"agent-running", "agent-review", "agent-blocked", "agent-done"})
RISK_ORDER = {"low": 0, "medium": 1, "high": 2}


@dataclass(frozen=True)
class QueueDecision:
    issue: Issue
    status: str
    reason: str | None = None


class TaskQueue:
    def __init__(self, client: GitHubClient) -> None:
        self.client = client

    def decisions(self, issues: Iterable[Issue] | None = None) -> list[QueueDecision]:
        candidates = list(issues if issues is not None else self.client.list_open_issues())
        by_number = {issue.number: issue for issue in candidates}
        decisions: list[QueueDecision] = []
        for issue in candidates:
            if ACTIVE_LABELS.intersection(issue.labels):
                decisions.append(QueueDecision(issue, "ineligible", "status label is active or terminal"))
                continue
            try:
                contract = parse_contract(issue.body)
            except ContractValidationError as exc:
                decisions.append(QueueDecision(issue, "blocked", "invalid contract: " + str(exc)))
                continue
            dependencies = contract.get("dependencies", [])
            missing = [number for number in dependencies if number not in by_number]
            if missing:
                missing_issues = [self.client.get_issue(number) for number in missing]
                by_number.update({item.number: item for item in missing_issues})
            dependency_issues = [by_number[number] for number in dependencies if number in by_number]
            if any(item.number == issue.number for item in dependency_issues):
                decisions.append(QueueDecision(issue, "blocked", "task depends on itself"))
                continue
            if any(item.state != "closed" or "agent-done" not in item.labels for item in dependency_issues):
                decisions.append(QueueDecision(issue, "waiting", "dependency is not closed with agent-done"))
                continue
            decisions.append(QueueDecision(issue, "ready"))
        ready = [decision for decision in decisions if decision.status == "ready"]
        ready.sort(key=lambda decision: (RISK_ORDER[parse_contract(decision.issue.body)["risk"]], decision.issue.created_at, decision.issue.number))
        others = [decision for decision in decisions if decision.status != "ready"]
        return ready + sorted(others, key=lambda decision: decision.issue.number)

    def next(self, issues: Iterable[Issue] | None = None) -> QueueDecision | None:
        return next((decision for decision in self.decisions(issues) if decision.status == "ready"), None)
