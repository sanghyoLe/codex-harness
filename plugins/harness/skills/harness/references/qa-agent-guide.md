# QA Agent Guide

QA나 reviewer 역할은 "있는 것이 좋아 보이기 때문"이 아니라, 실제로 경계면 오류와 품질 저하를 잡아낼 수 있을 때만 넣는다.

## 1. QA가 특히 필요한 경우

- 여러 산출물이 서로 정합해야 한다
- 생성 결과와 구현 결과를 교차 검증해야 한다
- 코드 변경의 회귀 리스크가 크다
- API, UI, 문서, 테스트가 함께 움직인다

## 2. QA가 약해지는 전형적 패턴

- 존재 확인만 하고 연결 정합성을 보지 않는다
- "looks good" 같은 모호한 리뷰를 한다
- 수정 기준과 재검수 기준이 없다
- producer와 같은 관점으로만 결과를 읽는다

## 3. 경계면 검증 우선

강한 QA는 개별 조각보다 경계면을 본다.

예:

- API 응답 shape ↔ 프론트 타입 기대
- 링크 경로 ↔ 실제 페이지 경로
- 상태 전이 설계 ↔ 실제 코드 분기
- 문서 설명 ↔ 실제 구현 동작
- 테스트 케이스 ↔ 실제 acceptance criteria

## 4. QA 역할에 넣어야 할 것

- 핵심 검증 영역
- severity 기준
- required fix / optional fix 구분
- 재검수 조건
- 최종 보고 포맷

## 5. 좋은 QA 출력 형식

```markdown
# QA Review

## Critical Findings
## Medium-Risk Findings
## Consistency Gaps
## Required Revisions
## Optional Improvements
## Verified Areas
```

좋은 보고서는 발견 사항을 severity 순으로 쓰고, 수정 필요 여부를 분명히 구분한다.

## 6. 코드 하네스에서의 QA 체크 예시

- 인터페이스 mismatch
- 누락된 error handling
- edge case 미처리
- 테스트 부재
- 문서와 구현 불일치

## 7. 콘텐츠 하네스에서의 QA 체크 예시

- 톤 일관성
- 사실성
- audience fit
- conversion intent 정합성
- visual brief와 script 간 충돌

## 8. QA를 넣지 말아야 하는 경우

- 산출물이 작고 단순하다
- 오케스트레이터가 직접 검수해도 충분하다
- review 기준을 명시할 수 없다

이 경우에는 오케스트레이터 validation 섹션을 강화하는 편이 낫다.
