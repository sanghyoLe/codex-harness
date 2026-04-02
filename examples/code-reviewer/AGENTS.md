# Code Reviewer Harness

Parallel code review harness for architecture, security, performance, and style, with a synthesis reviewer that merges findings into a single decision.

## Codex Structure

- `AGENTS.md` explains this harness.
- `.agents/skills/` stores the orchestrator and supporting skills.
- `.codex/config.toml` registers reusable subagent roles.
- `.codex/agents/*.toml` points each role to its instruction file.
- `.codex/agents/*.md` contains the actual role instructions.

Open the project in a trusted state so Codex loads the local `.codex/` config.

## Reference Lineage

- `/Users/isanghyo/Desktop/harness/codex-harness-100/ko/21-code-reviewer`: Closest existing Codex review harness with parallel specialist roles and a synthesis step.

## Collaboration Pattern

- `fan-out/fan-in`

## Skills

- `code-reviewer`: Use when the user asks for a broad code review harness, PR review structure, or a role-based review team for architecture, security, performance, and code style.
- `vulnerability-patterns`: Language-aware vulnerability checklist for the security analyst.
- `refactoring-catalog`: Refactoring patterns and code-smell remediation guidance for architecture and performance review.

## Subagent Roles

- `style-inspector`: Inspect naming, formatting, readability, comment quality, and local coding conventions.
- `security-analyst`: Inspect trust boundaries, exploitable issues, unsafe defaults, and sensitive-data handling.
- `performance-analyst`: Inspect latency, throughput, algorithmic waste, unnecessary allocations, and query inefficiencies.
- `architecture-reviewer`: Inspect module boundaries, dependency direction, cohesion, coupling, and long-term maintainability.
- `review-synthesizer`: Merge findings from all review roles, remove duplicates, and assign final severity and action priority.

## Usage

Ask Codex to use the `code-reviewer` skill, or use a natural-language request that matches it.
- Recommended start: `code-reviewer`
- `web_search` default: `off`
- Workspace root: `_workspace`

## Outputs

- `_workspace/00_input.md`
- `_workspace/01_style_review.md`
- `_workspace/02_security_review.md`
- `_workspace/03_performance_review.md`
- `_workspace/04_architecture_review.md`
- `_workspace/05_review_summary.md`

## Mode Matrix

- `full review` -> `style-inspector`, `security-analyst`, `performance-analyst`, `architecture-reviewer`, `review-synthesizer`: Default mode for broad repository or PR review.
- `security-only review` -> `security-analyst`, `review-synthesizer`: Skip unrelated roles when the user only wants security feedback.
- `performance-only review` -> `performance-analyst`, `review-synthesizer`: Focus on bottlenecks, waste, and scaling risks.

## Validation Checklist

- Confirm every role in `.codex/config.toml` points to a real `.toml` file.
- Confirm every role `.toml` points to a real `.md` instructions file.
- Remove any unresolved placeholders before considering the harness complete.
