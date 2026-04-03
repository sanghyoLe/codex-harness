# Fullstack Web App Harness

Pipeline-oriented fullstack delivery harness for requirements, architecture, frontend, backend, QA, and deployment preparation.

## Codex Structure

- `AGENTS.md` explains this harness.
- `.agents/skills/` stores the orchestrator and supporting skills.
- `.codex/config.toml` stores global Codex and subagent settings for the project.
- `.codex/agents/*.toml` defines standalone custom subagents with their own instructions.

Open the project in a trusted state so Codex loads the local `.codex/` config.

## Reference Lineage

- `/Users/isanghyo/Desktop/harness/codex-harness-100/ko/16-fullstack-webapp`: Closest existing Codex harness for multi-role website delivery with architecture-first sequencing.

## Collaboration Pattern

- `pipeline`

## Skills

- `fullstack-webapp`: Use when the user asks for a fullstack web app harness, a role-based website delivery workflow, or a project structure for frontend, backend, QA, and deployment work.
- `component-patterns`: Frontend component and state-management patterns for the frontend developer.
- `api-security-checklist`: Backend API hardening checklist for auth, validation, and unsafe defaults.

## Subagent Roles

- `architect`: Define system shape, data boundaries, API contracts, and execution order so implementation roles can proceed with minimal ambiguity.
- `frontend-dev`: Implement pages, UI components, client-side state, and API integration according to the agreed architecture.
- `backend-dev`: Implement API routes, data access, authentication, authorization, and business rules according to the agreed contracts.
- `qa-engineer`: Validate interface coherence, test strategy, regression risk, and readiness for release.
- `devops-engineer`: Prepare deployment, CI or release automation, environment assumptions, and operational handoff guidance.

## Usage

Ask Codex to use the `fullstack-webapp` skill, or use a natural-language request that matches it.
- Recommended start: `fullstack-webapp`
- `web_search` default: `disabled`
- Workspace root: `_workspace`

## Outputs

- `_workspace/00_input.md`
- `_workspace/01_architecture.md`
- `_workspace/02_api_spec.md`
- `_workspace/03_db_schema.md`
- `_workspace/04_test_plan.md`
- `_workspace/05_deploy_guide.md`
- `_workspace/06_review_report.md`

## Mode Matrix

- `full pipeline` -> `architect`, `frontend-dev`, `backend-dev`, `qa-engineer`, `devops-engineer`: Default mode for greenfield or major feature delivery.
- `backend-only feature` -> `architect`, `backend-dev`, `qa-engineer`: Skip frontend and deployment when the user only needs API or data-layer work.
- `frontend-only feature` -> `architect`, `frontend-dev`, `qa-engineer`: Assume an existing API contract or mock service.
- `deployment-only work` -> `devops-engineer`: Use a narrow infra mode when the product code already exists.

## Validation Checklist

- Confirm every custom agent TOML defines `name`.
- Confirm every custom agent TOML defines `description`.
- Confirm every custom agent TOML defines `developer_instructions`.
- Remove any unresolved placeholders before considering the harness complete.
