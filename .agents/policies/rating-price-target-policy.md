<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/policies/rating-price-target-policy.md; kind=policy; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# Rating and Price Target Policy

## Purpose

The harness may produce ratings, price targets, implied upside/downside, and risk-reward summaries when the supporting evidence is explicit.

## Allowed Labels

Allowed rating language:

- Buy
- Outperform
- Neutral
- Hold
- Underperform
- Sell

Allowed valuation language:

- Price Target
- Target Price
- Implied Upside
- Implied Downside
- Bear / Base / Bull
- Risk-Reward

## Required Basis

Every rating or price target must tie back to:

- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`
- stated valuation method
- stated scenario assumptions
- explicit calculation of implied upside or downside
- major risks that could invalidate the view

## Consistency Checks

QA must check that:

- rating direction matches the base-case upside/downside and risk profile
- Bear/Base/Bull scenarios do not contradict the stated rating
- target price inputs are sourced or clearly assumed
- scenario probabilities, if used, are labeled as assumptions
- price-target math can be recalculated from the report inputs

## Boundary

This policy changes report vocabulary and QA expectations. It does not add personalized portfolio advice, suitability analysis, or account-specific recommendations.

