# 공개 배포 가이드

이 문서는 `codex-harness`를 공식 Codex plugin 모델에 맞춰 어떻게 공개 배포할지 정리한다.

## 현재 상태

`codex-harness`는 Codex plugin 형태로 패키징되어 있다. 현재 실질적인 배포 경로는 다음 셋이다:

1. repo marketplace 설치
2. personal marketplace 설치
3. GitHub 오픈소스 저장소로 공개

현재 기준으로 Codex 공식 Plugin Directory에 대한 self-serve 공개 퍼블리싱은 아직 제공되지 않는다. 공식 문서에서는 public plugin publishing이 "coming soon"이라고 안내한다.

## 배포 모델

Codex plugin은 다음을 함께 묶을 수 있는 설치 단위다:

- skills
- apps
- MCP server 설정

`codex-harness`의 핵심 번들은 `harness` skill과 로컬 플러그인 메타데이터다:

- `plugins/harness/.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`

## 현재 시점의 권장 공개 배포 방식

오늘 기준 권장 방식:

1. 이 저장소를 GitHub의 canonical plugin source로 공개한다.
2. 플러그인 폴더는 `plugins/harness`에 유지한다.
3. `.agents/plugins/marketplace.json`에 repo-scoped marketplace 예시를 유지한다.
4. README에서 repo marketplace와 personal marketplace 설치법을 둘 다 제공한다.
5. `codex-harness-100`은 설치 번들이 아니라 companion example library로 설명한다.

## Repo Marketplace로 설치

팀이 특정 저장소 안에서만 플러그인을 쓰고 싶을 때 적합하다.

### 권장 구조

```text
$REPO_ROOT/
├── .agents/
│   └── plugins/
│       └── marketplace.json
└── plugins/
    └── harness/
```

### 절차

1. 플러그인을 `$REPO_ROOT/plugins/harness`에 복사하거나 클론한다.
2. `$REPO_ROOT/.agents/plugins/marketplace.json`을 추가 또는 갱신한다.
3. 플러그인 엔트리가 `./plugins/harness`를 가리키게 한다.
4. Codex를 재시작한다.
5. Plugin Directory에서 repo marketplace를 선택한다.
6. `harness`를 설치한다.
7. 새 스레드를 열고 플러그인을 사용하도록 요청한다.

### 예시

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

## Personal Marketplace로 설치

개인이 여러 저장소에서 같은 플러그인을 쓰고 싶을 때 적합하다.

### 권장 구조

```text
~/.agents/plugins/marketplace.json
~/.codex/plugins/harness
```

### 절차

1. 플러그인을 `~/.codex/plugins/harness`에 복사하거나 클론한다.
2. `~/.agents/plugins/marketplace.json`을 추가 또는 갱신한다.
3. marketplace root 기준 상대경로로 `./` 접두사를 붙여 플러그인 경로를 지정한다.
4. Codex를 재시작한다.
5. Plugin Directory에서 해당 marketplace를 선택하고 `harness`를 설치한다.

## 중요한 경로 규칙

공식 문서 기준 핵심 규칙:

- `source.path`는 `./`로 시작해야 한다
- `source.path`는 marketplace root 기준 상대경로로 해석된다
- plugin manifest 내부 경로는 plugin root 기준 상대경로여야 한다
- 필수 entry point는 `.codex-plugin/plugin.json`이다

## 설치 이후

설치 후에는:

- 번들된 skill이 Codex에서 사용 가능해진다
- plugin enable/disable 상태는 `~/.codex/config.toml`에 저장된다
- local plugin도 marketplace source를 직접 실행하는 것이 아니라 Codex cache에 설치된 복사본을 사용한다

local plugin 설치 경로:

```text
~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/local/
```

## Codex App / CLI에서 설치 진입

Codex app에서는:

- `Plugins`를 연다
- marketplace를 고른다
- `harness`를 설치한다

Codex CLI에서는:

```text
codex
/plugins
```

그 다음 marketplace를 선택해서 설치한다.

## 프로젝트 Trust 요구사항

`codex-harness`는 repo-local `.codex/config.toml`을 생성하고 사용한다. 공식 config 문서에 따르면 project-scoped `.codex/config.toml`은 프로젝트가 trusted 상태일 때만 로드된다.

즉, 설치만으로 끝나지 않는다. 대상 프로젝트도 trusted 상태로 열어야 repo-local agent config가 실제로 동작한다.

## Companion Repository

`codex-harness-100`은 companion repository로 설명하는 것이 맞다:

- `codex-harness` = generator plugin
- `codex-harness-100` = example / reference library

설치 필수 요소로 강제하지 말고, 선택적이지만 권장되는 reference dependency로 설명한다.

## 공식 문서

- Plugins: https://developers.openai.com/codex/plugins/
- Build plugins: https://developers.openai.com/codex/plugins/build
- Config reference: https://developers.openai.com/codex/config-reference/#configtoml
