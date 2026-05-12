---
name: code-reviewer
description: "Use when the user asks for a broad code review harness, PR review structure, or a role-based Codex review workflow for architecture, security, performance, and code style."
---

# Code Reviewer Harness

Parallel code review harness for architecture, security, performance, and style, with a synthesis reviewer that merges findings into a single decision.

## Execution Mode

- `codex-custom-agents-explicit-subagents`

## Activation Examples

- `코드 리뷰 하네스 만들어줘`
- `이 저장소에 맞는 PR 리뷰 워크플로우 설계해줘`
- `보안/성능/아키텍처를 나눠서 리뷰하는 구조 만들어줘`

## Mode Switching

- `full review` -> `style-inspector`, `security-analyst`, `performance-analyst`, `architecture-reviewer`, `review-synthesizer`: Default mode for broad repository or PR review.
- `security-only review` -> `security-analyst`, `review-synthesizer`: Skip unrelated roles when the user only wants security feedback.
- `performance-only review` -> `performance-analyst`, `review-synthesizer`: Focus on bottlenecks, waste, and scaling risks.

## Workflow

### Phase 1: Intake

1. Extract the review target, language or framework, scope, and any PR-specific context from the user request.
2. Inspect the repository or diff and write the normalized review brief to `_workspace/00_input.md`.
3. Decide whether the request needs the full review workflow or a narrow review mode.

### Phase 2: Parallel Review

1. Explicitly spawn `style-inspector`, `security-analyst`, `performance-analyst`, and `architecture-reviewer` as parallel Codex subagents when the request is broad.
2. Tell each spawned custom agent which input to read, which workspace file to write, and that blockers or cross-role contradictions must be returned through the parent workflow or shared workspace.
3. If the request is narrow, spawn only the relevant custom agent plus `review-synthesizer`.

### Phase 3: Synthesis

1. Read all specialist outputs and merge duplicates, overlaps, and contradictory recommendations.
2. Assign severity and action priority in `_workspace/05_review_summary.md`.
3. Return a final decision with required fixes, optional improvements, and residual uncertainty.

## Workspace Contract

- Primary workspace root: `_workspace`
- Expected artifact: `_workspace/00_input.md`
- Expected artifact: `_workspace/01_style_review.md`
- Expected artifact: `_workspace/02_security_review.md`
- Expected artifact: `_workspace/03_performance_review.md`
- Expected artifact: `_workspace/04_architecture_review.md`
- Expected artifact: `_workspace/05_review_summary.md`

## Validation

- Check that all generated paths resolve.
- Check that the trigger description matches likely user requests.
- Check that the chosen roles materially improve decomposition or quality.
- Remove unresolved placeholders before finalizing the harness.
