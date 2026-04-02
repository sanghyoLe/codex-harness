# Codex Harness

**Codex용 Harness Architect**  
`AGENTS.md`, 저장소 로컬 스킬, 재사용 가능한 Codex 서브에이전트 역할 구성을 생성하는 프로젝트 맞춤형 하네스 생성기.

[English](README.md) | **한국어**  
[Publishing Guide](PUBLISHING.md) | [공개 배포 가이드](PUBLISHING_KO.md)

이 저장소는 Claude용 원본 `harness` 프로젝트를 Codex-native 플러그인과 메타 스킬로 옮긴 것이다. 목표는 같다. 사용자가 "하네스 구성해줘" 또는 "이 프로젝트에 맞는 harness 만들어줘"라고 요청하면, Codex가 도메인을 분석하고 협업 패턴을 고른 뒤, 전문 역할과 오케스트레이터 스킬을 포함한 재사용 가능한 로컬 하네스를 생성하게 만드는 것이다.

## Codex에게 이렇게 요청하면 된다

의도한 사용 방식은 "이 저장소를 클론해서 파일을 수작업으로 베끼기"가 아니다. 더 간단한 방식은 Codex에게 `codex-harness` 저장소를 참고해서 새 하네스를 만들어 달라고 요청하는 것이다.

즉, Codex가 이 저장소를 보고, 포함된 예제를 참고하고, 같은 스타일로 원하는 도메인용 하네스를 생성하게 만들면 된다.

예시 프롬프트:

```text
codex-harness를 참고해서 일본 여행 길라잡이 웹 서비스 하네스 만들어줘
```

핵심 패턴은 이것이다. `codex-harness`를 레퍼런스로 쓰라고 지정하고, 그다음 어떤 제품이나 워크플로우를 위한 하네스를 만들고 싶은지 설명하면 된다.

## 빠른 설치

현재 사용자가 설치하는 현실적인 경로는 `repo marketplace` 또는 `personal marketplace`다. 공식 public Plugin Directory에 self-serve로 올려서 바로 설치하는 방식은 아직 지원되지 않는다.

### 옵션 1: 특정 저장소에만 설치

팀이 하나의 프로젝트 안에서만 `codex-harness`를 쓰고 싶을 때 적합하다.

1. 이 플러그인을 `$REPO_ROOT/plugins/harness`에 복사한다.
2. 이 marketplace 파일을 `$REPO_ROOT/.agents/plugins/marketplace.json`에 복사한다:
   - `./.agents/plugins/marketplace.json`
3. Codex를 재시작한다.
4. Codex 앱에서 `Plugins`를 열거나, CLI에서 아래를 실행한다:

```text
codex
/plugins
```

5. repo marketplace를 선택하고 `harness`를 설치한다.

Repo marketplace 파일 예시:

