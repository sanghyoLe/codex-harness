# Skill Testing Guide

생성된 하네스를 완성으로 간주하기 전에 최소한 트리거, 파일 정합성, dry run, reviewer coverage를 점검한다.

## 1. Trigger Test

오케스트레이터 description이 실제 사용자 표현을 받는지 본다.

예시:

- `하네스 구성해줘`
- `이 저장소에 맞는 연구 하네스 설계해줘`
- `코드 리뷰용 에이전트 팀 만들어줘`
- `기존 하네스를 QA 중심으로 재구성해줘`

실패 신호:

- description이 너무 추상적이라 특정 도메인을 못 잡는다
- narrow request도 항상 full harness로 오해한다

## 2. File Consistency Test

다음을 점검한다:

- 각 `config_file`이 실제 파일을 가리키는가
- 각 `model_instructions_file`이 실제 `.md`를 가리키는가
- 각 스킬에 valid frontmatter가 있는가
- `[TODO]`나 placeholder가 남아 있지 않은가

권장 검사:

```bash
rg -n "config_file|model_instructions_file|^---$|\\[TODO\\]" AGENTS.md .agents .codex
```

## 3. Dry Run Test

최소 세 가지를 가정해서 mentally simulate한다.

### Scenario A: Full Request

- 전체 하네스를 돌려야 하는 요청
- 기대: 역할 대부분이 활성화되고 통합 산출물이 나온다

### Scenario B: Narrow Request

- 특정 영역만 필요한 요청
- 기대: 오케스트레이터가 일부 역할만 활성화한다

### Scenario C: Existing Harness Present

- 이미 `AGENTS.md`와 `.codex`가 존재하는 저장소
- 기대: 전면 재생성이 아니라 수정/보강 모드로 동작한다

## 4. With-Harness vs Without-Harness Check

이 질문에 답한다:

- 하네스가 작업 분해를 개선하는가
- 역할 전문성이 실제로 결과 차이를 만드는가
- 검수 구조가 품질을 높이는가

셋 다 "아니오"에 가까우면 하네스는 과설계거나 잘못 분리된 것이다.

## 5. Reviewer Coverage Test

reviewer가 있다면 반드시 확인한다:

- 무엇을 체크하는가
- 무엇이 revision trigger인가
- 얼마나 재작업을 허용하는가
- producer와 충돌 시 어떤 기준으로 결정하는가

reviewer가 generic praise만 하게 설계되면 없는 편이 낫다.

## 6. Workspace Contract Test

`_workspace/`를 쓰는 하네스라면:

- 입력 파일이 정의되어 있는가
- 역할별 출력 경로가 충돌하지 않는가
- 최종 산출물과 중간 산출물이 구분되는가

좋은 기본 구조:

- `_workspace/00_input.md`
- `_workspace/01_plan.md`
- `_workspace/{phase}_{role}_{artifact}.md`
- `_workspace/99_final.md`

## 7. Regression Test After Edits

하네스를 수정했다면 수정 전보다 최소 하나는 좋아져야 한다:

- 더 나은 trigger coverage
- 더 적은 역할 중복
- 더 명확한 output contract
- 더 강한 reviewer rubric

변화가 없다면 수정은 noise일 가능성이 높다.
