---
name: fullstack-webapp
description: "Use when the user asks for a fullstack web app harness, a role-based website delivery workflow, or a project structure for frontend, backend, QA, and deployment work."
---

# Fullstack Web App Harness

Pipeline-oriented fullstack delivery harness for requirements, architecture, frontend, backend, QA, and deployment preparation.

## Activation Examples

- `풀스택 웹앱 하네스 구성해줘`
- `이 저장소에 맞는 웹서비스 개발 팀 설계해줘`
- `프론트엔드, 백엔드, QA, 배포까지 나눠서 일하는 구조 만들어줘`

## Mode Switching

- `full pipeline` -> `architect`, `frontend-dev`, `backend-dev`, `qa-engineer`, `devops-engineer`: Default mode for greenfield or major feature delivery.
- `backend-only feature` -> `architect`, `backend-dev`, `qa-engineer`: Skip frontend and deployment when the user only needs API or data-layer work.
- `frontend-only feature` -> `architect`, `frontend-dev`, `qa-engineer`: Assume an existing API contract or mock service.
- `deployment-only work` -> `devops-engineer`: Use a narrow infra mode when the product code already exists.

## Workflow

### Phase 1: Intake and Architecture

1. Extract product goal, key flows, target users, stack constraints, and whether the repository is greenfield or incremental.
2. Inspect the current repository and write the normalized brief to `_workspace/00_input.md`.
3. Have the architect define system shape, API boundaries, database model, and delivery assumptions in `_workspace/01_architecture.md`, `_workspace/02_api_spec.md`, and `_workspace/03_db_schema.md`.

### Phase 2: Parallel Delivery

1. Once architecture is stable, run frontend, backend, and deployment preparation in parallel where possible.
2. Have each implementation role write concrete artifacts and flag contract mismatches quickly.
3. Keep QA informed of architecture and interface decisions so review criteria are ready before integration.

### Phase 3: QA and Finalization

1. Have QA validate functionality, interface coherence, and regression risk, then write `_workspace/04_test_plan.md` and `_workspace/06_review_report.md`.
2. Have DevOps finalize deployment notes in `_workspace/05_deploy_guide.md`.
3. Return final deliverables with clear residual risks, follow-up work, and readiness status.

## Workspace Contract

- Primary workspace root: `_workspace`
- Expected artifact: `_workspace/00_input.md`
- Expected artifact: `_workspace/01_architecture.md`
- Expected artifact: `_workspace/02_api_spec.md`
- Expected artifact: `_workspace/03_db_schema.md`
- Expected artifact: `_workspace/04_test_plan.md`
- Expected artifact: `_workspace/05_deploy_guide.md`
- Expected artifact: `_workspace/06_review_report.md`

## Validation

- Check that all generated paths resolve.
- Check that the trigger description matches likely user requests.
- Check that the chosen roles materially improve decomposition or quality.
- Remove unresolved placeholders before finalizing the harness.
