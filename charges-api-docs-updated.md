# Charges API Documentation (LLM Access)

## Overview
The Charges application provides authenticated HTTP endpoints for billing data access and read-only SQL analytics.

## Authentication
All endpoints use a single LLM token in the request URL:
```
llm_token=llm_7c2530195f588cabd7a7e9eed97eead2ee9e7393e51b3dca7d8d31d5ca1d21cf
```

**Important:** With an LLM token, do NOT send `api_token` or `api_secret`.

## REST API Endpoints

### Invoices Index
**Endpoint:** `GET https://charges.launchlabs.ai/api/invoices?llm_token=llm_7c2530195f588cabd7a7e9eed97eead2ee9e7393e51b3dca7d8d31d5ca1d21cf`

**Returns:** Array of invoice objects with account details, charges, and billing information.

**Response Structure:**
```json
[
  {
    "id": "FR_10",
    "amount_in_dollars": "$17,000.00",
    "amount_in_cents": 1700000,
    "billing_period": "2026-04-30",
    "due_date": "2026-05-01",
    "status": "open",
    "account": {
      "pipedrive_id": 30,
      "name": "MOD Marketing",
      "address": "207 N Main St Ste 117, Rolesville, NC 27571",
      "account_manager": "Kelsey",
      "billing_emails": ["travis@modmarketing.com", "billing@modmarketing.com"]
    },
    "charges": [
      {
        "id": 32158,
        "amount_in_dollars": "$17,000.00",
        "amount_in_cents": 1700000,
        "description": "Fixed Rate: MOD Marketing (29 subscriptions)",
        "billing_period": "2026-04-30",
        "item_id": "100"
      }
    ]
  }
]
```

**Key Notes:**
- Amounts are provided in BOTH `amount_in_dollars` (formatted string) and `amount_in_cents` (integer)
- Use `amount_in_cents` for calculations, `amount_in_dollars` for display
- Status values: `open`, `paid`, `closed`, `historical`, `voided`

### Single Invoice
**Endpoint:** `GET https://charges.launchlabs.ai/api/invoices/{INVOICE_TOKEN}?llm_token=llm_7c2530195f588cabd7a7e9eed97eead2ee9e7393e51b3dca7d8d31d5ca1d21cf`

Replace `{INVOICE_TOKEN}` with the invoice ID (e.g., `FR_10`).

**Returns:** Single invoice object with same structure as above.

### Deal Invoices
**Endpoint:** `GET https://charges.launchlabs.ai/api/deal_invoices?llm_token=llm_7c2530195f588cabd7a7e9eed97eead2ee9e7393e51b3dca7d8d31d5ca1d21cf`

**Returns:** Flat-rate and enterprise deal invoices (subset of all invoices).

Same structure as the invoices endpoint.

## SQL Analytics (Read-Only)

### Schema Endpoint
**Endpoint:** `GET https://charges.launchlabs.ai/api/llm/schema?llm_token=llm_7c2530195f588cabd7a7e9eed97eead2ee9e7393e51b3dca7d8d31d5ca1d21cf`

**Purpose:** Retrieve the analytics schema BEFORE running queries.

**Returns:**
- Available relations (tables)
- Column names and types for each table
- Primary keys and join relationships
- Example queries
- Business guidance
- Query guardrails and restrictions

**Always call this first** to understand the data model before querying.

### Query Endpoint
**Endpoint:** `POST https://charges.launchlabs.ai/api/llm/query?llm_token=llm_7c2530195f588cabd7a7e9eed97eead2ee9e7393e51b3dca7d8d31d5ca1d21cf`

**Request Body:**
```json
{
  "sql": "SELECT accounts.name, accounts.monthly_subscription_amount FROM accounts LIMIT 10"
}
```

**⚠️ CRITICAL:** The parameter name is `sql`, NOT `query`.

**Response:**
```json
{
  "columns": ["name", "monthly_subscription_amount"],
  "rows": [
    {"name": "Glendale INFINITI", "monthly_subscription_amount": 1000.0},
    {"name": "CF Search", "monthly_subscription_amount": 0.0}
  ],
  "row_count": 2,
  "truncated": false,
  "elapsed_ms": 3
}
```

**Error Response:**
```json
{
  "error": {
    "code": "invalid_query",
    "message": "Unqualified column references are not allowed: total_charges."
  }
}
```

## SQL Query Guardrails

The query endpoint enforces strict read-only constraints:

