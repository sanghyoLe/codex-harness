# Orchestrator Template

오케스트레이터 스킬은 하네스의 중심이다. 역할 소개만 적는 문서가 아니라, 어떤 입력을 받고 어떤 순서로 위임하며 무엇을 완료 기준으로 삼는지까지 정의하는 실행 지침이어야 한다.

## 권장 섹션

1. 개요
2. 활성화 기준
3. 역할 구성
4. 워크플로우
5. 병렬 처리 / 순차 처리 기준
6. 데이터 전달 규약
7. 에러 핸들링
8. 검증
9. 산출물 계약

## 강한 오케스트레이터의 특징

- 사용자 요청을 구조화된 입력으로 바꾼다
- 기존 프로젝트 상태를 먼저 조사한다
- 어떤 역할이 언제 필요한지 분명히 쓴다
- 병렬 가능 구간과 의존 구간을 분리한다
- reviewer가 있다면 revision loop를 명시한다
- 완료 조건을 파일과 품질 기준으로 쓴다

## 약한 오케스트레이터의 냄새

- "철저히 분석한다"만 있고 출력 형식이 없다
- 역할 설명은 있는데 순서가 없다
- narrow request에서도 항상 전체 팀을 돌린다
- 기존 파일이 있을 때 어떻게 적응하는지 없다
- 실패 시 폴백이 없다

## 템플릿

```markdown
---
name: {orchestrator-name}
description: "{어떤 요청에서 이 하네스를 사용해야 하는지 자연어로 설명한다. 트리거 구문을 구체적으로 넣는다.}"
---

# {Harness Title}

{이 하네스가 해결하는 문제와 최종 산출물을 2~3문장으로 설명한다.}

## Activation Rules

- 전체 하네스 실행: {예시 프롬프트}
- 좁은 범위 실행: {예시 프롬프트}
- 재구성/개선 모드: {예시 프롬프트}

## Team Composition

| Role | Purpose | Primary Output |
|------|---------|----------------|
| {role-1} | {책임} | `{path}` |
| {role-2} | {책임} | `{path}` |
| {reviewer} | {검수 책임} | `{path}` |

## Workspace Contract

- 입력 정리: `_workspace/00_input.md`
- 실행 계획: `_workspace/01_plan.md`
- 역할별 산출물: `_workspace/{phase}_{role}_{artifact}.md`
- 최종 결과: `_workspace/99_final.md`

## Workflow

### Phase 1: Intake

1. 사용자 요청에서 목표, 범위, 최종 출력 형식을 추출한다.
2. 기존 `AGENTS.md`, `.agents`, `.codex`, 관련 코드와 문서를 읽는다.
3. 필요한 입력이 있으면 `_workspace/00_input.md`에 정리한다.
4. 기존 하네스가 있다면 재생성이 아니라 diff 기반 수정 모드로 전환한다.

### Phase 2: Plan

1. 활성화할 역할만 고른다.
2. 병렬 가능 구간과 순차 의존 구간을 구분한다.
3. `_workspace/01_plan.md`에 다음을 기록한다:
   - 활성 역할
   - 각 역할의 입력/출력
   - 의존 관계
   - 검증 체크포인트

### Phase 3: Delegation

1. 독립 작업은 병렬로 위임한다.
2. 의존 작업은 이전 산출물이 나온 뒤 순차 실행한다.
3. 각 역할에게 다음을 명시한다:
   - 읽어야 할 입력
   - 써야 할 출력 경로
   - 절대 넘지 말아야 할 책임 경계

### Phase 4: Integration

1. 역할별 산출물을 수집한다.
2. 중복, 충돌, 누락을 정리한다.
3. reviewer가 있다면 이 단계 전후로 검수를 수행한다.

### Phase 5: Validation

1. 모든 기대 파일이 존재하는지 확인한다.
2. 역할 간 정합성을 확인한다.
3. unresolved placeholder가 남아 있으면 수정한다.
4. 필요 시 1회 보정 루프를 돌린다.

### Phase 6: Finalization

1. 최종 산출물을 사용자-facing 파일 위치에 반영한다.
2. `_workspace/99_final.md`에 요약과 남은 리스크를 기록한다.
3. 사용자에게 변경 파일과 residual risk를 보고한다.

## Parallelism Rules

- `{role-1}`와 `{role-2}`는 서로 독립이면 병렬 처리한다.
- reviewer는 생성자 산출물이 나온 뒤 실행한다.
- narrow request이면 불필요한 역할은 생략한다.

## Error Handling

- 한 역할 실패: 1회 보정 후 부분 결과로 진행, 누락을 명시
- reviewer와 producer 충돌: reviewer의 근거를 기준으로 producer 수정
- 기존 파일과 충돌: 삭제하지 말고 차이를 비교한 뒤 최소 수정

## Validation Checklist

- `config_file` 경로와 실제 파일이 일치하는가
- `model_instructions_file` 경로와 실제 파일이 일치하는가
- 오케스트레이터 description이 실제 프롬프트를 충분히 받는가
- 역할 수가 문제 크기에 비해 과하지 않은가
- supporting skill이 오케스트레이터와 중복되지 않는가

## Test Scenarios

### Scenario A: Full Request

- 입력: {전체 요청 예시}
- 기대: 전체 역할이 활성화되고 `{final-output}`이 생성된다

### Scenario B: Narrow Request

- 입력: {부분 요청 예시}
- 기대: 일부 역할만 활성화되고 기존 결과를 재활용한다

### Scenario C: Existing Files Present

- 입력: {기존 하네스가 있는 저장소}
- 기대: 전면 재생성이 아니라 수정/보강 모드로 동작한다
```

## 작성 팁

- `Activation Rules`를 넣으면 좁은 요청에서도 과설계가 줄어든다
- `Workspace Contract`를 먼저 고정하면 역할 간 handoff가 쉬워진다
- reviewer가 있다면 "무엇이 revision trigger인가"를 반드시 쓴다
- 최종 답변은 오케스트레이터가 통합하지만, 전문 판단은 역할별 산출물에 위임한다
