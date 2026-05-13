Do this as a minimal, reviewable documentation-and-contract PR. Prefer adding contracts, templates, and tests over implementing runtime API clients. Avoid broad rewrites.

You are working in the GitHub repository:

https://github.com/122yjs/invest_harness

Goal:
Implement a generic Evidence Planning / Source Routing / Signal Primitive layer for the existing invest_harness.

This repository is a Markdown-first AI agent harness for investment research. Preserve the existing fan-out/fan-in analyst workflow. Do NOT rewrite the whole harness. Add a generic evidence layer before the current analyst fan-out.

Read these first:
- AGENTS.md
- README.md
- docs/harness/invest/runbook.md
- docs/harness/invest/team-spec.md
- docs/harness/invest/data-source-policy.md if present
- docs/harness/invest/mcp-routing.md if present
- docs/harness/invest/templates/
- scripts/verify_invest_harness.py
- scripts/test_harness_structure.py

Core design principle:
This is a GENERAL-PURPOSE investment harness.
Do NOT hard-code product/use-case categories such as cosmetics, pet supplies, semiconductors, power equipment, defense, K-food, etc. as router categories or allowed product enums.

Known use cases are examples only. They must be placed under evals/golden-scenarios or examples, not in the core router.

The core must be based on:
1. Open-ended question decomposition
2. Source capability registry
3. Evidence types
4. Signal primitives
5. Validation gates
6. Evidence ledger
7. Claim-boundary policy

The planner must decompose the user's request into subjects / entities / geographies / time horizon / investment claim types / required evidence types.
It must not classify the request into a fixed use_case name.

Use this schema direction:

question_decomposition:
  raw_request: string

  entities:
    companies:
      - surface_form: string
        ticker: null
        market: null
        canonical_id: null
        confidence: null
    peer_groups:
      - surface_form: string
        members: []
        confidence: null

  subjects:
    - surface_form: string
      description: string
      object_type_guess:
        - product
        - service
        - technology
        - theme
        - sector
        - commodity
        - regulation
        - macro_indicator
        - supply_chain_node
        - customer_segment
        - geography_market
        - unknown
      ontology_tags: []
      industry_classification:
        primary: null
        secondary: []
        systems:
          gics: []
          ksic: []
          sic: []
          naics: []
      candidate_source_identifiers:
        hs_codes: []
        kosis_categories: []
        naver_categories: []
        google_trends_queries: []
        kotra_keywords: []
        dart_business_segments: []
      requires_ontology_resolution: true
      mapping_confidence: null

  geographies:
    - surface_form: string
      country_or_region_code: null
      geo_type:
        - country
        - region
        - city
        - economic_bloc
        - sales_region
        - unknown

  time_horizon:
    surface_form: string
    bucket:
      - short_term
      - medium_term
      - long_term
      - unknown
    start_date: null
    end_date: null
    frequency_guess:
      - daily
      - weekly
      - monthly
      - quarterly
      - annual
      - unknown

  investment_claim_types:
    - demand_growth
    - export_momentum
    - valuation_gap
    - earnings_revision
    - regulatory_risk
    - procurement_tailwind
    - margin_change
    - supply_chain_shift
    - consumer_interest
    - competitive_position
    - macro_sensitivity
    - price_momentum
    - balance_sheet_risk
    - unknown

  required_evidence_types:
    - evidence_type:
        - company_disclosure
        - market_transaction
        - search_interest
        - export_import
        - market_context
        - macro_policy
        - price_valuation
        - procurement
        - regulatory
        - supply_chain
        - news_event
        - alternative_data
      reason: string
      priority:
        - required
        - optional
        - validation_only
      source_capabilities_needed: []
      validation_gates: []

Important:
- subjects must be open-ended extracted objects from the user request.
- ontology_tags and industry_classification are mapping aids only.
- candidate_source_identifiers are optional candidates, not forced categories.
- If mapping is uncertain, preserve surface_form and mark mapping_confidence low.
- Do not force unknown concepts into nearest known examples.

Implement the following changes.

