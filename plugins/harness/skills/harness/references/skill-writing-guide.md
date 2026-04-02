# Skill Writing Guide

하네스가 생성하는 스킬의 품질은 description과 workflow의 선명도에서 결정된다. 멋있는 문장보다 트리거 정확도와 실행 가능성이 중요하다.

## 1. Description 작성 원칙

description에는 반드시 세 가지가 있어야 한다:

- 이 스킬이 무엇을 하는가
- 어떤 사용자 요청에서 트리거되어야 하는가
- 어떤 경우에는 쓰지 않아야 하는가

좋은 예:

```yaml
description: "종합 코드 리뷰 하네스를 조율한다. 사용자가 '코드 리뷰 하네스 만들어줘', '이 저장소에 맞는 리뷰 팀 설계해줘', '아키텍처/보안/성능을 병렬 점검하는 구조를 만들어줘' 같은 요청을 할 때 사용한다. 단순 단일 파일 리뷰만 필요한 경우에는 전체 하네스를 강제하지 않는다."
```

나쁜 예:

```yaml
description: "엔지니어링 작업을 돕는 스킬"
```

## 2. 본문 작성 원칙

### Procedural, Not Inspirational

오케스트레이터 스킬은 절차를 써야 한다.

좋다:

- 어떤 파일을 읽는지
- 어떤 역할을 활성화하는지
- 어떤 출력 경로에 쓰는지
- 언제 검증하는지

나쁘다:

- "신중하게 생각한다"
- "고품질 결과를 만든다"
- "철저하게 검토한다"

### Why-First

규칙만 쓰지 말고 왜 그런지 짧게 설명한다. 이유가 있으면 도메인이 조금 달라져도 판단이 유지된다.

### Keep It Lean

스킬 본문에는 실행에 필요한 내용만 둔다. 긴 배경지식은 `references/`로 분리한다.

## 3. 오케스트레이터와 supporting skill의 역할 분리

오케스트레이터가 가져야 할 것:

- workflow
- activation rules
- mode switching
- dependency order
- validation

supporting skill이 가져야 할 것:

- 특정 전문영역 체크리스트
- 반복 기준
- 도메인별 세부 rubric
- 자주 쓰는 reference

supporting skill이 가져서는 안 되는 것:

- 오케스트레이터 workflow의 복제
- 전체 하네스 설명의 반복

## 4. 출력 형식 정의

형식이 중요하면 섹션 이름과 기대 내용을 분명히 쓴다.

예:

```markdown
## Review Output Format

# Executive Summary
## Critical Findings
## Medium-Risk Findings
## Suggested Follow-Ups
## Files Reviewed
```

형식만 강요하지 말고, 어떤 내용을 넣어야 하는지도 함께 적는다.

## 5. 예시 사용법

긴 설명보다 짧은 예시가 낫다. 특히 트리거 설명과 출력 포맷에는 예시가 효과적이다.

예:

```markdown
좋은 트리거 예:
- "하네스 구성해줘"
- "이 프로젝트에 맞는 에이전트 팀 설계해줘"
- "코드 리뷰용 역할 분해 구조 만들어줘"

좋은 narrow trigger 예:
- "기존 하네스를 QA 중심으로 재구성해줘"
```

## 6. Progressive Disclosure

reference가 길어질수록 바로 본문에 넣지 말고 조건부로 분리한다.

좋은 구조:

```text
skill/
├── SKILL.md
└── references/
    ├── qa-agent-guide.md
    ├── architecture-patterns.md
    └── skill-testing-guide.md
```

SKILL.md에서는:

- 언제 어떤 reference를 읽어야 하는지 지시한다
- reference 전문을 중복해서 붙이지 않는다

## 7. 스크립트 번들링 기준

다음 신호가 보이면 스크립트로 번들링한다:

- 같은 JSON spec 초안 생성이 반복된다
- 이름 정규화, 파일 생성, 일관성 검사가 반복된다
- 테스트에서 매번 비슷한 shell 절차를 재생산한다

반대로 스크립트로 만들지 말아야 하는 경우:

- 한 번만 쓰는 문서 편집
- 도메인별 판단이 많은 작업
- 작은 규칙 한 줄이면 충분한 경우

## 8. 스킬에 넣지 않을 것

- 모델이 이미 충분히 아는 일반론
- 긴 홍보 문구
- 도메인과 무관한 잡다한 팁
- 오케스트레이터가 직접 쓰지 않을 세부 자료

## 9. 최종 체크

스킬을 쓴 뒤 아래 질문에 "예"라고 답할 수 있어야 한다:

- 실제 사용자 문장으로 트리거될 것 같은가
- 누가 무엇을 언제 하는지 분명한가
- supporting skill과 역할 분담이 겹치지 않는가
- output path와 validation 기준이 명확한가
