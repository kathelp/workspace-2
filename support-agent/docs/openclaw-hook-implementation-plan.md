# OpenClaw Hook Implementation Plan for Help Scout

## Phase 1 - direct webhook to hook mapping

Use Help Scout webhooks to POST the conversation object directly into OpenClaw.

### Path
- OpenClaw hook endpoint: `/hooks/helpscout`

### Agent target
- `support`

### Session model
- one session per Help Scout conversation id

### Delivery
- `deliver: false`
- internal observer only

## Limitation

OpenClaw hooks can route and template payloads, but native hook config is not designed to validate Help Scout HMAC signatures by itself.

That means the first serious production design should be one of these:

### Option A - small verifier relay in front of OpenClaw
A tiny service receives Help Scout webhooks, verifies `X-HelpScout-Signature`, normalizes payload, then forwards a trusted request into OpenClaw hooks.

This is the cleaner production design.

### Option B - accept gateway hook token only
Rely on OpenClaw hook token and network controls without verifying Help Scout HMAC directly.

This is simpler but weaker. Fine for local prototyping, not my favorite for production.

## Recommended Production Design

1. Help Scout webhook hits small verifier service
2. verifier checks HMAC-SHA1 signature against raw body
3. verifier extracts event type from `X-HelpScout-Event`
4. verifier normalizes payload into a smaller JSON shape
5. verifier forwards to OpenClaw `/hooks/agent` or mapped `/hooks/helpscout`
6. OpenClaw routes to `support` agent

## Normalized Payload Shape

Suggested normalized JSON forwarded to OpenClaw:

```json
{
  "source": "helpscout",
  "event": "convo.customer.reply.created",
  "conversationId": 12345,
  "conversationNumber": 981,
  "mailboxId": 12,
  "status": "active",
  "subject": "Cannot log in",
  "preview": "I still can't access the dashboard",
  "sourceType": "email",
  "sourceVia": "customer",
  "createdAt": "2026-03-14T15:00:00Z",
  "updatedAt": "2026-03-14T15:05:00Z",
  "assigneeEmail": "agent@company.com",
  "primaryCustomerEmail": "customer@example.com",
  "tags": ["login", "urgent"]
}
```

## Why Normalize

Normalization gives us:
- smaller prompts
- less customer data retained
- less brittle templates
- easier future migration to another machine or service

## Immediate Next Step

Prototype with raw webhook payloads if you want speed.
But if you want durability and security, build the tiny verifier relay before going live.
