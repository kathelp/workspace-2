# Charges Data Access

Base URL: `https://charges.launchlabs.ai`

This document covers two ways to access Charges data:
- Legacy invoice-oriented HTTP endpoints
- New LLM analytics endpoints for schema discovery and read-only SQL

## 1) LLM Analytics Access

Authentication:
- Every request includes `llm_token` in the URL
- Current token:
  - `llm_d56f5ef48a062189e2aecf6fc8a4844adf18926b0968203c65a9124a4d3717cf`

### Endpoints

#### Schema endpoint
`GET /api/llm/schema`

Example:
```bash
curl "https://charges.launchlabs.ai/api/llm/schema?llm_token=LLM_TOKEN"
```

Purpose:
- Returns the curated analytics schema
- Lists allowed tables and columns
- Provides join hints
- Includes example queries
- Includes business guidance and SQL guardrails

#### Query endpoint
`POST /api/llm/query`

Example:
```bash
curl -X POST "https://charges.launchlabs.ai/api/llm/query?llm_token=LLM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT accounts.name, invoices.amount FROM invoices JOIN accounts ON accounts.id = invoices.account_id LIMIT 10"}'
```

Purpose:
- Executes read-only SQL
- Returns tabular JSON results
- Intended for exploratory analytics, billing analysis, revenue reporting, and account-level investigation

### How to use it
1. Call the schema endpoint first
2. Read available relations, columns, joins, example queries, and business guidance
3. Form hypotheses about the data model and workflows
4. Run small, explicit, qualified `SELECT` queries through the query endpoint
5. If a query is rejected, repair it using the returned error plus the schema response

### Guardrails
- Read-only
- Single statement only
- Allowed statement type: `SELECT`
- Wildcards are not allowed
- Subqueries are not allowed
- SQL comments are not allowed
- Qualified column names are required
- Max rows: 200
- Timeout: 3000 ms

### Available relations

#### `accounts`
Customer accounts and subscription attributes.

Useful columns:
- `accounts.id`
- `accounts.company_id`
- `accounts.parent_account_id`
- `accounts.name`
- `accounts.city`
- `accounts.state`
- `accounts.website_address`
- `accounts.monthly_subscription_amount`
- `accounts.active_indirect_subscriber`
- `accounts.self_serve`
- `accounts.trial_subscription`
- `accounts.subscription_start_date`
- `accounts.subscription_end_date`
- `accounts.created_at`
- `accounts.updated_at`

Joins:
- `accounts.id = contacts.account_id`
- `accounts.id = charges.account_id`
- `accounts.id = invoices.account_id`

#### `charges`
Line-item charges attached to accounts and invoices.

Useful columns:
- `charges.id`
- `charges.account_id`
- `charges.billing_application_id`
- `charges.invoice_id`
- `charges.billing_period`
- `charges.amount`
- `charges.override_amount`
- `charges.description`
- `charges.remote_id`
- `charges.charge_entity_id`
- `charges.created_at`
- `charges.updated_at`

Joins:
- `charges.account_id = accounts.id`
- `charges.invoice_id = invoices.id`
- `charges.billing_application_id = billing_applications.id`

#### `invoices`
Invoices generated for accounts and companies.

Useful columns:
- `invoices.id`
- `invoices.account_id`
- `invoices.company_id`
- `invoices.amount`
- `invoices.balance`
- `invoices.billing_period`
- `invoices.due_date`
- `invoices.status`
- `invoices.created_at`
- `invoices.updated_at`

Joins:
- `invoices.account_id = accounts.id`
- `invoices.id = payments.invoice_id`
- `invoices.id = charges.invoice_id`

#### `contacts`
Contact records for customer accounts.

Useful columns:
- `contacts.id`
- `contacts.account_id`
- `contacts.company_id`
- `contacts.name`
- `contacts.email`
- `contacts.phone`
- `contacts.created_at`
- `contacts.updated_at`

Joins:
- `contacts.account_id = accounts.id`

#### `billing_applications`
Billing applications that originate charges or subscription events.

Useful columns:
- `billing_applications.id`
- `billing_applications.company_id`
- `billing_applications.name`
- `billing_applications.quickbooks_item_id`
- `billing_applications.quickbooks_item_name`
- `billing_applications.created_at`
- `billing_applications.updated_at`

Joins:
- `billing_applications.id = charges.billing_application_id`
- `billing_applications.id = subscription_events.billing_application_id`

#### `billing_applications_accounts`
Join table mapping billing applications to accounts.

Useful columns:
- `billing_applications_accounts.id`
- `billing_applications_accounts.account_id`
- `billing_applications_accounts.billing_application_id`
- `billing_applications_accounts.href`
- `billing_applications_accounts.remote_id`
- `billing_applications_accounts.created_at`
- `billing_applications_accounts.updated_at`

Joins:
- `billing_applications_accounts.account_id = accounts.id`
- `billing_applications_accounts.billing_application_id = billing_applications.id`

#### `forecasted_charges`
Projected charges by account and billing period.

Useful columns:
- `forecasted_charges.id`
- `forecasted_charges.account_id`
- `forecasted_charges.billing_application_id`
- `forecasted_charges.billing_period`
- `forecasted_charges.amount`
- `forecasted_charges.description`
- `forecasted_charges.created_at`
- `forecasted_charges.updated_at`

Joins:
- `forecasted_charges.account_id = accounts.id`
- `forecasted_charges.billing_application_id = billing_applications.id`

