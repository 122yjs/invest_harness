# Planning

이 디렉터리는 `invest_harness` 프로젝트의 구현 계획과 마일스톤을 관리합니다. 파일 이름은 `[번호]_[상태]_[주제]` 형식을 따릅니다.

## 문서 목록

| 파일명 | 상태 | 설명 |
|---|---|---|
| [`01_archive_mvp_milestone.md`](01_archive_mvp_milestone.md) | ✅ **ARCHIVED** | 1차 MVP 마일스톤 (프레임워크 기초 및 밸류에이션 등) 완료 기록 |
| [`02_archive_evidence_layer_draft.md`](02_archive_evidence_layer_draft.md) | ✅ **ARCHIVED** | 2차 증거 레이어 구현 초안 (03번 문서에 의해 대체됨) |
| [`03_core_evidence_layer_implementation.md`](03_core_evidence_layer_implementation.md) | ✅ **90% 완료** | **현재 기준 문서**: 증거 레이어(Evidence Layer) 최종 구현 계획 |
| [`04_plan_ux_feedback_and_residuals.md`](04_plan_ux_feedback_and_residuals.md) | 🔲 **진행 예정** | **다음 계획**: 실제 리서치 UX 피드백 반영 및 03번 잔여 항목 통합 구현 계획 |
| [`05_plan_bkng_research_operational_reliability.md`](05_plan_bkng_research_operational_reliability.md) | 🔲 **진행 예정** | BKNG 실전 리서치에서 드러난 source availability, template fallback, delegation timeout, synthesis 병목 개선 계획 |

## 계보 (Lineage)

```text
01_archive (MVP)
 └─ 02_archive (Evidence Layer v1)
     └─ 03_core (Evidence Layer v2 - ACTIVE)
         └─ 04_plan (UX Refinement - NEXT)
             └─ 05_plan (BKNG Operational Reliability)
```

## 규칙

- **파일명 규칙**: `[순번]_[상태]_[주제].md` (예: `03_core_evidence_layer.md`)
- **상태 구분**:
  - `archive`: 완료되어 보존된 문서
  - `core`: 현재 진행 중인 핵심 기준 문서
  - `plan`: 다음 단계로 예정된 구체적인 계획서
- 완료된 계획은 `✅ ARCHIVED`로 상태를 변경하고 이력 보존을 위해 삭제하지 않습니다.