### ✅ Allowed
- `SELECT` statements only
- Qualified column references (e.g., `accounts.name`, `charges.amount`)
- Standard aggregations: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`
- `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT`
- `JOIN` operations (see schema for valid joins)
- Date literals: `DATE '2026-01-01'`

### ❌ Not Allowed
- Wildcards (`SELECT *`)
- Subqueries
- `CASE` statements
- SQL comments (`--` or `/* */`)
- Unqualified column references (aliases in `ORDER BY` or `GROUP BY`)
- Multiple statements
- Non-SELECT operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.)

### Limits
- **Max rows:** 200
- **Timeout:** 3 seconds
- **Single statement only**

### Writing Valid Queries

**❌ This will fail:**
```sql
SELECT accounts.name, SUM(charges.amount) AS total
FROM accounts
JOIN charges ON charges.account_id = accounts.id
GROUP BY accounts.name
ORDER BY total DESC
```
*Reason:* `total` is an unqualified alias.

**✅ This will work:**
```sql
SELECT accounts.name, SUM(charges.amount)
FROM accounts
JOIN charges ON charges.account_id = accounts.id
GROUP BY accounts.name
ORDER BY SUM(charges.amount) DESC
LIMIT 25
```
*Note:* Repeat the aggregate function in `ORDER BY` instead of using an alias.

## Data Model Key Facts

### Currency Storage
**⚠️ CRITICAL:** The `charges.amount` column stores values in **cents**, not dollars.

- `charges.amount = 1700000` means **$17,000.00**
- Always divide by 100 to convert to dollars for display
- REST API endpoints provide both `amount_in_cents` and `amount_in_dollars`

### Available Relations
- **accounts** - Customer subscription records
- **charges** - Line-item charges (stored in cents)
- **invoices** - Billing periods with amounts and status
- **billing_applications** - Products/services generating charges (e.g., "Ignite")
- **flat_rates** - Fixed monthly pricing terms
- **enterprise_sales** - Enterprise deal pricing
- **forecasted_charges** - Revenue projections
- **subscription_events** - Lifecycle events (starts, cancellations)
- **payments** - Payment records with fees
- **contacts** - Account contact information

### Common Joins
```sql
-- Accounts to charges
accounts.id = charges.account_id

-- Accounts to invoices
accounts.id = invoices.account_id

-- Charges to invoices
charges.invoice_id = invoices.id

-- Charges to billing applications
charges.billing_application_id = billing_applications.id
```

## Recommended Workflow

1. **Fetch schema first:**
   ```bash
   curl 'https://charges.launchlabs.ai/api/llm/schema?llm_token=...'
   ```

2. **Review available tables, columns, and example queries**

3. **Form hypotheses** about the data model and business workflows

4. **Write explicit, qualified SELECT queries:**
   ```bash
   curl -X POST 'https://charges.launchlabs.ai/api/llm/query?llm_token=...' \
     -H 'Content-Type: application/json' \
     -d '{"sql": "SELECT accounts.name, SUM(charges.amount) FROM accounts JOIN charges ON charges.account_id = accounts.id WHERE charges.billing_period >= DATE '\''2026-01-01'\'' GROUP BY accounts.name ORDER BY SUM(charges.amount) DESC LIMIT 25"}'
   ```

5. **If query is rejected,** read the error message and adjust based on guardrails

6. **For invoice listing or single invoice detail,** use REST endpoints instead of SQL

7. **Remember:** `charges.amount` is in cents - divide by 100 for dollar amounts

## Common Mistakes to Avoid

1. **Using `query` instead of `sql` in POST body** - Parameter name is `sql`
2. **Assuming dollar amounts** - `charges.amount` is stored in cents
3. **Using unqualified aliases in ORDER BY** - Repeat the full expression instead
4. **Skipping the schema endpoint** - Always fetch schema first to understand the data model
5. **Forgetting table qualifiers** - All column references must be prefixed with table name
6. **Trying to use wildcards** - `SELECT *` is not allowed

## Example Queries

### Top accounts by charges (2026 YTD)
```json
{
  "sql": "SELECT accounts.name, SUM(charges.amount) FROM accounts JOIN charges ON charges.account_id = accounts.id WHERE charges.billing_period >= DATE '2026-01-01' GROUP BY accounts.name ORDER BY SUM(charges.amount) DESC LIMIT 25"
}
```

### Open invoices with outstanding balances
```json
{
  "sql": "SELECT accounts.name, invoices.amount, invoices.balance, invoices.due_date FROM invoices JOIN accounts ON accounts.id = invoices.account_id WHERE invoices.status = 'open' AND invoices.balance > 0 ORDER BY invoices.due_date ASC LIMIT 25"
}
```

### Active flat-rate deals
```json
{
  "sql": "SELECT accounts.name, flat_rates.monthly_amount, flat_rates.start_date, flat_rates.end_date FROM flat_rates JOIN accounts ON accounts.id = flat_rates.account_id WHERE flat_rates.end_date IS NULL OR flat_rates.end_date > DATE '2026-04-13' ORDER BY flat_rates.monthly_amount DESC"
}
```

### Subscription events (2026 YTD)
```json
{
  "sql": "SELECT subscription_events.event_type, COUNT(subscription_events.id) FROM subscription_events WHERE subscription_events.event_date >= DATE '2026-01-01' GROUP BY subscription_events.event_type ORDER BY COUNT(subscription_events.id) DESC"
}
```

## Support
If endpoints return errors:
- **500 errors:** Check server logs using the `x-request-id` response header
- **422 errors:** Review query against guardrails and error message
- **401 errors:** Verify `llm_token` parameter is correct