Phase 1: Documentation layer
Create this directory if missing:

docs/harness/invest/research-layer/

Add these files:

1. docs/harness/invest/research-layer/overview.md
Explain the new evidence layer:
User Request
→ Input Gate
→ Question Decomposition
→ Evidence Planner
→ Source Capability Router
→ Evidence Ledger
→ Signal Primitives
→ Validation Gate
→ Existing Analyst Fan-out
→ Draft
→ QA
→ Final

Make clear that this layer precedes existing analyst roles and does not replace them.

2. docs/harness/invest/research-layer/question-decomposition.md
Define the open-ended question decomposition schema.
Use subjects, not product_classification as the core.
Explicitly forbid fixed product taxonomy and use-case hard routing.

Add this policy:
- no_fixed_product_taxonomy: true
- no_use_case_hard_routing: true
- preserve_user_surface_terms: true
- allow_unseen_market_objects: true
- use_ontology_for_candidate_mapping_only: true
- source_selection_based_on_evidence_need: true
- signal_selection_based_on_claim_type_and_evidence_type: true

3. docs/harness/invest/research-layer/source-capability-registry.md
Define source capability contracts.
Include at least these sources as contracts, but keep them generic:
- opendart / DART-KRX
- yfinance
- kosis
- customs_trade_api
- google_trends
- naver_datalab
- kotra
- g2b_procurement
- ecos or macro official statistics

For each source define:
- provides
- good_for
- not_good_for
- required_inputs
- outputs
- validation_rules
- forbidden_claims

Examples:
Google Trends:
- provides relative_search_interest, regional_interest, related_queries, rising_queries
- not_good_for absolute_market_size, sales_estimation_alone
- required validation: report geo, timeframe, query/topic, relative index caveat

Customs trade:
- provides item/country export-import value, weight, HS code dimensions
- not_good_for company_specific_sales or local country total market size
- required validation: HS code mapping, latest month, FOB/CIF basis if relevant, base effect check

KOSIS:
- provides official statistics, long time series, transaction/market baseline
- not_good_for real-time granular SKU demand
- required validation: table id, unit, period, update date if available

4. docs/harness/invest/research-layer/signal-primitives.md
Define reusable signal primitives.
Do not define product-specific use cases as primitives.

Include:
- search_interest_momentum
- export_momentum
- transaction_market_size
- procurement_demand
- disclosure_exposure
- market_context_signal
- regulatory_risk_signal
- valuation_anchor
- macro_regime_signal
- news_event_signal

For each primitive define:
- purpose
- required_inputs
- compatible_sources
- common_metrics
- output fields
- caveats
- claim boundaries

5. docs/harness/invest/research-layer/validation-gates.md
Define validation gates by evidence/source type:
- relative_index_gate
- official_statistics_gate
- trade_data_gate
- company_disclosure_gate
- procurement_gate
- market_context_gate
- valuation_gate
- source_conflict_gate

Include specific prohibitions:
- Do not infer sales from Google Trends alone.
- Do not infer market size from relative search interest.
- Do not infer company-specific revenue from customs trade data alone.
- Do not treat KOTRA text/news as export volume.
- Do not treat public procurement as total market demand.
- Do not average conflicting sources without explaining the conflict.

6. docs/harness/invest/research-layer/claim-boundary-policy.md
Define what the harness may and may not claim.
Structure:
- claim
- required evidence
- allowed wording
- forbidden wording
- required caveats

Examples:
Consumer interest claim:
requires search_interest evidence.
Cannot claim sales growth unless transaction/export/company evidence also supports it.

Export momentum claim:
requires export_import evidence.
Cannot claim company revenue growth unless company_disclosure or segment exposure evidence supports it.

7. docs/harness/invest/research-layer/ontology.md
Define ontology as candidate mapping only.
It must not be a fixed taxonomy.

It should map free-text subjects to candidate identifiers:
- aliases
- HS codes
- KOSIS categories
- Naver categories
- Google Trends queries
- KOTRA keywords
- DART business segment terms
- GICS/KSIC/SIC/NAICS codes

