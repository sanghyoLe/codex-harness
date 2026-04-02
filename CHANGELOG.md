# Changelog

This project follows Semantic Versioning in spirit while the distribution format is still being refined.

## [Unreleased]

### Changed

- Rewrote `README.md` to reflect the original `harness` product structure and messaging, adapted for Codex-native outputs
- Added `README_KO.md` so the Codex version keeps the original project's bilingual documentation pattern
- Rewrote `plugins/harness/skills/harness/SKILL.md` into a fuller 6-phase meta-skill workflow aligned with the Claude original
- Expanded the scaffolded harness templates so generated outputs include collaboration pattern, validation checklist, richer role guidance, and more procedural orchestrator steps
- Expanded the bundled reference documents so architecture selection, orchestrator design, QA design, skill writing, testing, and team examples are closer to the original `harness` depth
- Added generated sample harnesses under `examples/code-reviewer/` and `examples/fullstack-webapp/` to exercise both review-heavy and delivery-oriented scaffold outputs end to end
- Updated plugin metadata to describe the project as a Codex harness architect rather than a minimal scaffold helper
- Reworked the install and public distribution docs around the official Codex plugin model, including new `PUBLISHING.md` and `PUBLISHING_KO.md` guides

### Fixed

- Normalized orchestrator, supporting skill, and agent names before rendering files so generated `.codex/config.toml` entries stay aligned with actual file paths
- Fixed the reference search script's default root detection so it finds the sibling `codex-harness-100` repository in the current workspace layout
