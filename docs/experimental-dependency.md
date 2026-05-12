# Codex Runtime Compatibility

> **Status:** Active · **Owner:** revfactory · **Last updated:** 2026-05-11

This document tracks the runtime assumptions behind `codex-harness`. The upstream `harness` project targets Claude Code Agent Teams; this repository ports the idea to Codex-native project files.

## Current State

`codex-harness` generates plain repository artifacts:

- `AGENTS.md` as the short project pointer
- `.agents/skills/*/SKILL.md` for the orchestrator and supporting skills
- `.codex/config.toml` for project-level Codex configuration
- `.codex/agents/*.toml` for standalone custom subagents
- `_workspace/` for intermediate artifacts and handoff notes

There is no Claude-only `.claude/` output in the Codex port unless the user explicitly asks for it.

## Runtime Assumptions

| Surface | Assumption | Why it matters |
|---------|------------|----------------|
| Codex plugins | A local or marketplace plugin can expose `plugins/harness/skills/` | Users can install or iterate on the meta-skill |
| Repo-local skills | `.agents/skills/` is available to the project | Generated orchestrators are reusable across sessions |
| Custom subagents | `.codex/agents/*.toml` supports `name`, `description`, and `developer_instructions` | Specialist roles can be defined as durable files |
| Project config | `.codex/config.toml` supports web search and agent settings | Generated harnesses can declare default execution policy |

## Difference From Upstream Harness

The upstream Claude project emphasizes Agent Teams primitives such as team creation, task lists, and direct agent-to-agent messaging. The Codex port keeps the same architecture patterns, but expresses them through Codex-native files and orchestrator instructions:

- `pipeline`
- `fan-out/fan-in`
- `expert-pool`
- `producer-reviewer`
- `supervisor`
- `hierarchical-delegation`
- `hybrid`

The orchestrator owns workflow, dependency order, workspace contracts, and validation. Specialist subagents own depth in their assigned domains.

## Compatibility Response

If Codex changes one of the generated-file contracts, maintainers should:

1. Open a compatibility issue with the affected Codex version and generated surface.
2. Patch `plugins/harness/skills/harness/scripts/scaffold_harness.py`.
3. Update the relevant reference docs and examples.
4. Add a `CHANGELOG.md` entry under `Unreleased`.
5. Validate with at least one sample scaffold, such as `examples/code-reviewer/spec.json`.

## Related Documents

- [`docs/quickstart.md`](./quickstart.md)
- [`CONTRIBUTING.md`](../CONTRIBUTING.md)
- [`PUBLISHING.md`](../PUBLISHING.md)
