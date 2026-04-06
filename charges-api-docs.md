# Billing APIs

Base url: `https://charges.launchlabs.ai`

This document covers:
- `GET /api/invoices`
- `GET /api/invoices/:id`
- `GET /api/deal_invoices`

## Authentication

All endpoints require query params:
- `api_token`
- `api_secret`

In development, `api_secret` is bypassed.

## Date handling

For endpoints that accept `billing_period`, send `YYYY-MM-DD`.
If omitted, the API defaults to `Date.today`.

---

## 1) Invoices Index

`GET /api/invoices`

Returns invoice records for a billing period.

### Query params

| Param | Required | Notes |
|---|---|---|
| `api_token` | Yes | Billing application token |
| `api_secret` | Yes | Billing application secret |
| `account_pipedrive_id` | No | Filters to one account by `accounts.pipedrive_id` |
| `account_token` | No | Legacy filter by account token (still supported) |
| `billing_period` | No | `YYYY-MM-DD` |
| `invoice_status` | No | Example: `open`, `paid` |

### Response (JSON)

Array of invoices, formatted as:

```json
[
  {
    "id": 123,
    "amount_in_dollars": "$500.00",
    "amount_in_cents": 50000,
    "billing_period": "2026-03-01",
    "due_date": "2026-03-31",
    "status": "open",
    "account": {
      "name": "Acme Corp"
    },
    "charges": [
      {
        "id": 456,
        "amount_in_dollars": "$500.00",
        "amount_in_cents": 50000,
        "description": "Monthly subscription",
        "billing_period": "2026-03-01",
        "item_id": "100"
      }
    ]
  }
]
```

### Notes

- Invoices with an active flat rate for the billing period are excluded.
- If the request format is CSV (for example `.csv`), the endpoint returns CSV export instead of JSON.

### Example

```bash
curl "https://charges.launchlabs.ai/api/invoices?api_token=TOKEN&api_secret=SECRET&billing_period=2026-03-01&invoice_status=open"
```

---

## 2) Invoice Show

`GET /api/invoices/:id`

Returns one invoice by **invoice token** (`:id` is token, not numeric DB id).

### Query params

| Param | Required | Notes |
|---|---|---|
| `api_token` | Yes | Billing application token |
| `api_secret` | Yes | Billing application secret |

### Response (JSON)

Raw invoice JSON including associated account and charges.

```json
{
  "id": 123,
  "token": "inv_token_here",
  "amount": 50000,
  "billing_period": "2026-03-01",
  "due_date": "2026-03-31",
  "status": "open",
  "account": {},
  "charges": []
}
```

### Example

```bash
curl "https://charges.launchlabs.ai/api/invoices/inv_token_here?api_token=TOKEN&api_secret=SECRET"
```

---

## 3) Deal Invoices (Mocked Flat Rate + Enterprise Sale Invoices)

`GET /api/deal_invoices`

Returns mocked invoice-like objects for:
- active flat rates in the requested month
- active enterprise sales in the requested month

"Active in month" means overlap with that month:
- `start_date <= month_end`
- `end_date >= month_start`

### Query params

| Param | Required | Notes |
|---|---|---|
| `api_token` | Yes | Billing application token |
| `api_secret` | Yes | Billing application secret |
| `billing_period` | No | `YYYY-MM-DD` |
| `account_pipedrive_id` | No | Filters to one account by `accounts.pipedrive_id` |

### Response (JSON)

Array of mocked invoice-like records:

```json
[
  {
    "id": "fixed_rate_12",
    "amount_in_dollars": "$2000.00",
    "amount_in_cents": 200000,
    "billing_period": "2026-03-01",
    "due_date": "2026-03-31",
    "status": "open",
    "account": {
      "name": "Acme Corp"
    },
    "charges": [
      {
        "id": null,
        "amount_in_dollars": "$2000.00",
        "amount_in_cents": 200000,
        "description": "Flat Rate Deal: Acme Corp",
        "billing_period": "2026-03-01",
        "item_id": "100"
      }
    ]
  },
  {
    "id": "enterprise_sale_8",
    "amount_in_dollars": "$5000.00",
    "amount_in_cents": 500000,
    "billing_period": "2026-03-01",
    "due_date": "2026-03-31",
    "status": "open",
    "account": {
      "name": "Beta LLC"
    },
    "charges": [
      {
        "id": null,
        "amount_in_dollars": "$5000.00",
        "amount_in_cents": 500000,
        "description": "Enterprise Sale: Beta LLC",
        "billing_period": "2026-03-01",
        "item_id": "100"
      }
    ]
  }
]
```

### Notes

- These are not persisted `Invoice` records.
- `amount_in_cents` is computed from `monthly_amount` (`monthly_amount * 100`).
- `id` is prefixed by source type: `fixed_rate_<id>` or `enterprise_sale_<id>`.

### Example

```bash
curl "https://charges.launchlabs.ai/api/deal_invoices?api_token=TOKEN&api_secret=SECRET&billing_period=2026-03-01"
```

---

## Errors

### 401 Unauthorized

Returned when auth fails.

### 404 Not Found

Possible on `/api/invoices/:id` if token is not found.