Add:
unknown_concept_behavior:
  - keep_surface_form
  - generate_search_terms
  - mark_low_confidence_mapping
  - do_not_force_to_existing_category
  - proceed_with_best_effort_evidence_plan

Phase 2: Templates
Add templates under docs/harness/invest/templates/:

1. evidence-plan.md
Must include:
- raw request
- question decomposition
- required evidence types
- source capability needs
- signal primitives needed
- validation gates
- unresolved ambiguities

2. source-call-plan.md
Must include:
- evidence type
- candidate source
- reason selected
- required parameters
- fallback sources
- expected output
- validation checks
- source limitations

3. evidence-ledger.md
Must include a table:
Evidence ID | Source | Source Type | Retrieved At | Period | Metric | Value | Unit | Transformation | Used By | Claim Boundary | Caveat

4. signal-card.md
Must include:
- signal id
- signal primitive
- subject
- geography
- period
- inputs
- calculations
- output signal
- confidence
- caveats
- downstream analyst usage

5. source-validation.md
Must include:
- validation status
- missing data
- unit/date checks
- source conflicts
- relative vs absolute checks
- forbidden claim checks
- unresolved data gaps

6. api-call-log.md
Even if APIs are not implemented yet, define a log template:
- source
- endpoint/tool
- parameters
- timestamp
- success/failure
- response summary
- cache path if any
- error if any

Phase 3: Workspace/runbook integration
Update docs/harness/invest/runbook.md and docs/harness/invest/team-spec.md so the workflow becomes:

0. Input gate
1. Input summary
2. Evidence planning
3. Source call planning
4. Evidence ledger + signal cards
5. Validation gates
6. Existing analyst fan-out
7. Draft synthesis
8. QA + source/claim audit
9. Final report

Add a new workspace section:

${ACTIVE_WORKSPACE}/00_evidence/
  question-decomposition.md
  evidence-plan.md
  source-call-plan.md
  evidence-ledger.md
  signal-cards.md
  source-validation.md
  api-call-log.md
  unresolved-data-gaps.md

Do not remove the existing:
00_input/
01_financial/
02_fundamental/
03_valuation/
04_technical/
05_macro_sentiment/
06_risk_scenario/
07_draft/
09_qa/
08_final/

Existing analyst outputs must remain compatible.

Phase 4: Skills / agent instructions
Inspect current skill structure first.
If this repo has canonical source files that generate .agents/skills, edit the canonical source and run the sync script.
If .agents/skills are canonical in this repo, update them directly.
Do not make assumptions; inspect the repo conventions first.

Add or update skills as appropriate:

1. evidence-planner
Purpose:
- Parse user request into open-ended question decomposition.
- Produce 00_evidence/question-decomposition.md and 00_evidence/evidence-plan.md.
- Must not output use_case: cosmetics_sea_export or use_case: pet_ecommerce_trend as core routing.
- Must output required_evidence_types and signal_primitives_needed.

2. source-router
Purpose:
- Read evidence-plan.md.
- Select sources by capability, not by fixed use-case.
- Produce source-call-plan.md.
- Explain why each source is selected.
- Include fallback sources and limitations.

3. Optional signal-analyst
If lightweight to add:
- Read evidence-ledger.md.
- Produce signal-cards.md.
- Use signal primitives, not product use-cases.

4. Update invest-orchestrator
- It must create / require 00_evidence before analyst fan-out when the user request needs external evidence beyond ordinary company financials.
- It must pass evidence-ledger and signal-cards to analysts.
- It must preserve existing input gate behavior.

5. Update qa-reviewer
- It must check source/claim consistency.
- It must verify that Google Trends, Naver DataLab, KOTRA, KOSIS, customs, procurement, and DART evidence are not overclaimed.
- It must check that final reports do not use relative search interest as market size or sales.

Phase 5: Commands
If the repo has command stubs or command runtime, add thin commands only.
Do not implement heavy API execution in command stubs.

Add, if consistent with existing command style:
- evidence.md
- market-intel.md
- source-audit.md

