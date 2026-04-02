# Architecture Patterns

Codex 하네스는 보통 하나의 오케스트레이터 스킬과 여러 서브에이전트 역할로 구성된다. 중요한 것은 "몇 명을 두는가"가 아니라 "역할 경계와 데이터 흐름이 명확한가"다.

## 1. 실행 모델

### 기본 모델: 오케스트레이터 + 서브에이전트

Codex 하네스의 기본 형태는 다음과 같다:

```text
[orchestrator skill]
   ├── inspect request + repo
   ├── choose which roles to activate
   ├── delegate work
   ├── collect artifacts from _workspace/
   └── integrate, validate, and finalize
```

핵심 원칙:

- 오케스트레이터가 workflow를 소유한다
- specialist role은 depth를 소유한다
- `_workspace/`는 중간 산출물과 handoff contract를 소유한다

### 팀을 과도하게 만들지 말아야 하는 경우

다음 조건이면 다역할 하네스를 억지로 만들지 않는다:

- 산출물이 사실상 하나뿐이다
- 작업이 짧고 선형적이다
- 독립 검수가 품질을 실질적으로 올리지 않는다
- 역할별 전문성이 결과 차이에 거의 영향을 주지 않는다

### 최소 2개 역할이 유리한 경우

- 여러 관점의 검토가 필요하다
- 여러 산출물이 서로 정합해야 한다
- 생성 후 검수 루프가 중요하다
- 병렬 분석이 시간과 품질 모두에 이득이다

## 2. Pattern: Pipeline

순차 의존 작업에 적합하다.

```text
requirements -> architecture -> implementation -> QA -> release notes
```

적합한 경우:

- 이전 단계 결과가 다음 단계 입력을 실질적으로 결정한다
- 중간 산출물의 handoff가 명확하다
- 역할별 책임이 단계별로 잘 나뉜다

장점:

- 책임과 handoff 순서가 분명하다
- 진행 상황 추적이 쉽다
- 기존 레거시 저장소에 붙이기 쉽다

리스크:

- 앞 단계가 막히면 전체가 지연된다
- 단계를 너무 잘게 쪼개면 오버헤드가 커진다

권장 출력 예시:

- `_workspace/00_input.md`
- `_workspace/01_requirements.md`
- `_workspace/02_architecture.md`
- `_workspace/03_implementation_plan.md`
- `_workspace/04_qa_report.md`

## 3. Pattern: Fan-Out / Fan-In

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

- 동일 입력을 여러 관점에서 동시에 볼 수 있다
- 각 역할의 산출물이 독립적으로 생산 가능하다
- 마지막에 종합자 또는 reviewer가 필요하다

장점:

- 넓은 범위를 빠르게 커버한다
- 전문성 분리가 쉽다
- 코드 리뷰, 리서치, 감사성 작업에 강하다

리스크:

- 역할 범위가 흐리면 중복 작업이 발생한다
- 종합 단계가 약하면 병렬 분석의 가치가 사라진다

권장 출력 예시:

- `_workspace/01_architecture_review.md`
- `_workspace/02_security_review.md`
- `_workspace/03_performance_review.md`
- `_workspace/04_style_review.md`
- `_workspace/05_summary.md`

## 4. Pattern: Expert Pool

상황별로 필요한 전문가만 선택 호출하는 구조다.

```text
router -> {privacy | compliance | infra | security | docs}
```

적합한 경우:

- 매 요청마다 필요한 전문가가 다르다
- 고정 풀팀을 항상 돌리는 것이 낭비다
- 오케스트레이터의 라우팅 판단이 품질을 좌우한다

장점:

- 효율적이다
- 작은 요청에도 과하게 무거워지지 않는다
- 장기적으로 역할 확장이 쉽다

리스크:

- 라우팅 규칙이 약하면 누락이 생긴다
- 역할 설명이 모호하면 잘못된 전문가가 선택된다

좋은 예:

- 법률/개인정보/보안 중 필요한 것만 켜는 감사 하네스
- 특정 채널만 활성화하는 콘텐츠 하네스

