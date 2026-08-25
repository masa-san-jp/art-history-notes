from __future__ import annotations

import unittest

from agent_harness.github import Issue
from agent_harness.queue import TaskQueue


def body(*, risk: str = "low", dependencies: list[int] | None = None) -> str:
    deps = dependencies or []
    return f'''<!-- agent-task:v1 -->
```yaml
version: 1
objective: test
deliverables:
  - path: docs/test.md
    expected: exists
scope:
  include: [docs/**]
non_goals: [none]
dependencies: {deps}
checks:
  - argv: [python, -V]
    timeout_seconds: 5
permissions:
  network: none
  external_write: false
limits:
  timeout_minutes: 1
  max_attempts: 1
  max_output_bytes: 1024
risk: {risk}
completion: [done]
```'''


class FakeClient:
    def __init__(self, issues: list[Issue]) -> None:
        self.issues = {issue.number: issue for issue in issues}

    def list_open_issues(self):
        return list(self.issues.values())

    def get_issue(self, number):
        return self.issues[number]


class QueueTests(unittest.TestCase):
    def issue(self, number: int, *, state: str = "open", labels: frozenset[str] = frozenset(), dependencies: list[int] | None = None, risk: str = "low") -> Issue:
        return Issue(number, f"Issue {number}", body(risk=risk, dependencies=dependencies), state, labels, f"2026-01-01T00:00:0{number}Z")

    def test_dependency_and_risk_order_are_deterministic(self) -> None:
        dependency = self.issue(1, state="closed", labels=frozenset({"agent-done"}))
        medium = self.issue(2, dependencies=[1], risk="medium")
        low = self.issue(3, dependencies=[1], risk="low")
        queue = TaskQueue(FakeClient([medium, low, dependency]))
        self.assertEqual([decision.issue.number for decision in queue.decisions() if decision.status == "ready"], [3, 2])

    def test_invalid_and_unfinished_dependencies_are_not_ready(self) -> None:
        unfinished = self.issue(1)
        waiting = self.issue(2, dependencies=[1])
        active = self.issue(3, labels=frozenset({"agent-running"}))
        queue = TaskQueue(FakeClient([unfinished, waiting, active]))
        decisions = {decision.issue.number: decision for decision in queue.decisions()}
        self.assertEqual(decisions[2].status, "waiting")
        self.assertEqual(decisions[3].status, "ineligible")

    def test_missing_dependency_is_loaded_and_closed_dependency_can_ready(self) -> None:
        dependent = self.issue(2, dependencies=[1])
        dependency = self.issue(1, state="closed", labels=frozenset({"agent-done"}))
        client = FakeClient([dependent, dependency])
        self.assertEqual(TaskQueue(client).next().issue.number, 2)
