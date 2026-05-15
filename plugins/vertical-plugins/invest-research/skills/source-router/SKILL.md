---
name: source-router
description: evidence-plan을 읽고 source capability 기반 source-call-plan, validation, unresolved gaps를 작성하는 스킬
---

# source-router

## When to Use

- `${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md`가 존재하고, source capability에 맞춘 후보 소스와 fallback을 정해야 할 때 사용한다.
- `/market-intel` 또는 `/source-audit` thin command가 source routing 또는 audit handoff를 요청할 때 사용한다.

## Required Inputs

- `${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md`
- 기준 문서: `docs/harness/invest/research-layer/source-capability-registry.md`
- 기준 문서: `docs/harness/invest/research-layer/validation-gates.md`
- 기준 문서: `docs/harness/invest/research-layer/claim-boundary-policy.md`
- 템플릿: `docs/harness/invest/templates/source-call-plan.md`
- 템플릿: `docs/harness/invest/templates/source-validation.md`
- 템플릿: `docs/harness/invest/templates/unresolved-data-gaps.md`

## Output Paths

- `${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md`
- `${ACTIVE_WORKSPACE}/00_evidence/source-validation.md`
- `${ACTIVE_WORKSPACE}/00_evidence/unresolved-data-gaps.md`
- 선택 출력: `${ACTIVE_WORKSPACE}/00_evidence/api-call-log.md`

## Rules

- Select sources by `required_evidence_types` and source capability.
- Do not select sources by fixed use-case labels.
- Include fallback sources and source limitations.
- Include validation checks before analyst fan-out.
- Treat FRED, Alpha Vantage, FMP, EDGAR, DART-KRX, yfinance, KOSIS, customs trade, Google Trends, Naver DataLab, KOTRA, G2B, and ECOS as capabilities, not mandatory sources.
- Read each registry source's `connection_status` as repo-evidence status only, not live runtime proof.
- Valid `connection_status` values are `connected`, `documented_only`, `planned`, and `external_manual`.
- If a needed source is `documented_only`, `planned`, or `external_manual`, record the missing callable tool/endpoint in `${ACTIVE_WORKSPACE}/00_evidence/unresolved-data-gaps.md` instead of inventing a retrieval path.
- Reuse existing yfinance and DART-KRX/korea-stock tool contracts when applicable; represent FRED, SEC EDGAR, and Alpha Vantage as source capability contracts unless concrete callable repo evidence exists.
- Keep API execution outside this thin planning contract unless another skill explicitly owns retrieval.

## Workflow

1. Read evidence plan requirements.
2. For each evidence type, select candidate source, `source_id`, `connection_status`, reason selected, required parameters, fallback sources, expected output, validation checks, and source limitations.
3. Write claim boundaries for each source.
4. If required inputs are missing, write unresolved data gaps.
5. If the selected source is not `connected`, write the unavailable tool/endpoint and fallback path as a data gap before analyst fan-out.
6. If retrieval was performed by another role, summarize evidence IDs and validation status.
7. Write outputs under `${ACTIVE_WORKSPACE}/00_evidence/`.

## Prohibited

- Do not store API keys.
- Do not implement API clients or databases.
- Do not average conflicting sources without explaining the conflict.
- Do not treat relative search interest as sales or market size.
- Do not treat customs trade as company revenue.
- Do not treat public procurement as total market demand.
