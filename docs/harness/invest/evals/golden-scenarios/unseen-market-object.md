# Golden Scenario: unseen-market-object

This is an eval fixture only. It verifies unknown subjects are preserved.

## Input

```text
인도네시아 니켈 수출 제한이 한국 배터리 소재주에 미치는 영향 분석해줘.
```

## Expected Decomposition

- subjects:
  - 니켈
  - 수출 제한
  - 한국 배터리 소재주
- geographies:
  - Indonesia
  - Korea
- required evidence types:
  - regulatory
  - supply_chain
  - export_import
  - company_disclosure
  - price_valuation
- signal primitives:
  - regulatory_risk_signal
  - export_momentum
  - disclosure_exposure
  - valuation_anchor

## Expected Boundaries

- Preserve unknown surface terms.
- Do not force the request into an unrelated known example.
- Use ontology only for candidate mapping.
