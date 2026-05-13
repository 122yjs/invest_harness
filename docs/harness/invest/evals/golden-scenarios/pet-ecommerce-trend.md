# Golden Scenario: pet-ecommerce-trend

This is an eval fixture only. It must not become a core router category.

## Input

```text
국내 반려동물 이커머스 트렌드가 관련 상장사에 주는 영향을 분석해줘.
```

## Expected Decomposition

- subjects from surface form:
  - 국내 반려동물 이커머스
  - 관련 상장사
- required evidence types:
  - search_interest
  - market_transaction
  - optional official/admin proxy
  - company_disclosure
- signal primitives:
  - search_interest_momentum
  - transaction_market_size
  - disclosure_exposure

## Expected Boundaries

- Search index is not market size.
- Search interest is not sales.
- Market transaction evidence needs source definition, unit, geography, and period.
- No fixed `use_case` routing is allowed.
