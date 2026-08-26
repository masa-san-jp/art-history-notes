# External-agent repository harness

このディレクトリは、リポジトリの外で動くAgentがこのrepoを安全に変更し、
機械的な証拠を残すための入口です。リポジトリはAgentを起動しません。

## 最短手順

    uv sync --locked
    uv run --locked python tools/agent_doctor.py --json
    uv run --locked python tools/agent_task.py validate --file TASK --json
    uv run --locked python tools/agent_session.py begin --task-file TASK --output .agent-local/SESSION.json
    uv run --locked python tools/agent_verify.py --task-file TASK --session .agent-local/SESSION.json --json

詳細は次を順に読みます。

- architecture.md: 役割と責務境界
- task-contract.md: task contract v2の形式
- local-workflow.md: baseline、編集、検証、報告
- acceptance.md: 完成判定とE2Eの対応表

## 所有者

Repository harnessは指示、contract検証、baseline、scope・秘密検査、固定checkを所有します。
外部Agentは実際の編集と意味的な受入れ条件の証拠を所有します。commit、push、PRは
どちらの必須責務でもありません。