## 5. Pattern: Generate-Critique

생성자와 검수자를 분리하는 구조다.

```text
producer -> reviewer -> revise -> finalize
```

적합한 경우:

- 주된 실패 모드가 품질 드리프트다
- 산출물을 객관 기준으로 재검토할 수 있다
- 팀을 크게 만들 필요는 없지만 독립 검수는 중요하다

장점:

- 복잡도를 많이 늘리지 않고 품질을 올린다
- 글쓰기, 코드 생성, 전략 문서, 크리에이티브 작업에 잘 맞는다

리스크:

- reviewer가 generic하면 의미가 약하다
- revision loop 제한이 없으면 끝없이 흔들린다

권장 규칙:

- reviewer는 required fix와 optional fix를 구분한다
- 재작업은 보통 1~2회로 제한한다

## 6. Pattern: Supervisor

오케스트레이터가 중간 결과를 보고 다음 위임 대상을 동적으로 결정한다.

```text
supervisor
   ├-> search
   ├-> analyze
   ├-> deeper branch if needed
   └-> finalize
```

적합한 경우:

- 작업 방향이 중간 발견에 따라 달라진다
- 분기 규칙이 존재한다
- 초기 계획보다 현장 판단이 중요하다

장점:

- 유연하다
- 탐색형 리서치나 트리아지에 강하다

리스크:

- 역할 계약이 약하면 오케스트레이터가 모든 걸 직접 하게 된다
- branching 기준이 문서화되지 않으면 재현성이 낮다

## 7. Pattern: Hierarchical Delegation

큰 프로그램을 상위/하위 레이어로 나눠 처리한다.

```text
lead
  ├-> frontend lead -> ui, state, qa
  └-> backend lead -> api, db, qa
```

적합한 경우:

- 범위가 크고 workstream이 분리 가능하다
- 평평한 팀 하나로는 관리가 어렵다
- 각 하위 영역이 자체 미니 workflow를 가진다

장점:

- 큰 문제를 구조적으로 분해할 수 있다
- workstream 간 소유권이 분명하다

리스크:

- 일반 규모의 작업에는 과설계다
- 문서화가 약하면 handoff 손실이 크다

권장:

- 실제로 scope가 큰 경우에만 사용한다
- depth는 2단계 정도로 유지한다

## 8. 역할 분리 기준

역할을 분리할지 판단할 때는 네 가지 축을 본다.

### 전문성

- 다른 판단 기준이 필요한가
- 다른 체크리스트가 필요한가
- 다른 산출물 형식이 필요한가

### 병렬성

- 동시에 돌려도 되는가
- 서로 기다리지 않고 진행 가능한가

### 컨텍스트 밀도

- 한 역할이 너무 많은 문맥을 떠안고 있는가
- 분리하면 각 역할이 더 좁고 명확해지는가

### 재사용성

- 이후 다른 하네스에서도 같은 역할을 재사용할 가능성이 있는가

역할을 분리하지 말아야 하는 신호:

- 차이가 이름뿐이다
- 산출물이 거의 동일하다
- 오케스트레이터가 다시 다 병합해야 해서 이득이 없다

## 9. 기본 추천

- 기능 구현: `pipeline` 또는 `generate-critique`
- 넓은 범위 코드 리뷰: `fan-out/fan-in`
- 리서치/탐색 작업: `supervisor`
- 요청마다 다른 전문가가 필요한 경우: `expert-pool`
- 큰 프로그램 단위 설계/마이그레이션: `hierarchical-delegation`

## 10. 출력 계약 추천

하네스가 복잡할수록 `_workspace/` 계약을 명시한다.

추천 규칙:

- 입력: `_workspace/00_input.md`
- 계획: `_workspace/01_plan.md`
- 역할별 산출물: `_workspace/{phase}_{role}_{artifact}.md`
- 최종본: `_workspace/99_final.md`

중간 산출물은 지우지 않는다. 하네스는 재현성과 감사 추적까지 포함해야 한다.
