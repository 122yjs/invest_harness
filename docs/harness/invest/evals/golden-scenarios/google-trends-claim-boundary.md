# Golden Scenario: google-trends-claim-boundary

This is an eval fixture only. It verifies relative search evidence boundaries.

## Input

```text
Google Trends에서 관심도가 올랐으니 해당 시장 규모와 매출도 늘었는지 분석해줘.
```

## Expected Decomposition

- subjects:
  - Google Trends 관심도
  - 해당 시장 규모
  - 매출
- required evidence types:
  - search_interest
  - market_transaction
  - company_disclosure
- signal primitives:
  - search_interest_momentum
  - transaction_market_size
  - disclosure_exposure

## Expected Boundaries

- Google Trends is relative search interest only.
- Search interest is not sales.
- Google Trends is not market size.
- Sales or revenue claims require transaction or company disclosure evidence.
