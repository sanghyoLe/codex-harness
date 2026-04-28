# Team Examples

패턴은 베끼는 대상이 아니라 구조를 고르는 힌트다. 역할 이름, 출력 경로, 검증 기준은 대상 저장소에 맞게 바꾼다.

## Example 1: Research Harness

### Pattern

Fan-out / fan-in

### Roles

| Role | Responsibility | Output |
|------|----------------|--------|
| official-researcher | 공식 문서, 회사/기관 발표, 원문 자료 | `_workspace/01_official.md` |
| media-researcher | 뉴스, 인터뷰, 투자/시장 자료 | `_workspace/02_media.md` |
| community-researcher | 커뮤니티 반응, 사용자 피드백 | `_workspace/03_community.md` |
| source-critic | 출처 신뢰도와 상충 정보 검토 | `_workspace/04_source_critique.md` |
| synthesizer | 최종 보고서 통합 | `_workspace/99_final.md` |

### Why This Shape Works

- 수집 관점과 비판적 검토를 분리한다.
- 출처 품질 검증이 synthesis 전에 일어난다.
- 상충 정보는 삭제하지 않고 출처와 함께 병기한다.

## Example 2: Fullstack Web App Harness

### Pattern

Pipeline with selective parallelism

### Roles

| Role | Responsibility | Output |
|------|----------------|--------|
| product-analyst | 요구사항, acceptance criteria | `_workspace/01_requirements.md` |
| architect | 앱 구조, 데이터 흐름, API 계약 | `_workspace/02_architecture.md` |
| frontend-builder | UI와 클라이언트 상태 | `_workspace/03_frontend.md` |
| backend-builder | API, 데이터 모델, 서버 로직 | `_workspace/04_backend.md` |
| qa-engineer | 통합 정합성, 테스트, 회귀 리스크 | `_workspace/05_qa.md` |

### Flow

1. product-analyst와 architect가 순차로 범위를 고정한다.
2. frontend-builder와 backend-builder는 API 계약이 정리된 뒤 병렬로 작업한다.
3. qa-engineer는 UI/API shape, 테스트, 문서 정합성을 교차 검증한다.
4. 오케스트레이터가 최종 변경 요약과 남은 리스크를 통합한다.

## Example 3: Code Review Harness

### Pattern

Fan-out / fan-in + reviewer synthesis

### Roles

| Role | Responsibility | Output |
|------|----------------|--------|
| architecture-reviewer | 모듈 경계, coupling, 확장성 | `_workspace/01_architecture_review.md` |
| security-reviewer | 인증/인가, 입력 검증, 비밀 노출 | `_workspace/02_security_review.md` |
| performance-reviewer | 쿼리, 렌더링, 캐시, 병목 | `_workspace/03_performance_review.md` |
| test-reviewer | 테스트 누락, 깨지기 쉬운 검증 | `_workspace/04_test_review.md` |
| review-synthesizer | severity 기준으로 최종 보고서 통합 | `_workspace/99_review.md` |

### Key Point

병렬 분석보다 마지막 synthesis 기준이 더 중요하다. `critical`, `high`, `medium`, `low`의 기준과 중복 findings 병합 규칙을 반드시 쓴다.

## Example 4: Content Production Harness

### Pattern

Pipeline + producer-reviewer

### Roles

| Role | Responsibility | Output |
|------|----------------|--------|
| strategist | audience, angle, channel fit | `_workspace/01_strategy.md` |
| writer | script, copy, narrative draft | `_workspace/02_draft.md` |
| visual-planner | thumbnail, storyboard, asset brief | `_workspace/03_visual_brief.md` |
| seo-optimizer | title, tags, search intent | `_workspace/04_seo.md` |
| content-reviewer | tone, factuality, conversion intent | `_workspace/05_review.md` |

### Key Point

전략 문서를 공통 입력으로 쓰게 하면 writer, visual-planner, seo-optimizer의 톤이 덜 흔들린다.

## Example 5: API Documentation Harness

### Pattern

Pipeline + QA gate

### Roles

| Role | Responsibility | Output |
|------|----------------|--------|
| api-analyst | endpoint, schema, auth 추출 | `_workspace/01_api_inventory.md` |
| example-writer | curl/SDK 예시 작성 | `_workspace/02_examples.md` |
| reference-editor | 문서 문장과 구조 정리 | `_workspace/03_reference.md` |
| docs-reviewer | 누락 endpoint, 예시 실행 가능성 검토 | `_workspace/04_docs_review.md` |

### Why This Shape Works

- API 사실 추출과 설명 문장 작성은 성격이 다르다.
- example-writer를 분리하면 샘플 코드 품질이 올라간다.
- docs-reviewer가 문서와 실제 구현의 불일치를 잡을 수 있다.

## Example 6: Migration Harness

### Pattern

Supervisor or hierarchical delegation

### Roles

| Role | Responsibility | Output |
|------|----------------|--------|
| migration-lead | 범위 분해, 배치 순서, rollback 전략 | `_workspace/01_migration_plan.md` |
| schema-owner | DB/schema 영향 | `_workspace/02_schema.md` |
| app-updater | 애플리케이션 코드 변경 | `_workspace/03_app_changes.md` |
| test-keeper | 테스트 갱신과 회귀 검증 | `_workspace/04_tests.md` |
| risk-reviewer | 출시 리스크, rollback checklist | `_workspace/05_risk.md` |

### Key Point

마이그레이션은 구현 자체보다 영향 범위 추적과 rollback/risk 문서화가 중요하다. `_workspace/impact-map.md` 같은 중간 산출물을 두는 편이 좋다.

## 산출물 패턴 요약

- 에이전트 정의: `.codex/agents/{agent-name}.toml`
- 오케스트레이터 스킬: `.agents/skills/{orchestrator}/SKILL.md`
- supporting skill: `.agents/skills/{skill-name}/SKILL.md`
- 작업 산출물: `_workspace/*`
- 저장소 포인터: `AGENTS.md`

## 축소 규칙

다음 경우에는 위 예시보다 더 작게 만든다:

- 산출물이 1개뿐이다.
- 역할 둘이 사실상 같은 문서를 보고 같은 판단을 한다.
- 작은 저장소에 과한 QA/리뷰 단계를 붙이려는 경우.
- 사용자가 좁은 수정만 요청했는데 전체 하네스 실행이 필요하지 않은 경우.
