# Changelog

This project follows Semantic Versioning in spirit while the distribution format is still being refined.

## [Unreleased]

### Added

- Added Codex-adapted upstream Harness 1.2.x concepts:
  - Phase 0 existing-harness audit before scaffolding or maintenance
  - `AGENTS.md` pointer policy so agent and skill files remain the source of truth
  - hybrid execution mode and producer-reviewer naming
  - harness evolution / maintenance workflow for follow-up changes and drift repair
- Added scaffold output sections for harness pointers, execution mode, and change history.
- Expanded plugin metadata to version `1.2.1` with team-architecture-factory positioning and broader keywords.

### Changed

- Updated the `harness` skill workflow from a simple 6-phase generator to a Codex-native audit -> design -> scaffold -> validate -> evolve workflow.
- Refreshed bundled reference documents from the newer Claude Harness material, then adapted them to Codex-native outputs (`AGENTS.md`, `.agents/skills/`, `.codex/agents/*.toml`) instead of `.claude/`.
- Updated README and README_KO to describe the newer team-architecture factory positioning, pointer policy, validation, and evolution loop.
- Rewrote `README.md` to reflect the original `harness` product structure and messaging, adapted for Codex-native outputs
- Added `README_KO.md` so the Codex version keeps the original project's bilingual documentation pattern
- Rewrote `plugins/harness/skills/harness/SKILL.md` into a fuller 6-phase meta-skill workflow aligned with the Claude original
- Expanded the scaffolded harness templates so generated outputs include collaboration pattern, validation checklist, richer role guidance, and more procedural orchestrator steps
- Expanded the bundled reference documents so architecture selection, orchestrator design, QA design, skill writing, testing, and team examples are closer to the original `harness` depth
- Added generated sample harnesses under `examples/code-reviewer/` and `examples/fullstack-webapp/` to exercise both review-heavy and delivery-oriented scaffold outputs end to end
- Updated plugin metadata to describe the project as a Codex harness architect rather than a minimal scaffold helper
- Reworked the install and public distribution docs around the official Codex plugin model, including new `PUBLISHING.md` and `PUBLISHING_KO.md` guides

### Fixed

- Kept upstream Claude Agent Teams terminology out of the Codex port where it would imply `.claude/` output or Claude-only tools.
- Normalized orchestrator, supporting skill, and agent names before rendering files so generated `.codex/config.toml` entries stay aligned with actual file paths
- Fixed the reference search script's default root detection so it finds the sibling `codex-harness-100` repository in the current workspace layout
