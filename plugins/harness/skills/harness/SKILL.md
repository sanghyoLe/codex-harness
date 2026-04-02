---
name: harness
description: "하네스를 구성합니다. 현재 저장소에 맞는 Codex-native 하네스를 설계하고 `AGENTS.md`, `.agents/skills/*/SKILL.md`, `.codex/config.toml`, `.codex/agents/*.toml`, `.codex/agents/*.md`를 생성하거나 재구성할 때 사용합니다. '하네스 구성해줘', '에이전트 팀 설계해줘', 'research harness 만들어줘', '코드 리뷰 하네스 만들어줘' 같은 요청에서 적극적으로 사용합니다."
---

# Harness

Codex용 프로젝트 하네스를 설계하고 스캐폴드하는 메타 스킬이다. 목표는 현재 저장소에 맞는 역할 분해, 오케스트레이션, 검증 구조를 만들고, 이를 재사용 가능한 로컬 하네스로 남기는 것이다.

## 핵심 원칙

1. 결과물은 반드시 Codex-native 구조로 남긴다.
2. 가능하면 `codex-harness-100`을 먼저 참고하고, 필요할 때만 새 구조를 발명한다.
3. 역할 수는 최소화하되 역할 경계는 날카롭게 잡는다.
4. 오케스트레이터 스킬은 추상적 설명이 아니라 실행 절차를 담아야 한다.
5. 생성된 하네스는 다음 세션에서도 그대로 재사용 가능해야 한다.

## 생성 대상

기본 산출물:

- `AGENTS.md`
- `.agents/skills/<orchestrator>/SKILL.md`
- 선택적 `.agents/skills/<supporting-skill>/SKILL.md`
- `.codex/config.toml`
- `.codex/agents/<role>.toml`
- `.codex/agents/<role>.md`

사용자가 명시적으로 원하지 않는 한 Claude 전용 `.claude/` 구조는 만들지 않는다.

## 워크플로우

### Phase 0: 레퍼런스 라이브러리 검색

기본적으로 sibling 경로의 `codex-harness-100`을 1차 레퍼런스로 사용한다. 일반적인 기본 위치는 `/Users/isanghyo/Desktop/harness/codex-harness-100`이다. 처음부터 팀 구조를 상상으로 만들지 말고, 먼저 가까운 사례를 찾는다.

가능하면 아래 스크립트를 먼저 실행한다:

```bash
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "code review" --limit 5
```

선정된 하네스에서는 보통 다음 파일을 우선 읽는다:

- `AGENTS.md`
- 메인 오케스트레이터 `SKILL.md`
- 대표 역할 1~2개의 `.codex/agents/*.md`

선택한 레퍼런스는 새 하네스의 `reference_harnesses`에 기록한다.

### Phase 1: 도메인 분석

사용자 요청과 현재 저장소에서 다음을 추출한다:

- 프로젝트/도메인
- 핵심 작업 유형: 생성, 편집, 분석, 검증, 연구, 구현
- 최종 산출물 형식
- 순차 처리인지, 병렬 처리인지, 리뷰 중심인지, 동적 라우팅인지
- 외부 검색이 필요한지
- 기존 `AGENTS.md`, `.agents`, `.codex`와 충돌 가능성이 있는지

요청이 다소 모호해도 실용적인 기본값을 추론해서 진행한다. 하네스 구조가 크게 달라질 정도의 공백만 질문한다.

### Phase 2: 협업 패턴 설계

`references/architecture-patterns.md`를 읽고 가장 작은 패턴을 선택한다:

- `pipeline`
- `fan-out/fan-in`
- `expert-pool`
- `generate-critique`
- `supervisor`
- `hierarchical-delegation`

기본 판단 기준:

- 병렬 독립 분석 후 종합이면 `fan-out/fan-in`
- 생성 후 품질 검수가 핵심이면 `generate-critique`
- 중간 결과에 따라 라우팅이 달라지면 `supervisor`
- 역할이 1~2개로 충분하면 과도한 팀 구조를 만들지 않는다

### Phase 3: 하네스 스펙 정의

파일을 쓰기 전에 최소한 아래 항목을 먼저 정리한다:

- 하네스 slug
- 하네스 제목
- 한 줄 요약
- 협업 패턴
- 오케스트레이터 스킬 이름과 트리거 설명
- 서브에이전트 2~6개
- 선택적 supporting skill
- 작업 중간 산출물 위치
- 최종 산출물 위치
- `web_search` 기본값
- 참고한 레퍼런스 하네스 목록

참조 문서:

- `references/orchestrator-template.md`
- `references/team-examples.md`
- `references/skill-writing-guide.md`
- `references/skill-testing-guide.md`
- `references/qa-agent-guide.md`
- `references/reference-library.md`

### Phase 4: 역할 정의 생성

