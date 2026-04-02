# Task Handoff Document

## 작업 개요
원래 `harness-100`(Claude Code용 하네스 컬렉션)을 Codex용으로 변환하는 작업에서 시작했지만, 이후 사용자의 의도를 다시 확인한 결과 핵심 목표는 `harness-100` 카탈로그가 아니라, 원본 `Harness`처럼 "하네스 구성해줘" 요청으로 새 하네스를 생성할 수 있는 **Codex용 오픈소스 배포물**을 만드는 것이었다.

현재는 두 갈래 작업이 생긴 상태다:

- `codex-harness-100`: 기존 `harness-100`을 Codex 포맷으로 변환한 카탈로그/레퍼런스 저장소
- `codex-harness`: 새 하네스를 생성하는 Codex용 메타 스킬/플러그인 저장소. 실제 경로는 `/Users/isanghyo/Desktop/harness/codex-harness`

## 현재 상태
작업은 아직 중간 단계다.

1. `codex-harness-100` 쪽은 대량 변환이 이미 들어간 상태다.
2. `codex-harness` 쪽은 메타 스킬/플러그인으로 설계 방향을 잡았고, 실제 파일은 `/Users/isanghyo/Desktop/harness/codex-harness`에 있다.
3. 현재 저장소 루트에 있는 `codex-harness` 엔트리는 `/Users/isanghyo/Desktop/codex-harness`를 가리키는 **잘못된 symlink**이며, 실제 작업물 위치와 다르다.

즉, 다음 에이전트는 `codex-harness` 작업을 이어갈 때 `/Users/isanghyo/Desktop/harness/codex-harness`를 기준으로 보면 된다. 현재 저장소 안의 symlink는 정리 대상이다.

중요한 판단 변경:

- 처음에는 `AGENTS.md + .agents + .codex` 복사형 사용 흐름으로 설명했는데, 이건 사용자의 의도와 어긋났다.
- 이후 OpenAI 공식 문서를 다시 확인한 결과, Codex에는 실제로 `plugin` 개념이 있으며:
  - skills는 authoring format
  - plugins는 installable distribution unit
  - local/personal/repo marketplace를 통해 설치 가능
  - 다만 official public plugin directory에 대한 self-serve publishing은 아직 coming soon

따라서 최종 방향은:

1. `codex-harness`를 GitHub 오픈소스용 Codex plugin repo로 재정비
2. `codex-harness-100`은 companion examples/reference repo로 위치시킴
3. README에서 local marketplace / repo marketplace 설치법을 공식 문서 기준으로 제공

## 시도한 내용

### 성공한 것
- 원본 `harness-100`을 Codex용 구조로 변환하는 스크립트를 만들고, `codex-harness-100`에 반영했다.
- 원래 작업 폴더를 `/Users/isanghyo/Desktop/codex-harness-100`로 이동했다.
- `codex-harness-100`의 README류에 이 저장소가 원본 `harness-100`을 클론해 Codex용으로 바꾼 것임을 명시했다.
- `codex-harness-100`에서 `AGENTS.md`, `.agents/skills/*/SKILL.md`, `.codex/config.toml`, `.codex/agents/*` 구조가 생성되도록 반영했다.
- OpenAI 공식 문서를 확인해서 Codex 배포 모델을 다시 정리했다:
  - Customization: https://developers.openai.com/codex/concepts/customization/
  - Skills: https://developers.openai.com/codex/skills/
  - Plugins: https://developers.openai.com/codex/plugins/
  - Build plugins: https://developers.openai.com/codex/plugins/build
  - Team Config: https://developers.openai.com/codex/enterprise/admin-setup/#step-4-standardize-local-configuration-with-team-config
- 위 문서 근거로 다음 결론을 확보했다:
  - skills는 authoring format
  - plugins는 installable distribution unit
  - repo marketplace / personal marketplace 설치는 공식 지원
  - official public plugin directory self-serve publishing은 아직 아님

### 실패한 것
- 처음에 사용자 의도를 `harness-100 컬렉션을 Codex에서 쓰는 저장소`로 해석해 설명했다. 사용자 의도는 `하네스 생성기` 쪽이었음.
- Codex 공개 배포 방식을 충분히 확인하기 전에 복사형 배포 흐름으로 설명했다.
- 현재 저장소 안의 `codex-harness` symlink는 잘못된 대상(`/Users/isanghyo/Desktop/codex-harness`)를 가리킨다.
- 실제 작업물은 `/Users/isanghyo/Desktop/harness/codex-harness`에 있으므로, symlink와 실제 경로가 불일치한다.
- 따라서 다음 에이전트는 symlink 정리 또는 경로 통합을 먼저 해야 한다.

