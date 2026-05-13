# Ontology Mapping Contract

Ontology is a candidate mapping aid. It is not a fixed taxonomy, not a product
enum, and not a use-case router. The planner keeps the user's surface terms and
uses ontology only to propose source-specific identifiers.

## Candidate Mapping Targets

Free-text `subjects` may map to:

- aliases
- HS codes
- KOSIS categories
- Naver categories
- Google Trends queries
- KOTRA keywords
- DART business segment terms
- GICS codes
- KSIC codes
- SIC codes
- NAICS codes

## Mapping Record

```yaml
subject_mapping:
  surface_form: string
  normalized_aliases: []
  candidate_identifiers:
    hs_codes: []
    kosis_categories: []
    naver_categories: []
    google_trends_queries: []
    kotra_keywords: []
    dart_business_segments: []
    classification_codes:
      gics: []
      ksic: []
      sic: []
      naics: []
  mapping_confidence: null
  unresolved_terms: []
  source_specific_notes: []
```

## Unknown Concept Behavior

```yaml
unknown_concept_behavior:
  - keep_surface_form
  - generate_search_terms
  - mark_low_confidence_mapping
  - do_not_force_to_existing_category
  - proceed_with_best_effort_evidence_plan
```

## Rules

- Preserve the original `surface_form` in every plan and ledger reference.
- A candidate identifier does not prove that the mapping is correct.
- Low-confidence mappings must select validation gates that can catch overclaiming.
- Source routing uses evidence requirements even when ontology mapping is incomplete.
- Unknown subjects remain valid research subjects.