#### `flat_rates`
Flat-rate commercial terms for accounts.

Useful columns:
- `flat_rates.id`
- `flat_rates.account_id`
- `flat_rates.description`
- `flat_rates.monthly_amount`
- `flat_rates.notes`
- `flat_rates.start_date`
- `flat_rates.end_date`
- `flat_rates.created_at`
- `flat_rates.updated_at`

Joins:
- `flat_rates.account_id = accounts.id`

#### `enterprise_sales`
Enterprise sale pricing terms for accounts.

Useful columns:
- `enterprise_sales.id`
- `enterprise_sales.account_id`
- `enterprise_sales.description`
- `enterprise_sales.monthly_amount`
- `enterprise_sales.notes`
- `enterprise_sales.start_date`
- `enterprise_sales.end_date`
- `enterprise_sales.created_at`
- `enterprise_sales.updated_at`

Joins:
- `enterprise_sales.account_id = accounts.id`

#### `payments`
Payments collected for invoices.

Useful columns:
- `payments.id`
- `payments.account_id`
- `payments.invoice_id`
- `payments.amount`
- `payments.fee`
- `payments.created_at`
- `payments.updated_at`

Joins:
- `payments.account_id = accounts.id`
- `payments.invoice_id = invoices.id`

#### `subscription_events`
Subscription lifecycle events and event amounts.

Useful columns:
- `subscription_events.id`
- `subscription_events.account_id`
- `subscription_events.billing_application_id`
- `subscription_events.amount_in_cents`
- `subscription_events.event_date`
- `subscription_events.event_type`
- `subscription_events.subscription_remote_id`
- `subscription_events.created_at`
- `subscription_events.updated_at`

Joins:
- `subscription_events.account_id = accounts.id`
- `subscription_events.billing_application_id = billing_applications.id`

### Business playbook from schema
- Use `accounts` for customer and subscription attributes
- Use `charges` and `invoices` for billing and receivables analysis
- Use `flat_rates` and `enterprise_sales` for pricing term analysis
- Use `forecasted_charges` and `subscription_events` for forward-looking or lifecycle reporting

### Initial dataset summary
The analytics schema suggests the Charges application models billing across five connected layers:
1. Customer/account master data in `accounts`
2. Source systems or product lines in `billing_applications`
3. Billable line items in `charges`
4. Commercial terms in `flat_rates` and `enterprise_sales`
5. Invoicing, collections, and lifecycle history in `invoices`, `payments`, `forecasted_charges`, and `subscription_events`

This is enough to answer not just invoice questions, but also:
- account-level revenue composition
- application-level revenue contribution
- billed vs forecasted revenue
- receivables and payment timing
- recurring term coverage and start/end timing
- subscription lifecycle changes over time

### High-value SQL questions to answer next
Before deeper analysis, these are good first questions:
- Which accounts generated the most charges in the latest billing period?
- How much billed revenue came from each billing application by month?
- Which invoices are still open, overdue, or only partially paid?
- Which accounts have active flat-rate or enterprise-sale terms right now?
- Which forecasted charges differ most from actual charges by account or application?
- Which subscription events indicate upgrades, downgrades, churn, or reactivations?
- Which accounts have recurring commercial terms ending soon?
- How concentrated is revenue across the top 5, top 10, and long-tail accounts?

## 2) Legacy Invoice-Oriented API Access

These older endpoints still exist and are useful for application-facing invoice retrieval.

### Authentication
All endpoints require query params:
- `api_token`
- `api_secret`

In development, `api_secret` is bypassed.

### Date handling
For endpoints that accept `billing_period`, send `YYYY-MM-DD`.
If omitted, the API defaults to `Date.today`.

---

### Invoices Index
`GET /api/invoices`

Returns invoice records for a billing period.

#### Query params
| Param | Required | Notes |
|---|---|---|
| `api_token` | Yes | Billing application token |
| `api_secret` | Yes | Billing application secret |
| `account_pipedrive_id` | No | Filters to one account by `accounts.pipedrive_id` |
| `account_token` | No | Legacy filter by account token, still supported |
| `billing_period` | No | `YYYY-MM-DD` |
| `invoice_status` | No | Example: `open`, `paid` |

#### Response
Returns invoice records with nested account and charges.

Notes:
- Invoices with an active flat rate for the billing period are excluded
- CSV format is supported through request format negotiation

---

### Invoice Show
`GET /api/invoices/:id`

Returns one invoice by invoice token.

#### Query params
- `api_token`
- `api_secret`

Notes:
- `:id` is invoice token, not numeric DB id

---

### Deal Invoices
`GET /api/deal_invoices`

Returns mocked invoice-like records for:
- active flat rates in the month
- active enterprise sales in the month

"Active in month" means overlap with the requested month:
- `start_date <= month_end`
- `end_date >= month_start`

#### Query params
- `api_token`
- `api_secret`
- `billing_period`
- `account_pipedrive_id`

Notes:
- These are not persisted `Invoice` records
- Amount is derived from `monthly_amount`
- Returned ids are prefixed, for example `fixed_rate_12` or `enterprise_sale_8`

## Recommended next step
Use the LLM schema endpoint as the default discovery tool, then build a small library of vetted read-only SQL queries for:
- monthly recurring revenue by segment
- earn-out tracking by account and billing application
- open receivables
- forecast vs actual revenue
- upcoming term expirations and lifecycle events
