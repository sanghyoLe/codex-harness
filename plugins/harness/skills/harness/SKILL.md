---
name: harness
description: "Codex-native 하네스를 구성, 확장, 점검합니다. 현재 저장소에 맞는 `AGENTS.md`, `.agents/skills/*/SKILL.md`, `.codex/config.toml`, `.codex/agents/*.toml`를 생성하거나 재구성할 때 사용합니다. '하네스 구성해줘', 'Codex 서브에이전트 워크플로우 설계해줘', '하네스 점검', '에이전트/스킬 동기화', '코드 리뷰 하네스 만들어줘' 같은 요청에서 적극적으로 사용합니다."
---

# Harness — Codex Workflow-Architecture Factory

Codex용 프로젝트 하네스를 설계하고 스캐폴드하는 메타 스킬이다. 목표는 현재 저장소의 도메인, 코드 구조, 작업 흐름에 맞춰 역할 분해, 오케스트레이션, 검증 루프를 만들고 이를 재사용 가능한 로컬 하네스로 남기는 것이다.

## 핵심 원칙

1. 결과물은 반드시 Codex-native 구조로 남긴다: `AGENTS.md`, `.agents/skills/`, `.codex/config.toml`, `.codex/agents/*.toml`.
2. 가능하면 `codex-harness-100`이나 upstream `harness-100` 계열 예시를 참고하되, 비-Codex 런타임 개념은 Codex 공식 표면으로 바꾼다.
3. `AGENTS.md`에는 하네스 포인터만 기록한다. 에이전트/스킬 전체 내용을 중복하지 말고 트리거 규칙, 주요 경로, 변경 이력만 남긴다.
4. 하네스는 고정물이 아니라 진화하는 시스템이다. 실행 후 피드백을 반영해 역할, 스킬, 오케스트레이터, `AGENTS.md` 포인터를 계속 갱신한다.
5. 역할 수는 최소화하되 역할 경계와 데이터 흐름은 명확하게 잡는다.

사용자가 명시적으로 원하지 않는 한 Codex 공식 표면이 아닌 런타임 구조나 용어는 만들지 않는다.

## 생성 대상

- `AGENTS.md`
- `.agents/skills/<orchestrator>/SKILL.md`
- 선택적 `.agents/skills/<supporting-skill>/SKILL.md`
- `.codex/config.toml`
- `.codex/agents/<role>.toml`
- 필요 시 `_workspace/` 작업 계약 및 변경 이력

## 워크플로우

### Phase 0: 현황 감사

하네스 스킬이 트리거되면 가장 먼저 기존 하네스 상태를 확인한다.

1. `AGENTS.md`, `.agents/skills/`, `.codex/agents/`, `.codex/config.toml` 존재 여부를 읽는다.
2. 실행 모드를 분기한다:
   - **신규 구축**: 하네스 파일이 없거나 비어 있음 -> Phase 0-1부터 전체 실행
   - **기존 확장**: 새 에이전트/스킬/패턴 추가 요청 -> 필요한 Phase만 실행
   - **운영/유지보수**: 점검, 감사, 동기화 요청 -> Phase 7-5로 이동
3. 기존 에이전트/스킬 목록과 `AGENTS.md` 포인터를 대조해 drift를 찾는다.
4. 기존 사용자의 변경을 보존해야 하므로, 전면 덮어쓰기보다 diff 기반 수정을 우선한다.

기존 확장 시 선택 매트릭스:

| 변경 유형 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|----------|---------|---------|---------|---------|---------|---------|
| 에이전트 추가 | 감사 결과 활용 | 배치 결정 | 필수 | 전용 스킬 필요 시 | 오케스트레이터 수정 | 필수 |
| 스킬 추가/수정 | 건너뜀 | 건너뜀 | 건너뜀 | 필수 | 연결 변경 시 | 필수 |
| 아키텍처 변경 | 감사 결과 활용 | 필수 | 영향받는 에이전트 | 영향받는 스킬 | 필수 | 필수 |

### Phase 0-1: 레퍼런스 검색

sibling 경로의 `codex-harness-100`을 1차 레퍼런스로 사용한다. 경로는 `find_reference_harness.py`가 자동으로 탐색한다.

```bash
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "code review" --limit 5
```

