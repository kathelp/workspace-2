# Launch Labs — Earn-Out Strategy

## The Deal
- Launch Labs acquired by **Banyan Software** (PE)
- Earn-out: up to **$11M** based on **incremental net recurring revenue growth**
- Structure: **Year-over-year** — each lookback period measures growth over the *previous* period
- Timeline: 3 annual lookback periods (or until $11M earned)
- **Only top-line NRR matters** — expenses are irrelevant to earn-out

## Baseline (March 2025 – Feb 2026)
- **Total Revenue:** $6.47M
- **Current Run Rate (Feb 2026):** ~$633K/mo → **$7.6M annualized**
- **Already ~$1.1M above baseline** on annualized basis

## Revenue Model

### Tier 1 — Usage-Based Agencies
- Agencies resell Ignite platform to their dealer clients
- Variable revenue based on usage
- Natural organic growth as agencies add dealers
- **Feb 2026:** $470K/mo in subscriptions
- **Pipeline:** "New Ignite Partner" in Pipedrive (Auto + Non-Auto)

### Tier 2 — Fixed Rate Agreements
- Graduated agencies move from usage-based to fixed annual agreements
- **No downward churn adjustment** — revenue is locked
- Grow ~**20% per year** at renewal
- Conversion is currently **ad hoc** — no formal pipeline or trigger criteria
- **Feb 2026:** $98K/mo (CF Search $65K, Moran Group $33K)

### Tier 3 — Focal Graph / Enterprise Direct
- New revenue motion — direct sales, not through channel
- 12-month fixed agreements
- **Feb 2026:** $20K/mo (3 customers: Lotlinx $7.5K, Morgan Auto $7.5K, Activator $5K)
- **Pipeline:** "Enterprise Data & APIs" in Pipedrive

### Add-On Packages
- Upsell on top of Tier 1 and Tier 2 accounts
- **Feb 2026:** $35K/mo
- **Pipeline:** "Ignite Package Upsells" in Pipedrive

## Customer Profile (Feb 2026)
- **67 total customers**
- **Top 5 = 42% of revenue** (moderate concentration)
- Top customer: Catalyst IQ at $79K/mo
- Long tail: ~30 customers at $1-2K/mo
- **479 active dealer trials** through agencies

## Pipeline (as of March 2026)
| Segment | Open Deals | Total Value |
|---------|-----------|-------------|
| New Ignite Partner - Auto | 10 | $856K |
| New Ignite Partner - Non-Auto | 7 | $240K |
| Enterprise Data & APIs | 3 | $120K |
| Package Upsells | TBD | TBD |
| **Total (excl. trials)** | **20+** | **~$1.2M+** |

### Notable Pipeline Deals
- **Cars Commerce** — $60K, Proposal Submitted (late stage)
- **CarGurus** — $60K, Pilot Outline Agreed
- **JDT Marketing** — $120K, Billing Setup (near close)
- **Crossroads Auto** — $100K, Billing Setup (near close)
- **3 agencies in demo stage** — $120K each

## Growth Math
- Need **$11M total earn-out** across 3 years
- Incremental YoY means ~**$3.7M net new per year**
- Year 3 target revenue: ~**$17.5M** (from $6.47M baseline)
- Must **nearly triple the business**

## 5 Growth Levers
1. **Land new agencies** (Tier 1 pipeline)
2. **Grow usage within existing agencies** (organic + package upsells)
3. **Graduate agencies to fixed rate** (Tier 1 → Tier 2)
4. **Expand fixed rate renewals** (~20%/yr built in)
5. **Close enterprise direct deals** (Tier 3 — highest ACV potential)

## Data Access
| System | Status | Notes |
|--------|--------|-------|
| Gmail (work) | ✅ Connected | garrett@launchlabs.ai via gog |
| Pipedrive CRM | ✅ Connected | API key in Keychain |
| Charges LLM schema/query API | ✅ Connected | Read-only analytics access via `/api/llm/schema` and `/api/llm/query` with `llm_token` |
| Legacy Charges invoice endpoints | ✅ Documented | `/api/invoices`, `/api/invoices/:id`, `/api/deal_invoices` |

### Charges Data Model - What we can analyze now
The new Charges analytics API exposes a useful billing warehouse slice covering:
- `accounts` - customer records, subscription flags, subscription dates, monthly subscription amount
- `charges` - line-item billed activity by account, billing application, invoice, and billing period
- `invoices` - billed amount, balance, due date, and status
- `payments` - cash collection against invoices
- `billing_applications` - source products or billing streams behind charges and subscription events
- `forecasted_charges` - projected billing by account and period
- `flat_rates` - fixed recurring commercial terms
- `enterprise_sales` - enterprise recurring terms
- `subscription_events` - lifecycle signals like upgrades, downgrades, churn, or activations
- `contacts` - account contacts

### What this unlocks for earn-out analysis
This is materially better than the earlier endpoint plan because we can now answer both billing and revenue questions with direct SQL instead of waiting on separate purpose-built endpoints.

High-value analyses now possible:
- monthly billed revenue by account and billing application
- split between usage-based, flat-rate, and enterprise-style revenue models
- invoice balances and receivables aging
- forecast vs actual revenue by month
- subscription lifecycle trends from `subscription_events`
- active commercial terms and upcoming expirations
- revenue concentration across top accounts

### Immediate hypotheses to validate in Charges
1. `billing_applications` may map closely to revenue streams that matter for earn-out segmentation
2. `flat_rates` and `enterprise_sales` should make Tier 2 and Tier 3 revenue measurable without separate mocked endpoints
3. `forecasted_charges` may provide an early warning layer for future revenue tracking
4. `subscription_events` may be the cleanest source for upgrade, downgrade, churn, and activation analysis

## Open Questions
- What's the organic growth rate of usage-based revenue (if nothing changes)?
- What's the churn rate?
- What triggers a fixed rate conversion conversation?
- How many more agencies are candidates for fixed rate?
- Focal Graph pipeline depth — how many enterprise prospects exist?
- Sales team: who's selling each tier, and what's capacity?

## TODO
- [x] Charges analytics API documentation captured locally
- [ ] Run first-pass SQL exploration of Charges schema and validate mapping from tables to Tier 1, Tier 2, Tier 3, and add-on revenue buckets
- [ ] Formalize Tier 1 → Tier 2 conversion tracking (pipeline or criteria)
- [ ] Build automated monthly revenue tracking using Charges + Pipedrive
- [ ] Develop detailed growth strategy per lever

---
*Last updated: 2026-03-07*