```json
{
  "name": "codex-harness-local",
  "interface": {
    "displayName": "Codex Harness Local"
  },
  "plugins": [
    {
      "name": "harness",
      "source": {
        "source": "local",
        "path": "./plugins/harness"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

### 옵션 2: 한 사용자가 여러 저장소에서 공통 사용

1. `plugins/harness`를 `~/.codex/plugins/harness`에 복사한다.
2. `~/.agents/plugins/marketplace.json`에 personal marketplace 파일을 만든다.
3. `source.path`가 설치된 플러그인을 `./` 접두사의 상대경로로 가리키게 한다.
4. Codex를 재시작한 뒤 해당 marketplace에서 `harness`를 설치한다.

Personal marketplace 파일 예시:

```json
{
  "name": "codex-harness-personal",
  "interface": {
    "displayName": "Codex Harness Personal"
  },
  "plugins": [
    {
      "name": "harness",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/harness"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

전체 예시와 파일 포맷은 [PUBLISHING_KO.md](PUBLISHING_KO.md)에 정리했다.

## 개요

`codex-harness`는 생성기다. 완성된 100개 하네스를 담은 카탈로그가 아니라, 현재 프로젝트에 맞는 새 하네스를 만든다.

생성 대상:

- `AGENTS.md`
- `.agents/skills/` 아래의 오케스트레이터 스킬
- 선택적 supporting skill
- `.codex/agents/` 아래의 서브에이전트 역할 설정
- `.codex/config.toml`

기본 sibling 경로인 `/Users/isanghyo/Desktop/harness/codex-harness-100`이 있으면, 이 저장소는 그 레퍼런스 라이브러리를 우선적으로 참고해야 한다.

## 핵심 기능

- **하네스 아키텍처 설계**: pipeline, fan-out/fan-in, expert pool, generate-critique, supervisor, hierarchical delegation 패턴 선택
- **Reference-First 생성**: `codex-harness-100`에서 가까운 예시를 찾고, 그대로 복사하지 않고 구조만 적응
- **Codex-Native 산출물**: Claude 전용 `.claude/` 대신 `AGENTS.md`, `.agents`, `.codex` 구조 생성
- **재사용 가능한 스캐폴딩**: 레퍼런스 검색과 JSON spec 기반 생성 스크립트 포함
- **검증 중심 구성**: 역할 경계, workflow, 출력 계약, placeholder 정리 기준까지 포함

## 워크플로우

```text
Phase 1: 도메인 분석
    ↓
Phase 2: 협업 패턴 설계
    ↓
Phase 3: 서브에이전트 역할 정의 (.codex/agents/)
    ↓
Phase 4: 스킬 생성 (.agents/skills/)
    ↓
Phase 5: 오케스트레이션 & 워크스페이스 계약
    ↓
Phase 6: 검증 & 정제
```

## `codex-harness-100`과의 관계

두 저장소의 역할은 다르다:

- `codex-harness`: 생성기 플러그인 / 메타 스킬
- `codex-harness-100`: 완성형 하네스 예시 라이브러리

권장 흐름:

1. 현재 저장소에 맞는 하네스를 만들어 달라고 요청한다.
2. `codex-harness-100`이 있으면 `harness` 스킬이 그 안에서 가까운 하네스를 찾는다. 없어도 `codex-harness` 단독으로 하네스를 생성할 수 있어야 한다.
3. 상위 1~3개 예시를 읽는다.
4. 역할 구조와 출력 계약을 현재 프로젝트에 맞게 조정한다.
5. 새 로컬 하네스를 스캐폴드하고 다듬는다.

## 설치

공식 Codex plugin 문서 기준으로 이 프로젝트와 직접 관련 있는 설치 surface는 세 가지다:

1. Codex 안의 Plugin Directory
2. `$REPO_ROOT/.agents/plugins/marketplace.json` 기반 repo marketplace
3. `~/.agents/plugins/marketplace.json` 기반 personal marketplace

현재 `codex-harness`는 repo / personal marketplace 배포에 맞춰 정리되어 있다. 공식 Plugin Directory에 대한 self-serve 공개 퍼블리싱은 아직 coming soon 상태다.

### Repo marketplace

팀이 하나의 저장소 안에서만 플러그인을 쓰고 싶을 때 적합하다.

1. 플러그인 폴더를 `$REPO_ROOT/plugins/harness`에 둔다.
2. `$REPO_ROOT/.agents/plugins/marketplace.json`을 추가하거나 갱신한다.
3. 플러그인 엔트리가 `./plugins/harness`를 가리키게 한다.
4. Codex를 재시작한다.
5. Plugin Directory에서 `harness`를 설치한다.

이 저장소에는 필요한 로컬 메타데이터가 이미 포함되어 있다:

- `.agents/plugins/marketplace.json`
- `plugins/harness/.codex-plugin/plugin.json`

### Personal marketplace

개인이 여러 저장소에서 같은 플러그인을 쓰고 싶을 때 적합하다.

1. 플러그인을 `~/.codex/plugins/harness`에 복사한다.
2. `~/.agents/plugins/marketplace.json`을 추가하거나 갱신한다.
3. `./`로 시작하는 상대경로로 플러그인 위치를 지정한다.
4. Codex를 재시작하고 해당 marketplace에서 `harness`를 설치한다.

### 직접 로컬 사용

플러그인 설치 전에 메타 스킬을 계속 다듬고 싶다면:

1. 이 저장소를 Codex에서 연다.
2. `plugins/harness/skills/harness/`를 메인 스킬 소스로 사용한다.
3. 번들된 스크립트로 레퍼런스를 검색하고 현재 프로젝트에 하네스를 생성한다.

repo marketplace, personal marketplace, 공개 배포 상태는 [PUBLISHING_KO.md](PUBLISHING_KO.md)에 별도로 정리했다.

## 저장소 구조

```text
codex-harness/
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── plugins/
│   └── harness/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── harness/
│               ├── SKILL.md
│               ├── agents/openai.yaml
│               ├── references/
│               │   ├── architecture-patterns.md
│               │   ├── reference-library.md
│               │   ├── orchestrator-template.md
│               │   ├── team-examples.md
│               │   ├── skill-writing-guide.md
│               │   ├── skill-testing-guide.md
│               │   └── qa-agent-guide.md
│               └── scripts/
│                   ├── find_reference_harness.py
│                   └── scaffold_harness.py
├── examples/
│   └── code-reviewer/
│       ├── spec.json
│       ├── AGENTS.md
│       ├── .agents/...
│       └── .codex/...
│   └── fullstack-webapp/
│       ├── spec.json
│       ├── AGENTS.md
│       ├── .agents/...
│       └── .codex/...
└── README.md
```

## 사용법

다음과 같은 프롬프트로 트리거한다:

```text
하네스 구성해줘
이 프로젝트에 맞는 에이전트 팀 설계해줘
research harness 만들어줘
코드 리뷰 하네스 만들어줘
fullstack-webapp 하네스 설계해줘
```

### 협업 패턴

| 패턴 | 적합한 경우 |
|------|------------|
| Pipeline | 순차 의존 단계 |
| Fan-out / Fan-in | 병렬 분석 후 종합 |
| Expert Pool | 조건부 전문가 호출 |
| Generate-Critique | 생성자 + 검수자 |
| Supervisor | 중간 결과에 따른 동적 라우팅 |
| Hierarchical Delegation | 큰 범위의 다층 workstream |

### 전형적인 산출물

```text
your-project/
├── AGENTS.md
├── .agents/
│   └── skills/
│       ├── orchestrator/
│       │   └── SKILL.md
│       └── supporting-skill/
│           └── SKILL.md
└── .codex/
    ├── config.toml
    └── agents/
        ├── researcher.toml
        ├── researcher.md
        ├── reviewer.toml
        └── reviewer.md
```

## 레퍼런스 검색

하네스를 처음부터 설계하지 말고 먼저 검색한다:

```bash
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "code review" --limit 5
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "youtube seo thumbnail" --language ko
```

이 스크립트는 `codex-harness-100`을 스캔해서 가장 가까운 하네스를 보여준다.

## 스캐폴딩

JSON spec에서 새 하네스를 생성할 수 있다:

```bash
python3 plugins/harness/skills/harness/scripts/scaffold_harness.py \
  --spec /tmp/harness-spec.json \
  --target .
```

생성되는 항목:

- `AGENTS.md`
- `.agents/skills/<skill>/SKILL.md`
- `.codex/config.toml`
- `.codex/agents/<role>.toml`
- `.codex/agents/<role>.md`

스크립트는 이름을 Codex-friendly slug로 정규화해 config와 실제 파일 경로가 어긋나지 않게 만든다.

## 예제 산출물

생성된 샘플 하네스는 `examples/code-reviewer/`에 들어 있다. 포함 내용:

- 입력 spec: `examples/code-reviewer/spec.json`
- 생성된 `AGENTS.md`
- 생성된 `.agents/skills/`
- 생성된 `.codex/` 역할 설정

추가로 `examples/fullstack-webapp/`에는 더 순차적인 delivery workflow를 검증하는 샘플이 들어 있다. 아키텍처, 프론트엔드, 백엔드, QA, 배포 역할 분해가 포함된다.

## 예시 사용 사례

**딥 리서치**

```text
Build a harness for deep research. I need a team that can investigate any topic
from multiple angles, cross-check sources, and produce a structured report.
```

**웹사이트 개발**

```text
풀스택 웹사이트 개발 하네스를 구성해줘. 디자인, 프론트엔드, 백엔드, QA를
와이어프레임부터 배포까지 조율하는 구조가 필요해.
```

**코드 리뷰**

```text
종합 코드 리뷰 하네스를 구성해줘. 아키텍처, 보안, 성능, 코드 스타일을 병렬로
점검하고 마지막에 결과를 하나의 보고서로 통합해줘.
```

**콘텐츠 제작**

```text
Build a harness for YouTube content production. The team should research topics,
write scripts, optimize SEO, and plan thumbnails with a clear review step.
```

## 범위

이 저장소는 하네스 생성기다. 완성형 하네스 카탈로그는 `codex-harness-100`의 역할이다.

## 공식 문서

- [Codex Plugins](https://developers.openai.com/codex/plugins/)
- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [Config reference](https://developers.openai.com/codex/config-reference/#configtoml)

## 라이선스

Apache 2.0
