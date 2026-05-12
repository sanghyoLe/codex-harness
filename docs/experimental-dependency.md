# Codex Runtime Compatibility

> **Status:** Active · **Owner:** revfactory · **Last updated:** 2026-05-12

This document tracks the runtime assumptions behind `codex-harness`. The upstream `harness` project uses a different runtime vocabulary, so this repository ports the idea to Codex-native project files and Codex subagent workflows.

## Current State

`codex-harness` generates plain repository artifacts:

- `AGENTS.md` as the short project pointer
- `.agents/skills/*/SKILL.md` for the orchestrator and supporting skills
- `.codex/config.toml` for project-level Codex configuration
- `.codex/agents/*.toml` for project-scoped custom agents used by explicit subagent workflows
- `_workspace/` for intermediate artifacts and handoff notes

There is no non-Codex runtime output unless the user explicitly asks for it.

## Runtime Assumptions

| Surface | Assumption | Why it matters |
|---------|------------|----------------|
| Codex plugins | A local or marketplace plugin can expose `plugins/harness/skills/` | Users can install or iterate on the meta-skill |
| Repo-local skills | `.agents/skills/` is available to the project | Generated orchestrators are reusable across sessions |
| Custom agents | `.codex/agents/*.toml` supports `name`, `description`, and `developer_instructions` | Specialist roles can be defined as durable files |
| Project config | `.codex/config.toml` supports web search and agent settings | Generated harnesses can declare default execution policy |

Official Codex references:

- <https://developers.openai.com/codex/subagents>
- <https://developers.openai.com/codex/skills>
- <https://developers.openai.com/codex/guides/agents-md>
- <https://developers.openai.com/codex/plugins/build>
- <https://developers.openai.com/codex/config-reference>

## Codex-Specific Behavior

Codex subagent workflows are explicit: Codex spawns subagents when asked to do so. The port therefore keeps the upstream architecture patterns, but expresses them through Codex-native custom agent files and orchestrator instructions:

- `pipeline`
- `fan-out/fan-in`
- `expert-pool`
- `producer-reviewer`
- `supervisor`
- `hierarchical-delegation`
- `hybrid`

The orchestrator owns workflow, dependency order, workspace contracts, validation, and spawn criteria. Specialist custom agents own depth in their assigned domains and return results through the parent workflow and shared workspace files.

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
