# Quickstart — First Codex Harness

This guide shows the shortest local path for trying `codex-harness`.

## What You Get

A generated project harness with:

- `AGENTS.md`
- `.agents/skills/<orchestrator>/SKILL.md`
- `.codex/config.toml`
- `.codex/agents/*.toml`
- `_workspace/` contracts for intermediate outputs

## Prerequisites

- Codex installed and able to open the target repository
- This repository checked out locally
- The target repository opened in a trusted state so Codex can load repo-local `.codex/` config

## Option 1: Use This Repo As A Reference

The simplest workflow is to ask Codex to inspect `codex-harness` and generate a harness for another project.

```text
Use ~/Desktop/harness/codex-harness as the reference and build a Codex-native harness for this project.
```

Useful prompt variants:

```text
하네스 구성해줘. codex-harness 구조를 참고해서 이 저장소에 맞게 만들어줘.
Build a code review harness for this repository.
Design a fullstack webapp harness with architecture, frontend, backend, QA, and release roles.
```

## Option 2: Install As A Local Plugin

During local iteration, install the plugin through a repo or personal marketplace as described in [`PUBLISHING.md`](../PUBLISHING.md).

At a high level:

1. Put the plugin at `plugins/harness` in the marketplace source.
2. Ensure the marketplace entry points to `./plugins/harness`.
3. Restart Codex.
4. Install `harness` from the Codex plugin UI or plugin command surface.

This repository already includes the local plugin metadata:

- `.agents/plugins/marketplace.json`
- `plugins/harness/.codex-plugin/plugin.json`

## Generate From A Spec

For deterministic local testing, use the scaffold script directly:

```bash
python3 plugins/harness/skills/harness/scripts/scaffold_harness.py \
  --spec examples/code-reviewer/spec.json \
  --target /tmp/codex-harness-demo
```

Expected output:

```text
/tmp/codex-harness-demo/
├── AGENTS.md
├── .agents/skills/code-reviewer/SKILL.md
└── .codex/
    ├── config.toml
    └── agents/*.toml
```

## Verify

```bash
rg -n "\\[TODO\\]|\\{[^}]+\\}" /tmp/codex-harness-demo/AGENTS.md /tmp/codex-harness-demo/.agents /tmp/codex-harness-demo/.codex
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "code review" --limit 3
```

The placeholder search should return no unresolved template markers. The reference search may return no matches if `codex-harness-100` is not available next to this checkout; that is acceptable for local smoke testing.

## Next Reads

- [`docs/experimental-dependency.md`](./experimental-dependency.md)
- [`PUBLISHING.md`](../PUBLISHING.md)
- [`README.md`](../README.md)