한국어 요청이면 `ko/*`, 영어 요청이면 `en/*` 레퍼런스를 먼저 본다. 선정한 레퍼런스는 새 spec의 `reference_harnesses`에 기록한다.

### Phase 1: 도메인 분석

사용자 요청과 현재 저장소에서 다음을 추출한다:

- 프로젝트/도메인
- 핵심 작업 유형: 생성, 편집, 분석, 검증, 연구, 구현
- 최종 산출물 형식과 기본 언어
- 순차 처리인지, 병렬 처리인지, 리뷰 중심인지, 동적 라우팅인지
- 외부 검색 필요 여부
- 기존 하네스와 충돌하거나 중복되는 지점
- 사용자의 숙련도 단서와 설명 깊이

요청이 모호해도 실용적인 기본값으로 진행한다. 하네스 구조가 크게 달라질 정도의 공백만 질문한다.

### Phase 2: 워크플로우 아키텍처 설계

`references/agent-design-patterns.md` 또는 `references/architecture-patterns.md`를 읽고 가장 작은 패턴을 선택한다:

- `pipeline`
- `fan-out/fan-in`
- `expert-pool`
- `producer-reviewer`
- `supervisor`
- `hierarchical-delegation`
- `hybrid`

실행 모드는 다음 중 하나로 표기한다. Codex는 subagent를 자동 라우팅하지 않으므로, 오케스트레이터 스킬은 필요한 역할을 명시적으로 spawn하도록 지시해야 한다.

- **Codex custom agents + explicit subagent workflow**: `.codex/agents/*.toml` 역할을 만들고, 오케스트레이터가 필요할 때 명시적으로 spawn하도록 설계한다. 기본값이다.
- **오케스트레이터 단독**: 작업이 작고 분업 가치가 없을 때 사용한다.
- **하이브리드**: 수집/분석/검증 Phase별로 역할 활성화 방식을 다르게 한다.

2개 이상의 독립 관점이 품질을 높이면 다역할 하네스를 쓰고, 결과물 하나를 선형으로 만드는 작은 요청이면 오케스트레이터 단독 또는 producer-reviewer로 축소한다. 깊은 재귀 위임은 `agents.max_depth`와 비용/예측 가능성 리스크를 고려해 기본적으로 피한다.

### Phase 3: 하네스 스펙 정의

파일을 쓰기 전에 최소한 아래 항목을 정리한다:

- 하네스 slug, title, summary, `language`
- 워크플로우 패턴과 실행 모드
- 오케스트레이터 스킬 이름과 trigger description
- 역할 1~6개와 각 역할의 output path
- 선택적 supporting skill
- `_workspace/` 계약
- `web_search` 기본값: `cached`, `live`, `disabled`
- 참고한 레퍼런스 하네스 목록

### Phase 4: 커스텀 에이전트 정의 생성

각 역할은 Codex custom agent 파일인 `.codex/agents/{name}.toml`로 남긴다. Codex 공식 문서 기준으로 이 파일은 프로젝트 범위 custom agent이며, 사용 시에는 명시적 subagent workflow에서 spawn된다.

필수 필드:

- `name`
- `description`
- `developer_instructions`

`developer_instructions`에는 최소한 다음을 포함한다:

- 핵심 역할
- 작업 원칙
- 입력/출력 프로토콜
- 산출물 기대치
- 부모 스레드/공유 워크스페이스 기반 조율 또는 handoff 규약
- 에러 핸들링

QA 역할은 단순 존재 확인이 아니라 경계면 교차 검증을 맡긴다. 예: API 응답 shape과 프론트 타입, 문서와 실제 구현, 테스트와 acceptance criteria.

### Phase 5: 스킬 생성

오케스트레이터 스킬은 `.agents/skills/<name>/SKILL.md`에 생성한다. 이 스킬은 추상 설명이 아니라 실제 실행 절차여야 한다.

포함 요소:

- activation rules와 narrow/full/follow-up 요청 구분
- 역할 구성과 활성화 기준
- Phase별 실행 순서
- 병렬 가능 구간과 순차 의존 구간
- 어떤 역할을 어떤 조건에서 명시적으로 spawn할지
- `_workspace/` 데이터 전달 규약
- 실패 시 폴백
- 최종 검증 기준

