# Delivery and reconciliation

Delivery stages only the exact verified manifest. The post-stage index is
compared to that manifest before committing. The commit contains the run ID,
Issue number, and recorded base SHA. Empty manifests produce an explicit
no-change result and no empty commit.

Before pushing, an existing remote branch must point at the same run-marked
commit; a different SHA is a hard block and is never force-overwritten. PR
creation and status comments use stable run markers so retries reconcile before
creating anything. A merged PR is finalized by the `pull_request.closed`
workflow and only then closes the Issue. Blocked, failed, or unmerged results
remain open with evidence and a resume path.

`reconcile_issue` is safe to call repeatedly. It projects run state to the
single status comment and `agent-running`, `agent-review`, `agent-blocked`, or
`agent-done` label set without treating labels as the source of truth.
