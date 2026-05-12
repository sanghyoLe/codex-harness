# Orchestrator Template

오케스트레이터 스킬은 하네스의 중심이다. 역할 소개가 아니라 어떤 입력을 받고, 어떤 역할을 언제 활성화하며, 무엇을 완료 기준으로 삼는지 정의하는 실행 지침이어야 한다.

## 실행 모드

### A. Codex Custom Agents + Explicit Subagent Workflow

2개 이상의 전문 역할이 실질적으로 결과 품질을 높일 때 기본으로 사용한다. 각 역할은 `.codex/agents/{role}.toml`에 custom agent로 정의하고, 오케스트레이터는 필요한 역할을 명시적으로 spawn하도록 지시한다. Codex는 description만 보고 자동으로 하위 에이전트를 띄우지 않는다.

### B. Orchestrator Only

작업이 작고 선형적이며 독립 검수 가치가 낮을 때 사용한다. 이 경우에도 `_workspace/`와 검증 기준은 남긴다.

### C. Hybrid

Phase별로 역할 활성화 방식을 다르게 한다. 예: 요구사항 정리는 오케스트레이터 단독, 리뷰는 여러 custom agent를 명시적으로 spawn, 최종 통합은 오케스트레이터.

## 권장 섹션

1. 개요
2. 활성화 기준
3. 실행 모드
4. 역할 구성
5. 워크스페이스 계약
6. 워크플로우
7. 병렬/순차 기준
8. 데이터 전달 규약
9. 에러 핸들링
10. 검증
11. 테스트 시나리오

## 템플릿

```markdown
---
name: {orchestrator-name}
description: "{도메인} 하네스를 실행한다. {초기 실행 키워드}. 후속 작업: 결과 수정, 부분 재실행, 업데이트, 보완, 다시 실행, 이전 결과 개선 요청 시에도 이 스킬을 사용한다."
---

# {Harness Title}

{이 하네스가 해결하는 문제와 최종 산출물을 2~3문장으로 설명한다.}

## Activation Rules

- 전체 실행: {예시 프롬프트}
- 좁은 범위 실행: {예시 프롬프트}
- 재구성/개선: {예시 프롬프트}
- 운영/점검: {예시 프롬프트}

## Execution Mode

- 기본 모드: Codex custom agents + explicit subagent workflow
- 축소 모드: orchestrator only
- 하이브리드 조건: {조건}

## Role Composition

| Role | Config | Purpose | Primary Output |
|------|--------|---------|----------------|
| {role-1} | `.codex/agents/{role-1}.toml` | {책임} | `{path}` |
| {role-2} | `.codex/agents/{role-2}.toml` | {책임} | `{path}` |
| {reviewer} | `.codex/agents/{reviewer}.toml` | {검수 책임} | `{path}` |

## Workspace Contract

- 입력 정리: `_workspace/00_input.md`
- 실행 계획: `_workspace/01_plan.md`
- 역할별 산출물: `_workspace/{phase}_{role}_{artifact}.md`
- 최종 결과: `_workspace/99_final.md`
- 변경 이력: `_workspace/harness_changes.md`

## Workflow

### Phase 0: Context Check

1. 기존 `_workspace/`, `AGENTS.md`, `.agents/skills/`, `.codex/agents/` 상태를 확인한다.
2. `_workspace/`가 있고 사용자가 부분 수정 요청을 했다면 해당 역할만 재실행한다.
3. 새 입력으로 전체 재실행해야 하면 기존 `_workspace/`를 보관 디렉터리로 이동한 뒤 새로 만든다.

### Phase 1: Intake

1. 목표, 범위, 최종 출력 형식을 추출한다.
2. 기존 코드, 문서, 하네스 파일을 읽는다.
3. 필요한 입력을 `_workspace/00_input.md`에 정리한다.

### Phase 2: Plan

1. 활성화할 역할만 고른다.
2. 병렬 가능 구간과 순차 의존 구간을 구분한다.
3. `_workspace/01_plan.md`에 활성 역할, 입력/출력, 의존 관계, 검증 체크포인트를 기록한다.

### Phase 3: Explicit Subagent Delegation

1. 독립 작업은 필요한 custom agent만 명시적으로 spawn하여 병렬로 맡긴다.
2. 의존 작업은 이전 산출물이 나온 뒤 순차 실행한다.
3. 각 역할에게 읽을 입력, 쓸 출력 경로, 책임 경계를 명시한다.
4. Codex subagent는 부모 스레드와 공유 워크스페이스 파일을 통해 결과를 반환한다고 가정하고, 에이전트 간 직접 메시징을 전제로 하지 않는다.

### Phase 4: Integration

1. 역할별 산출물을 수집한다.
2. 중복, 충돌, 누락을 정리한다.
3. reviewer가 있으면 required fix와 optional fix를 구분해 반영한다.

### Phase 5: Validation

1. 모든 기대 파일이 존재하는지 확인한다.
2. 역할 간 정합성을 확인한다.
3. unresolved placeholder가 남아 있으면 수정한다.
4. 필요 시 1회 보정 루프를 돌린다.

### Phase 6: Finalization

1. 최종 산출물을 사용자-facing 위치에 반영한다.
2. `_workspace/99_final.md`에 요약과 남은 리스크를 기록한다.
3. `AGENTS.md` 포인터와 변경 이력을 갱신한다.
4. 사용자에게 변경 파일과 residual risk를 보고한다.

## Parallelism Rules

- `{role-1}`와 `{role-2}`는 서로 독립이면 병렬 subagent로 처리한다.
- reviewer는 생성자 산출물이 나온 뒤 실행한다.
- narrow request이면 불필요한 역할은 생략한다.

## Error Handling

- 한 역할 실패: 1회 보정 후 부분 결과로 진행하고 누락을 명시한다.
- reviewer와 producer 충돌: reviewer의 근거를 기준으로 producer를 수정한다.
- 기존 파일과 충돌: 삭제하지 말고 차이를 비교한 뒤 최소 수정한다.
- 과반 역할 실패: 사용자에게 현재까지의 부분 결과와 선택지를 제시한다.

## Validation Checklist

- 각 `.codex/agents/*.toml`에 `name`, `description`, `developer_instructions`가 있는가
- 오케스트레이터 description이 실제 프롬프트를 충분히 받는가
- 역할 수가 문제 크기에 비해 과하지 않은가
- supporting skill이 오케스트레이터와 중복되지 않는가
- `AGENTS.md`가 포인터 역할만 하고 세부 내용을 중복하지 않는가

## Test Scenarios

### Full Request

- 입력: {전체 요청 예시}
- 기대: 전체 역할이 활성화되고 `{final-output}`이 생성된다.

### Narrow Request

- 입력: {부분 요청 예시}
- 기대: 일부 역할만 활성화되고 기존 결과를 재활용한다.

### Existing Files Present

- 입력: {기존 하네스가 있는 저장소}
- 기대: 전면 재생성이 아니라 수정/보강 모드로 동작한다.
```

## 작성 팁

- `Activation Rules`를 넣으면 좁은 요청에서도 과설계가 줄어든다.
- `Workspace Contract`를 먼저 고정하면 역할 간 handoff가 쉬워진다.
- reviewer가 있다면 "무엇이 revision trigger인가"를 반드시 쓴다.
- 최종 답변은 오케스트레이터가 통합하지만, 전문 판단은 역할별 산출물에 위임한다.