## 다음 단계
다음 에이전트가 해야 할 일:

1. `codex-harness` 경로 정리
   - 실제 작업 위치는 `/Users/isanghyo/Desktop/harness/codex-harness`
   - 현재 저장소 안의 `codex-harness` symlink는 잘못된 대상이므로 정리 또는 교체 필요
2. `codex-harness`를 GitHub 공개용 오픈소스 플러그인 repo로 재정비
3. README를 공식 Codex plugin 설치 흐름 기준으로 다시 작성
   - repo marketplace 설치
   - personal marketplace 설치
   - plugin install/use 흐름
   - `codex-harness-100`을 companion reference repo로 설명
4. `codex-harness-100`과의 관계를 명확히 정리
   - `codex-harness` = generator
   - `codex-harness-100` = reference/examples library
5. 필요하면 `codex-harness-100` 안에 있는 현재 잘못된 symlink `codex-harness` 정리
6. 사용자가 원하면 이후 GitHub 공개 전:
   - git init / remote / README polish / LICENSE / install docs / example prompts 준비

## 관련 파일
- 현재 저장소 루트 문서:
  - `/Users/isanghyo/Desktop/codex-harness-100/README.md`
  - `/Users/isanghyo/Desktop/codex-harness-100/README_ko.md`
  - `/Users/isanghyo/Desktop/codex-harness-100/HANDOFF.md`
- 언어별 소개:
  - `/Users/isanghyo/Desktop/codex-harness-100/en/README.md`
  - `/Users/isanghyo/Desktop/codex-harness-100/ko/README.md`
  - `/Users/isanghyo/Desktop/codex-harness-100/ko/harness-100-cases.md`
- 대표 레퍼런스 하네스:
  - `/Users/isanghyo/Desktop/codex-harness-100/ko/21-code-reviewer/AGENTS.md`
  - `/Users/isanghyo/Desktop/codex-harness-100/ko/16-fullstack-webapp/AGENTS.md`
  - `/Users/isanghyo/Desktop/codex-harness-100/ko/01-youtube-production/AGENTS.md`
- 실제 메타 플러그인 작업 경로:
  - `/Users/isanghyo/Desktop/harness/codex-harness/README.md`
  - `/Users/isanghyo/Desktop/harness/codex-harness/.agents/plugins/marketplace.json`
  - `/Users/isanghyo/Desktop/harness/codex-harness/plugins/harness/.codex-plugin/plugin.json`
  - `/Users/isanghyo/Desktop/harness/codex-harness/plugins/harness/skills/harness/SKILL.md`
  - `/Users/isanghyo/Desktop/harness/codex-harness/plugins/harness/skills/harness/references/reference-library.md`
  - `/Users/isanghyo/Desktop/harness/codex-harness/plugins/harness/skills/harness/scripts/find_reference_harness.py`
  - `/Users/isanghyo/Desktop/harness/codex-harness/plugins/harness/skills/harness/scripts/scaffold_harness.py`
- 경로 문제:
  - `/Users/isanghyo/Desktop/codex-harness-100/codex-harness` -> `/Users/isanghyo/Desktop/codex-harness` (잘못된 symlink)

## 참고 사항
- `codex-harness-100`은 Git 저장소 상태가 남아 있고, 대량의 generated files 변경이 있다. `git status --short` 결과도 매우 큼.
- 현재 `git status --short`에서 `?? codex-harness`가 보이는데, 이건 실제 메타 플러그인 repo가 아니라 잘못된 symlink다.
- 공식 문서상 중요한 포인트:
  - `Skills are the authoring format.`
  - `Plugins are the installable distribution unit.`
  - local marketplace / repo marketplace 설치는 가능하다.
  - official public Plugin Directory에 self-serve publish는 아직 coming soon.
- 따라서 사용자가 말한 "GitHub에 오픈소스로 올리고 사람들이 사용할 수 있는 형태"의 현재 최선은:
  - GitHub에 plugin repo 공개
  - README에 local install / marketplace install 가이드 제공
  - `codex-harness-100`은 companion repo로 설명
