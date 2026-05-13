# Claim Boundary Policy

Every claim must state the evidence required, wording allowed, wording forbidden,
and caveats required. If the evidence is weaker than the claim, downgrade the
claim wording before analyst fan-out or QA approval.

## Claim Contract

| Field | Meaning |
|---|---|
| claim | What the report wants to say |
| required evidence | Evidence types needed before the claim is allowed |
| allowed wording | Bounded language the report may use |
| forbidden wording | Overclaims that must fail QA |
| required caveats | Limits that must appear near the claim |

## Mandatory Prohibitions

- Google Trends is not market size.
- Search interest is not sales.
- Customs trade is not company revenue.
- KOTRA text is not export volume.
- Public procurement is not total market demand.
- Macro indicators are not company causality without an exposure mechanism.

## Consumer Interest Claim

- claim: consumers or market participants show rising/falling attention.
- required evidence: `search_interest` with query/topic, geography, timeframe, and relative index caveat.
- allowed wording: "relative search interest increased", "attention proxy improved", "query momentum weakened".
- forbidden wording: "sales increased", "market size expanded", "revenue rose" unless transaction, export, or company disclosure evidence also supports it.
- required caveats: search interest is relative, query-dependent, and not a transaction metric.

## Export Momentum Claim

- claim: exports or imports for a mapped item/geography are rising/falling.
- required evidence: `export_import` with mapped code/category, country, period, value or weight, and base-effect check.
- allowed wording: "mapped trade value rose", "export momentum improved", "shipment proxy weakened".
- forbidden wording: "company revenue grew" unless `company_disclosure` or segment exposure evidence supports attribution.
- required caveats: mapping confidence, item coverage, country scope, latest period, value vs weight basis.

## Market Size Claim

- claim: a defined market has a transaction or official baseline.
- required evidence: `market_transaction` or `official_statistics` with unit, period, geography, and source definition.
- allowed wording: "official transaction baseline", "reported category value", "defined-market proxy".
- forbidden wording: "total addressable market" without source coverage limits and methodology.
- required caveats: source coverage, excluded channels, unit, and update date.

## Procurement Demand Claim

- claim: public buyers show demand or budget activity.
- required evidence: `procurement` records with tender/award distinction, buyer, amount, date, and status.
- allowed wording: "public procurement activity increased", "award value suggests public-sector demand".
- forbidden wording: "total market demand increased" or "private demand increased" from procurement alone.
- required caveats: public-sector scope, tender vs award status, cancellations, buyer concentration.

## Company Exposure Claim

- claim: a company is exposed to a subject, geography, customer, or supply chain node.
- required evidence: `company_disclosure` or verified company materials identifying the exposure.
- allowed wording: "company discloses exposure", "segment notes indicate relevance", "risk factor mentions".
- forbidden wording: "material revenue driver" without quantified or strongly supported disclosure evidence.
- required caveats: filing period, qualitative vs quantitative disclosure, and stale-report risk.

## Regulatory Risk Claim

- claim: policy or regulation can affect a subject, company, or value chain.
- required evidence: `regulatory` or `macro_policy` source with effective date and affected scope.
- allowed wording: "regulatory risk increased", "policy change may affect margins", "compliance burden is a monitoring item".
- forbidden wording: "earnings will decline by X" without company exposure and quantified scenario evidence.
- required caveats: proposed vs enacted status, timing, affected geography, uncertainty.

## Valuation Claim

- claim: market price, multiple, DCF, or peer evidence supports a valuation anchor.
- required evidence: `price_valuation` with date, source, share count, financial metric period, and calculation path.
- allowed wording: "valuation anchor", "multiple comparison", "scenario-implied range".
- forbidden wording: "guaranteed upside" or "certain mispricing".
- required caveats: price date, metric period, peer comparability, scenario assumptions.

## Macro Sensitivity Claim

- claim: macro regime or indicator changes may affect the thesis.
- required evidence: `macro_policy` or `macro_indicator` plus a stated exposure mechanism.
- allowed wording: "macro backdrop is supportive", "rates are a headwind", "sensitivity should be monitored".
- forbidden wording: "company earnings changed because of macro indicator alone".
- required caveats: indicator series, geography, period, revision risk, exposure pathway.