/evidence should dispatch to evidence-planner.
/market-intel should dispatch to evidence-planner + source-router + optional signal-analyst.
/source-audit should dispatch to qa-reviewer or data/source audit logic.

Keep command runtime thin. It should parse/dispatch and write handoff metadata, not perform full analysis itself.

Phase 6: Evals / golden scenarios
Create:

docs/harness/invest/evals/golden-scenarios/

Add example scenarios only as eval fixtures, not router categories:

1. pet-ecommerce-trend.md
Purpose:
Verify the planner decomposes a domestic pet e-commerce trend question into:
- subjects from surface form
- search_interest
- market_transaction
- optional pet population/admin proxy
- validation that search index is not market size

2. cosmetics-sea-export.md
Purpose:
Verify the planner decomposes a K-beauty Southeast Asia question into:
- search_interest
- export_import
- market_context
- company_disclosure
- no fixed use_case routing

3. unseen-market-object.md
Use this input:
"인도네시아 니켈 수출 제한이 한국 배터리 소재주에 미치는 영향 분석해줘."
Expected decomposition:
- subjects: 니켈, 수출 제한, 한국 배터리 소재주
- geographies: Indonesia, Korea
- evidence types: regulatory, supply_chain, export_import, company_disclosure, price_valuation
- no forced mapping to cosmetics/pet/power/etc.

4. google-trends-claim-boundary.md
Verify that Google Trends is treated as relative search interest only.

Phase 7: Tests
Add Python tests if the repo already uses Python verification scripts.
Do not require PowerShell for Linux/macOS validation.

Add or extend tests under scripts/:

1. test_evidence_layer_structure.py
Check required docs/templates/evals exist.

2. test_no_fixed_product_taxonomy.py
Fail if core research-layer docs define fixed allowed products/use-case categories such as:
- cosmetics
- pet_supplies
- semiconductors
- power_equipment
- defense
- k_food
as required router enum values.
Allow these words only in evals/golden-scenarios or clearly marked examples.

3. test_signal_primitives.py
Check signal-primitives.md includes generic primitives and required sections.

4. test_source_capability_registry.py
Check each source contract has provides/good_for/not_good_for/validation_rules/forbidden_claims.

5. test_claim_boundary_policy.py
Check claim-boundary-policy.md includes prohibitions:
- Google Trends is not market size.
- Search interest is not sales.
- Customs trade is not company revenue.
- KOTRA text is not export volume.

6. test_workspace_evidence_contracts.py
Check templates for 00_evidence outputs exist and contain required headings/fields.

Update scripts/verify_invest_harness.py to include these tests.
Preserve existing tests.

Phase 8: README / AGENTS updates
Update README.md and AGENTS.md lightly:
- Mention the new evidence layer.
- Mention 00_evidence workspace.
- Mention that source selection is capability-based.
- Mention that use-case examples are non-exhaustive eval fixtures, not core router categories.
- Preserve the existing investment-disclaimer language.

Do not over-expand README. Link to research-layer docs instead.

Non-goals:
- Do not implement real API clients yet.
- Do not store API keys.
- Do not build a database.
- Do not create a hardcoded use-case classifier.
- Do not replace existing analyst skills.
- Do not force all research through Google Trends/KOSIS/Customs.
- Do not infer investment recommendations from a single alternative-data signal.

Acceptance criteria:
1. Existing verification still passes.
2. New verification tests pass with:
   python3 scripts/verify_invest_harness.py
3. Existing workspace structure remains backward-compatible.
4. New 00_evidence structure is documented and templated.
5. Core planner docs use open-ended subjects, not fixed product categories.
6. Source routing is based on evidence type and source capability.
7. Golden scenarios are located under evals/examples only.
8. QA policy includes claim-boundary checks.
9. No source claims market size/sales/revenue beyond its evidence boundary.
10. The implementation is Markdown-first and consistent with the existing harness style.

After implementing:
- Show a concise summary of changed files.
- Explain how the new flow works in 5-8 bullets.
- Show the validation command output.
- If any test cannot be run, explain why and what remains unverified.