각 역할은 `.codex/agents/{name}.toml` + `.codex/agents/{name}.md`로 남긴다.

역할 정의 파일에는 최소한 다음이 있어야 한다:

- 핵심 역할
- 작업 원칙
- 산출물 기대치
- 협업 또는 전달 프로토콜
- 에러 핸들링

역할 작성 규칙:

- 설명은 "무슨 전문가인가"보다 "무엇을 내놓는가" 중심으로 쓴다
- 역할 간 책임이 겹치면 검수 역할이 아닌 한 분리 기준을 다시 잡는다
- 검수자가 있다면 리뷰 기준과 병합 책임을 명시한다
- QA 역할은 단순 존재 확인이 아니라 경계면 비교와 정합성 검증을 맡긴다

### Phase 5: 스킬 생성

오케스트레이터 스킬은 `.agents/skills/<name>/SKILL.md`에 생성한다. 이 스킬은 실제 작업 순서를 담아야 하며, 다음 요소를 포함해야 한다:

- 사용자 요청 해석
- 어떤 역할을 언제 쓸지 판단하는 기준
- 병렬 처리와 의존 관계
- 중간 산출물 경로
- 실패 시 폴백
- 최종 검증 기준

supporting skill은 반복 전문지식만 담는다. 메인 스킬의 절차를 복붙하지 않는다.

### Phase 6: 오케스트레이션과 검증

생성 후 반드시 다음을 점검한다:

- `[TODO]` 플레이스홀더가 남지 않았는지
- `.codex/config.toml`의 `config_file` 경로가 실제 파일과 일치하는지
- 각 `.toml`의 `model_instructions_file`이 실제 `.md`와 일치하는지
- 오케스트레이터 description이 실제 사용자 프롬프트를 잘 받는지
- 레퍼런스를 참고했다면 맹목적 복사가 아니라 의도적 변형인지

검사용 예시:

```bash
rg -n "\\[TODO\\]|config_file|model_instructions_file" AGENTS.md .agents .codex
```

## 파일 작성 규칙

### `AGENTS.md`

반드시 포함:

- 하네스 목적
- Codex 구조 설명
- 사용 스킬 목록
- 서브에이전트 역할 목록
- 시작 프롬프트 또는 추천 진입점
- 출력 위치
- 레퍼런스 계보가 있다면 그 근거

### `.codex/config.toml`

반드시 포함:

- `web_search` 설정
- `multi_agent` 여부
- 각 역할의 설명
- 각 역할의 `config_file`

### 역할별 `.md`

가능하면 다음 섹션을 쓴다:

- `## Core Responsibilities`
- `## Working Principles`
- `## Deliverable Expectations`
- `## Team Communication Protocol`
- `## Error Handling`

### 오케스트레이터 `SKILL.md`

반드시 절차형이어야 한다. "좋은 결과를 내라" 같은 모호한 문장은 금지한다. Phase 순서, 위임 기준, 병렬 처리 조건, 결과 통합 규칙을 써야 한다.

## 설계 제약

- 역할 수는 보통 2~6개로 제한한다
- 하네스가 작을수록 유지보수성이 높다
- 리뷰 역할이 없다면 오케스트레이터가 최소한의 검증 책임을 진다
- supporting skill은 정말 반복 가치가 있을 때만 만든다
- 실서비스 저장소에 추가하는 경우 기존 문체와 구조를 존중한다

## 품질 기준

좋은 하네스는 최소한 아래 셋 중 둘 이상을 분명히 개선해야 한다:

1. 작업 분해 품질
2. 역할 전문성
3. 최종 검증 신뢰도

이 개선이 없다면 하네스를 단순화한다.

## 스캐폴딩 절차

가능하면 번들된 스크립트를 사용한다:

```bash
python3 plugins/harness/skills/harness/scripts/scaffold_harness.py \
  --spec /tmp/harness-spec.json \
  --target .
```

최소 spec 예시:

```json
{
  "slug": "code-reviewer",
  "title": "Code Reviewer Harness",
  "summary": "Parallel code review harness for architecture, security, performance, and style.",
  "collaboration_pattern": "fan-out/fan-in",
  "workspace_root": "_workspace",
  "orchestrator": {
    "name": "code-reviewer",
    "description": "Use when the user asks for a broad code review harness."
  },
  "agents": [
    {
      "name": "security-analyst",
      "role_title": "Security Analyst",
      "description": "Find exploitable issues, insecure defaults, and trust-boundary violations."
    }
  ],
  "reference_harnesses": [
    {
      "path": "/Users/isanghyo/Desktop/harness/codex-harness-100/ko/21-code-reviewer",
      "reason": "Closest existing code review harness."
    }
  ]
}
```

스캐폴딩 후에는 생성된 일반 템플릿을 현재 프로젝트의 실제 도메인 언어로 반드시 치환한다.
