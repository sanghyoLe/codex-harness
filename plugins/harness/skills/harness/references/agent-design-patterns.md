# Architecture Patterns

Codex 하네스는 보통 하나의 오케스트레이터 스킬, 여러 repo-local 스킬, 여러 `.codex/agents/*.toml` custom subagent 역할로 구성된다. 중요한 것은 역할 수가 아니라 역할 경계, 데이터 흐름, 검증 루프다.

## 실행 모드

### 1. Codex Custom Subagents

기본 실행 모드다. 오케스트레이터가 작업을 분해하고, 필요한 역할을 `.codex/agents/*.toml` 정의에 맞춰 활성화한다.

```text
[orchestrator skill]
   ├── inspect request + repo
   ├── choose active roles
   ├── delegate with explicit input/output paths
   ├── collect artifacts from _workspace/
   └── integrate, validate, and finalize
```

핵심 원칙:

- 오케스트레이터는 workflow를 소유한다.
- specialist role은 depth를 소유한다.
- `_workspace/`는 중간 산출물과 handoff contract를 소유한다.
- `AGENTS.md`는 포인터와 변경 이력만 소유한다.

### 2. Orchestrator Only

작업이 작고 선형적이면 별도 역할을 만들지 않는다.

사용 신호:

- 산출물이 하나뿐이다.
- 독립 검수가 품질을 실질적으로 올리지 않는다.
- 작업이 짧고 기존 코드 탐색만으로 충분하다.
- 역할별 전문성이 결과 차이에 거의 영향을 주지 않는다.

### 3. Hybrid

Phase마다 실행 방식을 섞는다.

예:

- Phase 1 요구사항 정리: orchestrator only
- Phase 2 병렬 리뷰: custom subagents
- Phase 3 최종 통합: orchestrator
- Phase 4 독립 QA: reviewer subagent

하이브리드에서는 각 Phase 상단에 실행 모드를 명시한다.

## 역할 분리 기준

역할은 다음 네 축 중 둘 이상이 강할 때 분리한다:

| 기준 | 질문 |
|------|------|
| 전문성 | 서로 다른 지식/판단 기준이 필요한가 |
| 병렬성 | 동시에 처리하면 시간이나 품질이 좋아지는가 |
| 컨텍스트 | 한 역할에 모든 정보를 넣으면 과도하게 넓어지는가 |
| 재사용성 | 다음 세션에서도 같은 역할을 다시 쓸 가능성이 높은가 |

역할을 줄여야 하는 신호:

- 같은 파일을 보고 같은 판단을 한다.
- 출력이 서로 구분되지 않는다.
- 오케스트레이터가 역할 결과를 거의 그대로 버린다.
- 사용자가 narrow request를 했는데 항상 전체 팀이 돈다.

## 1. Pipeline

순차 의존 작업에 적합하다.

```text
requirements -> architecture -> implementation -> QA -> release notes
```

적합한 경우:

- 이전 단계 결과가 다음 단계 입력을 결정한다.
- 중간 산출물 handoff가 명확하다.
- 역할별 책임이 단계별로 잘 나뉜다.

권장 출력:

- `_workspace/00_input.md`
- `_workspace/01_requirements.md`
- `_workspace/02_architecture.md`
- `_workspace/03_implementation_plan.md`
- `_workspace/04_qa_report.md`

리스크:

- 앞 단계가 막히면 전체가 지연된다.
- 단계를 너무 잘게 쪼개면 오버헤드가 커진다.

## 2. Fan-Out / Fan-In

병렬 독립 분석 후 종합이 필요한 경우에 적합하다.

```text
               ┌-> architecture review
input -> split ├-> security review
               ├-> performance review
               └-> style review
                         ↓
                    synthesis
```

적합한 경우:

- 동일 입력을 여러 관점에서 동시에 볼 수 있다.
- 각 역할의 산출물이 독립적으로 생산 가능하다.
- 마지막에 종합자 또는 reviewer가 필요하다.

권장 출력:

- `_workspace/01_architecture_review.md`
- `_workspace/02_security_review.md`
- `_workspace/03_performance_review.md`
- `_workspace/04_style_review.md`
- `_workspace/05_summary.md`

리스크:

- 역할 범위가 흐리면 중복 작업이 발생한다.
- 종합 단계가 약하면 병렬 분석의 가치가 사라진다.

## 3. Expert Pool

