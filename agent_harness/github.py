"""Small, shell-safe GitHub client boundary used by queue and delivery."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any, Protocol
import subprocess


class GitHubError(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None) -> None:
        self.status = status
        super().__init__(message)


@dataclass(frozen=True)
class Issue:
    number: int
    title: str
    body: str
    state: str
    labels: frozenset[str]
    created_at: str
    url: str = ""
    closed_at: str | None = None

    @classmethod
    def from_json(cls, value: dict[str, Any]) -> "Issue":
        return cls(
            number=int(value["number"]),
            title=str(value.get("title", "")),
            body=str(value.get("body") or ""),
            state=str(value.get("state", "open")).lower(),
            labels=frozenset(str(item["name"] if isinstance(item, dict) else item) for item in value.get("labels", [])),
            created_at=str(value.get("createdAt", value.get("created_at", ""))),
            url=str(value.get("url", "")),
            closed_at=value.get("closedAt", value.get("closed_at")),
        )


class GitHubClient(Protocol):
    def list_open_issues(self) -> list[Issue]: ...

    def get_issue(self, number: int) -> Issue: ...

    def add_label(self, number: int, label: str) -> None: ...

    def remove_label(self, number: int, label: str) -> None: ...

    def comment_issue(self, number: int, body: str) -> None: ...


class GhClient:
    """Use the authenticated gh CLI without invoking a shell."""

    def __init__(self, repository: str | None = None) -> None:
        self.repository = repository or self._discover_repository()

    @staticmethod
    def _discover_repository() -> str:
        result = _run(["gh", "repo", "view", "--json", "nameWithOwner"])
        try:
            return json.loads(result)["nameWithOwner"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise GitHubError(f"cannot determine repository: {exc}") from exc

    def _api(self, endpoint: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
        argv = ["gh", "api", endpoint, "--method", method]
        input_text = None
        if payload is not None:
            argv += ["--input", "-"]
            input_text = json.dumps(payload, ensure_ascii=False)
        raw = _run(argv, input_text=input_text)
        try:
            return json.loads(raw) if raw else None
        except json.JSONDecodeError as exc:
            raise GitHubError(f"GitHub returned invalid JSON: {exc}") from exc

    def list_open_issues(self) -> list[Issue]:
        raw = _run(["gh", "issue", "list", "--state", "open", "--label", "agent-task", "--limit", "100", "--json", "number,title,body,state,labels,createdAt,url"])
        try:
            values = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise GitHubError(f"cannot parse issue list: {exc}") from exc
        return [Issue.from_json(value) for value in values if "pull_request" not in value]

    def get_issue(self, number: int) -> Issue:
        raw = _run(["gh", "issue", "view", str(number), "--json", "number,title,body,state,labels,createdAt,url,closedAt"])
        try:
            return Issue.from_json(json.loads(raw))
        except (json.JSONDecodeError, TypeError, KeyError) as exc:
            raise GitHubError(f"cannot parse Issue #{number}: {exc}") from exc

    def add_label(self, number: int, label: str) -> None:
        _run(["gh", "issue", "edit", str(number), "--add-label", label])

    def remove_label(self, number: int, label: str) -> None:
        _run(["gh", "issue", "edit", str(number), "--remove-label", label])

    def comment_issue(self, number: int, body: str) -> None:
        _run(["gh", "issue", "comment", str(number), "--body", body])

    def find_or_create_pr(self, run: Any, *, objective: str, base_branch: str) -> dict[str, Any]:
        marker = f"<!-- agent-harness:run={run.run_id};issue={run.issue_number} -->"
        raw = _run(["gh", "pr", "list", "--head", run.branch, "--state", "all", "--json", "number,url,state,body"])
        values = json.loads(raw)
        for value in values:
            if marker in (value.get("body") or ""):
                return value
        title = f"agent(issue #{run.issue_number}): {objective.replace(chr(10), ' ')[:72]}"
        body = marker + "\n\n" + f"Automated delivery for run `{run.run_id}`.\n\nBase SHA: `{run.base_sha}`"
        created = _run(["gh", "pr", "create", "--base", base_branch, "--head", run.branch, "--title", title, "--body", body])
        url = created.strip().splitlines()[-1] if created.strip() else ""
        listed = json.loads(_run(["gh", "pr", "list", "--head", run.branch, "--state", "all", "--json", "number,url,state,body"]))
        for value in listed:
            if marker in (value.get("body") or ""):
                return value
        raise GitHubError(f"PR was created but could not be reconciled: {url}")

    def sync_issue(self, number: int, *, status: str, pr: dict[str, Any] | None, message: str) -> None:
        status_labels = ["agent-running", "agent-review", "agent-blocked", "agent-done"]
        target = {"running": "agent-running", "review": "agent-review", "blocked": "agent-blocked", "done": "agent-done"}.get(status)
        for label in status_labels:
            try:
                self.remove_label(number, label)
            except GitHubError:
                pass
        if target:
            self.add_label(number, target)
        marker = f"<!-- agent-harness:status issue={number} -->"
        body = marker + "\n\n" + message + (f"\n\nPR: {pr.get('url', '')}" if pr else "")
        comments = self._api(f"repos/{self.repository}/issues/{number}/comments?per_page=100") or []
        existing = next((comment for comment in comments if marker in (comment.get("body") or "")), None)
        if existing:
            self._api(f"repos/{self.repository}/issues/comments/{existing['id']}", method="PATCH", payload={"body": body})
        else:
            self._api(f"repos/{self.repository}/issues/{number}/comments", method="POST", payload={"body": body})

    def get_ref(self, ref: str) -> dict[str, Any] | None:
        try:
            return self._api(f"repos/{self.repository}/git/ref/{ref}")
        except GitHubError as exc:
            if exc.status == 404:
                return None
            raise

    def create_ref(self, ref: str, sha: str) -> None:
        self._api(f"repos/{self.repository}/git/refs", method="POST", payload={"ref": ref, "sha": sha})

    def update_ref(self, ref: str, sha: str, *, force: bool = False) -> None:
        self._api(f"repos/{self.repository}/git/refs/{ref}", method="PATCH", payload={"sha": sha, "force": force})

    def delete_ref(self, ref: str) -> None:
        self._api(f"repos/{self.repository}/git/refs/{ref}", method="DELETE")

    def get_commit_message(self, sha: str) -> str:
        value = self._api(f"repos/{self.repository}/git/commits/{sha}")
        return str(value.get("message", ""))

    def get_commit_tree(self, sha: str) -> str:
        value = self._api(f"repos/{self.repository}/git/commits/{sha}")
        return value["tree"]["sha"]

    def create_commit(self, *, message: str, tree: str, parent: str) -> str:
        value = self._api(f"repos/{self.repository}/git/commits", method="POST", payload={"message": message, "tree": tree, "parents": [parent]})
        return value["sha"]

    def close_issue(self, number: int) -> None:
        self._api(f"repos/{self.repository}/issues/{number}", method="PATCH", payload={"state": "closed"})

    def finalize_merged_pr(self, number: int) -> dict[str, Any]:
        raw = _run(["gh", "pr", "view", str(number), "--json", "number,url,state,mergedAt,body"])
        value = json.loads(raw)
        if value.get("state") != "MERGED" or not value.get("mergedAt"):
            raise GitHubError(f"PR #{number} is not merged")
        body = value.get("body") or ""
        marker = "<!-- agent-harness:run="
        if marker not in body or "issue=" not in body:
            raise GitHubError(f"PR #{number} has no agent-harness delivery marker")
        match = re.search(r"issue=(\d+)", body)
        if not match:
            raise GitHubError(f"PR #{number} has an invalid agent-harness marker")
        issue_number = int(match.group(1))
        self.sync_issue(issue_number, status="done", pr=value, message=f"PR #{number} merged; verified run finalized.")
        self.close_issue(issue_number)
        return {"pr_number": number, "issue_number": issue_number, "status": "done"}


def _run(argv: list[str], *, input_text: str | None = None) -> str:
    try:
        result = subprocess.run(argv, input=input_text, capture_output=True, text=True, check=False, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitHubError(f"GitHub command failed to start: {exc}") from exc
    if result.returncode:
        status = None
        if "HTTP 404" in result.stderr or "HTTP 404" in result.stdout:
            status = 404
        raise GitHubError(result.stderr.strip() or result.stdout.strip() or "GitHub command failed", status=status)
    return result.stdout
