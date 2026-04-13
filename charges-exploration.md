# Charges Application Dataset Exploration
**Date:** 2026-04-13  
**Token:** `llm_7c2530195f588cabd7a7e9eed97eead2ee9e7393e51b3dca7d8d31d5ca1d21cf`

## Schema Summary

The Charges application tracks:
- **Accounts** (customers with subscription attributes)
- **Charges** (line-item charges by account, invoice, billing period)
- **Invoices** (billing periods with amounts, balances, status)
- **Billing Applications** (products/services generating charges)
- **Flat Rates & Enterprise Sales** (alternative pricing models)
- **Forecasted Charges** (forward revenue projections)
- **Subscription Events** (lifecycle events: starts, cancellations, upgrades)
- **Payments** (payment records with fees)
- **Contacts** (account contact info)

## Dataset Snapshot (2026 YTD)

### Top Accounts by Charges (Jan 1 - Apr 13, 2026)
1. **Catalyst IQ** - $70.99M
2. **Retargit** - $33.31M
3. **CF Search** - $31.44M
4. **The Moran Group** - $19.19M
5. **Turnkey Marketing** - $17.83M
6. **Pin-Up Marketing** - $16.39M
7. **MUDD Advertising** - $14.71M
8. **The Market Doctors - LeadRX** - $13.03M
9. **launchlabs | Chumney | FPD360** - $8.28M
10. **iFrog Marketing Solutions** - $8.24M

### Billing Applications
- **Ignite** is the dominant product (32,560 charges)
- No other billing applications show significant volume

### Invoice Status Distribution
- **Historical:** 978 invoices ($0 balance)
- **Paid:** 977 invoices ($602,698.18)
- **Closed:** 530 invoices ($120,665.96)
- **Open:** 133 invoices ($345,254.19)
- **Voided:** 1 invoice ($0)

### Active Flat Rate Deals (as of Apr 13, 2026)
8 active flat-rate contracts:

| Account | Monthly Amount | Start Date | End Date |
|---------|---------------|------------|----------|
| Catalyst IQ | $70,200 | 2026-01-01 | 2026-12-31 |
| CF Search | $65,000 | 2026-02-01 | 2027-01-31 |
| The Moran Group | $33,000 | 2026-02-01 | 2027-01-31 |
| Retargit | $30,000 | 2026-01-01 | 2026-12-31 |
| The Market Doctors - LeadRX | $27,500 | 2026-04-01 | 2027-03-31 |
| MOD Marketing | $17,000 | 2026-01-01 | 2026-12-31 |
| launchlabs \| Chumney \| FPD360 | $15,000 | 2026-01-01 | 2026-12-31 |
| Pin-Up Marketing | $13,500 | 2026-01-01 | 2026-12-31 |

**Total flat-rate MRR:** $271,200/month

### Subscription Activity (2026 YTD)
- **Starts:** 303
- **Cancellations:** 203
- **Net new:** +100 subscriptions

### Outstanding AR Sample (Due May 1, 2026)
Top 10 open invoices by balance:
1. MUDD Advertising - $38,131.34
2. Action Integrated Marketing - $27,000.00
3. Roadmaster Marketing - $5,339.58
4. Fairway Chevrolet GMC - $5,445.00
5. Blue Gorilla Digital Agency - $5,000.00
6. Auto Marketing Team - $4,049.00
7. The Moran Group - $3,425.00

Most open invoices show balances at ~1% of invoice amount (likely deposits or payment plans).

## Available Endpoints

### REST APIs
- **Invoices:** `GET /api/invoices?llm_token=...` (currently 500 error)
- **Single Invoice:** `GET /api/invoices/:token?llm_token=...`
- **Deal Invoices:** `GET /api/deal_invoices?llm_token=...` (✅ working)

### SQL Analytics
- **Schema:** `GET /api/llm/schema?llm_token=...` (✅ working)
- **Query:** `POST /api/llm/query?llm_token=...` with `{"sql": "SELECT ..."}` (✅ working)

#### SQL Guardrails
- Read-only SELECT queries only
- No wildcards, subqueries, CASE statements, or comments
- All column references must be table-qualified
- 200 row limit, 3-second timeout
- Single statement only

## High-Value Questions I Can Answer

### Revenue Analysis
- MRR breakdown (flat-rate vs usage-based)
- Account concentration risk (top 10 customers as % of total)
- Month-over-month charge growth trends
- Average revenue per account by customer type

### AR & Collections
- Aging buckets for open invoices
- Payment collection rates and timelines
- Outstanding balance trends
- Fee analysis on collected payments

### Customer Lifecycle
- Trial conversion rates
- Churn rate and churn reasons (if captured in subscription events)
- Time-to-cancel after subscription start
- Subscription tenure distribution

### Product Performance
- Revenue attribution by billing application
- Cross-sell/upsell opportunities (accounts using multiple billing apps)
- Usage patterns by customer segment

### Forecasting
- Projected vs actual charge variance
- Flat-rate renewal pipeline (contracts expiring in next 90 days)
- Subscription growth trajectory

## Next Steps

Let me know what angle you want to explore:
- **Growth levers:** Which accounts are growing? Where's the expansion opportunity?
- **Churn risk:** Which flat-rate deals are expiring soon? What's the cancellation trend?
- **Collections:** How's AR aging? Any problem accounts?
- **Product mix:** What's the revenue split between Ignite subscriptions vs flat deals?