상황별로 필요한 전문가만 선택 호출하는 구조다.

```text
router -> {privacy | compliance | infra | security | docs}
```

적합한 경우:

- 매 요청마다 필요한 전문가가 다르다.
- 고정 역할을 항상 돌리는 것이 낭비다.
- 오케스트레이터의 라우팅 판단이 품질을 좌우한다.

리스크:

- 라우팅 규칙이 약하면 누락이 생긴다.
- role description이 모호하면 잘못된 전문가가 선택된다.

## 4. Producer-Reviewer

생성자와 검수자를 분리하는 구조다.

```text
producer -> reviewer -> revise -> finalize
```

적합한 경우:

- 주된 실패 모드가 품질 드리프트다.
- 산출물을 객관 기준으로 재검토할 수 있다.
- 팀을 크게 만들 필요는 없지만 독립 검수는 중요하다.

권장 규칙:

- reviewer는 required fix와 optional fix를 구분한다.
- 재작업은 보통 1~2회로 제한한다.
- reviewer 기준은 "좋아 보임"이 아니라 구체적 acceptance criteria여야 한다.

## 5. Supervisor

오케스트레이터가 중간 결과를 보고 다음 위임 대상을 동적으로 결정한다.

```text
supervisor
   ├-> search
   ├-> analyze
   ├-> deeper branch if needed
   └-> finalize
```

적합한 경우:

- 작업 방향이 중간 발견에 따라 달라진다.
- 분기 규칙이 존재한다.
- 초기 계획보다 현장 판단이 중요하다.

리스크:

- 역할 계약이 약하면 오케스트레이터가 모든 걸 직접 하게 된다.
- branching 기준이 문서화되지 않으면 재현성이 낮다.

## 6. Hierarchical Delegation

큰 프로그램을 상위/하위 레이어로 나눠 처리한다.

```text
lead
  ├-> frontend lead -> ui, state, qa
  └-> backend lead -> api, db, qa
```

적합한 경우:

- 범위가 크고 workstream이 분리 가능하다.
- 평평한 팀 하나로는 관리가 어렵다.
- 각 하위 영역이 자체 미니 workflow를 가진다.

리스크:

- 깊이 3단계 이상은 지연과 컨텍스트 손실이 커진다.
- Codex custom subagents는 repo-local 파일 기반으로 재사용하되, 실제 실행은 오케스트레이터가 조율하도록 설계한다.

## 복합 패턴

| 복합 패턴 | 구성 | 예시 |
|----------|------|------|
| Pipeline + Fan-Out | 순차 단계 중 일부 병렬화 | 분석 -> 프론트/백엔드 병렬 구현 -> 통합 QA |
| Fan-Out + Producer-Reviewer | 병렬 생성 후 각각 검증 | 다국어 번역 -> 네이티브 리뷰 |
| Supervisor + Expert Pool | 감독자가 전문가 선택 | 고객 문의 분류 후 법무/보안/기술 전문가 호출 |
| Hierarchical + QA Gate | workstream별 산출 후 중앙 검증 | 대규모 마이그레이션 |

## 에이전트 정의 구조

Codex custom subagent는 `.codex/agents/{name}.toml`로 정의한다.

```toml
name = "security-reviewer"
description = "인증, 인가, 데이터 노출, 입력 검증 리스크를 검토한다."

developer_instructions = """
# Security Reviewer

## Core Responsibilities
- 인증/인가 경계와 데이터 노출 가능성을 검토한다.
- 위험도를 critical/high/medium/low로 분류한다.

## Inputs
- `_workspace/00_input.md`
- 관련 코드 경로

## Outputs
- `_workspace/02_security_review.md`

## Working Principles
- 추측보다 근거를 우선한다.
- exploit 가능성과 실제 영향도를 분리한다.
- 수정 제안은 파일/라인 단위로 구체화한다.

## Error Handling
- 재현이 불가능하면 가정과 필요한 추가 확인을 명시한다.
"""
```

## 축소 규칙

하네스가 좋아지려면 역할 수 증가가 아니라 역할 간 경계 명확화가 먼저다. 다음 경우에는 더 작게 만든다:

- 산출물이 1개뿐이다.
- 두 역할이 같은 입력으로 같은 판단을 한다.
- reviewer 기준을 명시할 수 없다.
- 오케스트레이터가 직접 검증해도 충분하다.
