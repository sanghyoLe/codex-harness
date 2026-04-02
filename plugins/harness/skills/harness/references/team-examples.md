# Team Examples

패턴은 베끼는 대상이 아니라 구조를 고르는 힌트다. 역할 이름은 도메인에 맞게 바꾸고, 범위가 작으면 팀도 줄인다.

## Example 1: Research Harness

### Pattern

- `supervisor` + `generate-critique`

### Roles

- `research-lead`
- `web-researcher`
- `source-critic`
- `synthesizer`
- `qa-reviewer`

### Suggested Outputs

- `_workspace/00_input.md`
- `_workspace/01_web_findings.md`
- `_workspace/02_source_critique.md`
- `_workspace/03_synthesis.md`
- `_workspace/04_review.md`
- `_workspace/99_final.md`

### Why This Shape Works

- 탐색과 비판적 검토를 분리한다
- synthesis 전에 source quality를 따로 검증할 수 있다
- broad research에서도 오케스트레이터가 라우팅을 통제할 수 있다

## Example 2: Fullstack Web App Harness

### Pattern

- `pipeline` with selective parallelism

### Roles

- `architect`
- `frontend-dev`
- `backend-dev`
- `qa-engineer`
- `release-reviewer`

### Suggested Flow

1. `architect`가 요구사항과 구조를 정리한다
2. `frontend-dev`와 `backend-dev`가 병렬로 구현한다
3. `qa-engineer`가 통합 정합성을 점검한다
4. `release-reviewer`가 최종 리스크를 정리한다

### Good Fit Signals

- UI와 API를 동시에 진행할 수 있다
- 중간 설계 문서가 품질에 중요하다
- QA가 단순 존재 확인이 아니라 interface mismatch를 잡아야 한다

## Example 3: YouTube Content Harness

### Pattern

- `pipeline` + `fan-out`

### Roles

- `content-strategist`
- `scriptwriter`
- `thumbnail-designer`
- `seo-optimizer`
- `production-reviewer`

### Suggested Outputs

- `_workspace/01_content_angle.md`
- `_workspace/02_script.md`
- `_workspace/03_thumbnail_briefs.md`
- `_workspace/04_seo_package.md`
- `_workspace/05_review.md`

### Key Point

스크립트와 썸네일은 분리하되, 둘 다 content angle 문서를 공통 입력으로 쓰게 하면 톤이 덜 흔들린다.

## Example 4: Code Review Harness

### Pattern

- `fan-out/fan-in`

### Roles

- `architecture-reviewer`
- `security-analyst`
- `performance-analyst`
- `style-inspector`
- `review-synthesizer`

### Suggested Outputs

- `_workspace/01_architecture_review.md`
- `_workspace/02_security_review.md`
- `_workspace/03_performance_review.md`
- `_workspace/04_style_review.md`
- `_workspace/05_summary.md`

### Key Point

이 패턴은 병렬 분석 자체보다 마지막 `review-synthesizer`의 기준이 더 중요하다. severity 기준과 merge 방식을 반드시 써야 한다.

## Example 5: API Documentation Harness

### Pattern

- `pipeline` + `generate-critique`

### Roles

- `api-analyst`
- `example-writer`
- `reference-editor`
- `docs-reviewer`

### Why This Shape Works

- API 사실 추출과 설명 문장 작성의 성격이 다르다
- example-writer를 분리하면 샘플 코드 품질이 올라간다
- docs-reviewer가 누락된 엔드포인트와 모순 표현을 잡을 수 있다

## Example 6: Marketing Campaign Harness

### Pattern

- `supervisor` or `generate-critique`

### Roles

- `market-researcher`
- `copywriter`
- `creative-strategist`
- `experiment-planner`
- `campaign-reviewer`

### Good Fit Signals

- 메시지, 비주얼, 실험 계획이 분리되어야 한다
- 그러나 팀이 너무 커지면 오히려 톤이 분산된다
- 작은 캠페인이면 `copywriter + reviewer` 두 역할만으로 축소해도 된다

## Example 7: Migration Harness

### Pattern

- `hierarchical-delegation` or `supervisor`

### Roles

- `migration-lead`
- `schema-owner`
- `application-updater`
- `test-keeper`
- `risk-reviewer`

### Key Point

마이그레이션 하네스는 구현 자체보다 영향 범위 추적과 rollback/risk 문서화가 중요하다. `_workspace/impact-map.md` 같은 중간 산출물을 두는 편이 좋다.

## 축소 규칙

다음 경우에는 위 예시보다 더 작게 만든다:

- 산출물이 1개뿐인 경우
- 역할 둘이 사실상 같은 문서를 보고 같은 판단을 하는 경우
- 작은 저장소에 과한 QA/리뷰 단계를 붙이려는 경우

하네스가 좋아지려면 "역할 수 증가"가 아니라 "역할 간 경계 명확화"가 먼저다.