supporting skill은 반복 전문지식만 담는다. 오케스트레이터 workflow를 복붙하지 않는다.

### Phase 5-4: `AGENTS.md` 포인터 등록

`AGENTS.md`에는 다음만 간결히 남긴다:

- 이 저장소에 하네스가 있음을 알리는 섹션
- 시작 프롬프트와 오케스트레이터 스킬 경로
- custom agent/skill 디렉터리 경로
- `_workspace/` 사용 규칙
- 변경 이력 표

custom agent 목록과 스킬 전문은 `.codex/agents/`와 `.agents/skills/`가 단일 출처다. `AGENTS.md`에 중복해서 길게 쓰지 않는다.

### Phase 6: 검증

생성 후 반드시 점검한다:

- `[TODO]`, `{placeholder}` 같은 미해결 placeholder가 없는지
- 각 `.codex/agents/*.toml`에 `name`, `description`, `developer_instructions`가 있는지
- `.codex/config.toml`의 `web_search`, `[agents]` 설정이 Codex config reference에 맞는지
- 오케스트레이터 description이 실제 사용자 프롬프트를 잘 받는지
- 레퍼런스를 참고했다면 맹목적 복사가 아니라 현재 도메인에 맞게 변형했는지

검사용 예시:

```bash
rg -n "\\[TODO\\]|\\{[^}]+\\}|developer_instructions|^name =|^description =" AGENTS.md .agents .codex
```

### Phase 7: 하네스 진화 메커니즘

하네스 실행 후 다음 델타를 수집한다:

- 어떤 역할이 실제로 도움이 됐는가
- 어떤 역할이 중복이었는가
- 어떤 입력/출력 계약이 자주 깨졌는가
- 어떤 검증 기준이 누락됐는가
- 사용자가 반복해서 수정 요청한 지점은 무엇인가

피드백 유형별 수정 대상:

| 피드백 | 수정 대상 |
|--------|----------|
| 역할이 겹침 | `.codex/agents/*.toml`, 오케스트레이터 spawn 기준 |
| 스킬이 트리거되지 않음 | `SKILL.md` description |
| 산출물 형식이 흔들림 | 오케스트레이터 workspace contract, 역할 출력 프로토콜 |
| QA가 약함 | QA agent guide 기준 보강, 재검수 루프 |
| 후속 작업이 끊김 | `AGENTS.md` 포인터와 오케스트레이터 Phase 0 |

### Phase 7-5: 운영/유지보수

사용자가 "하네스 점검", "하네스 감사", "에이전트/스킬 동기화"를 요청하면:

1. 현재 파일 목록과 `AGENTS.md` 포인터를 대조한다.
2. 깨진 경로, orphan skill, 미등록 agent, 오래된 trigger를 찾는다.
3. 최소 수정으로 동기화한다.
4. 변경 이력에 날짜, 변경 내용, 대상, 사유를 기록한다.
5. `rg` 기반 검증을 실행한다.

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
  "language": "ko",
  "title": "코드 리뷰 하네스",
  "summary": "아키텍처, 보안, 성능, 스타일을 병렬로 검토하는 코드 리뷰 하네스.",
  "collaboration_pattern": "fan-out/fan-in",
  "execution_mode": "codex-custom-agents-explicit-subagents",
  "workspace_root": "_workspace",
  "web_search": "disabled",
  "orchestrator": {
    "name": "code-reviewer",
    "description": "넓은 범위의 코드 리뷰 하네스나 역할 기반 리뷰 워크플로우가 필요할 때 사용한다. 후속 리뷰, 부분 재검토, 기존 리뷰 보완 요청에도 사용한다."
  },
  "agents": [
    {
      "name": "security-analyst",
      "description": "보안 취약점과 인증/인가 리스크를 검토한다.",
      "output_path": "_workspace/01_security_review.md"
    }
  ]
}
```

## 참고 문서

- `references/architecture-patterns.md`
- `references/agent-design-patterns.md`
- `references/orchestrator-template.md`
- `references/team-examples.md`
- `references/skill-writing-guide.md`
- `references/skill-testing-guide.md`
- `references/qa-agent-guide.md`
- `references/reference-library.md`
- repo docs: `docs/quickstart.md`, `docs/experimental-dependency.md`, `CONTRIBUTING.md`
