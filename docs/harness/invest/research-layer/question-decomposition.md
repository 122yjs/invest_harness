# Question Decomposition Contract

The evidence layer decomposes the user's request into open-ended research objects.
`subjects` are the core unit. The core router must not use `product_classification`
or fixed use-case routing as the primary decision point.

## Policy

```yaml
no_fixed_product_taxonomy: true
no_use_case_hard_routing: true
preserve_user_surface_terms: true
allow_unseen_market_objects: true
use_ontology_for_candidate_mapping_only: true
source_selection_based_on_evidence_need: true
signal_selection_based_on_claim_type_and_evidence_type: true
```

## Schema

```yaml
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
```

## Constraints

- `subjects` are open-ended objects extracted from the user request.
- `ontology_tags` and `industry_classification` are mapping aids only.
- `candidate_source_identifiers` are optional candidates, not forced categories.
- If mapping is uncertain, preserve `surface_form` and mark `mapping_confidence` low.
- Unknown concepts must not be forced into the nearest known example.
- Source selection is based on evidence need, not on a hardcoded request class.
