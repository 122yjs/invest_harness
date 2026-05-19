---
name: source-router
description: evidence-plan을 읽고 source capability 기반 source-call-plan, validation, unresolved gaps를 작성하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/source-router/SKILL.md; kind=skill; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


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
- Rank selected sources by evidence trust tier before availability convenience: T0 company official/regulator disclosure, T1 official market/statistical sources, T2 vendor snapshots, T3 discovery/context.
- For reported company facts, financial statements, guidance, segment data, risk factors, share count, and issuer identity, select Company IR, SEC EDGAR, DART/KRX, or local regulator filings before yfinance/FMP/Alpha Vantage/Web Search.
- Runtime availability can force a fallback, but it cannot promote T2/T3 evidence above T0 for material company claims. If T0 is unavailable, stale, or not fetchable, record the data gap before using lower-tier evidence.
- Treat FRED, Alpha Vantage, FMP, EDGAR, DART-KRX, yfinance, KOSIS, customs trade, Google Trends, Naver DataLab, KOTRA, G2B, and ECOS as capabilities, not mandatory sources.
- Read each registry source's `connection_status` as repo-evidence status only, not live runtime proof.
- Before analyst fan-out, record live runtime proof separately as `Runtime Availability` and `Live Tool Probe` in `${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md`.
- If `yfinance` is documented in repo contracts but unavailable in the live tool inventory, do not block the run. Mark it unavailable, prefer T0 company IR, SEC EDGAR, DART/KRX, or local regulator filings for reported company facts, then select FMP/Alpha Vantage only when actually callable. Use Web Search + Fetch for source discovery and source retrieval support.
- Valid `connection_status` values are `connected`, `documented_only`, `planned`, and `external_manual`.
- If a needed source is `documented_only`, `planned`, or `external_manual`, record the missing callable tool/endpoint in `${ACTIVE_WORKSPACE}/00_evidence/unresolved-data-gaps.md` instead of inventing a retrieval path.
- Reuse existing yfinance and DART-KRX/korea-stock tool contracts when applicable; represent FRED, SEC EDGAR, Alpha Vantage, and FMP as source capability contracts unless concrete callable repo evidence exists.
- For public web evidence, use Web Search only to discover candidate URLs. If search returns only summary snippets, require Web Fetch/browser/PDF reading of the candidate URL body before using the source as evidence.
- Search finds links; Fetch reads the article, document, or PDF body. Do not cite or validate claims from search snippets alone.
- Web Search + Web Fetch does not require a separate scraping infrastructure for ordinary public articles, documents, or PDFs, but body retrieval failures must be recorded as data gaps.
- Keep API execution outside this thin planning contract unless another skill explicitly owns retrieval.

## Workflow

1. Read evidence plan requirements.
2. For each evidence type, select candidate source, trust tier, `source_id`, `connection_status`, runtime availability, live tool probe evidence, reason selected, required parameters, fallback sources, expected output, validation checks, and source limitations.
3. Write claim boundaries for each source.
4. If required inputs are missing, write unresolved data gaps.
5. If the selected source is not `connected`, or is `connected` in repo evidence but unavailable in the live runtime, write the unavailable tool/endpoint and fallback path as a data gap before analyst fan-out.
6. If a lower-trust source is used because T0/T1 evidence is unavailable, write the missing higher-trust evidence and affected claim in unresolved data gaps.
7. For web sources, include both the search query/link-discovery step and the fetch/body-read step in the source-call plan.
8. If retrieval was performed by another role, summarize evidence IDs, fetched URL/body status, and validation status.
9. Write outputs under `${ACTIVE_WORKSPACE}/00_evidence/`.

## Prohibited

- Do not store API keys.
- Do not implement API clients or databases.
- Do not average conflicting sources without explaining the conflict.
- Do not treat relative search interest as sales or market size.
- Do not treat customs trade as company revenue.
- Do not treat public procurement as total market demand.
