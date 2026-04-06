# Help Scout Webhook Plan

## Objective

Ingest Help Scout conversation events into the support observer agent through OpenClaw hooks.

## Preferred Flow

1. Help Scout sends webhook event
2. Gateway receives it at a dedicated hook path
3. Hook mapping routes it to agent `support`
4. Agent summarizes the event in observer mode
5. Agent updates daily notes and durable memory when warranted

## Desired Event Types

Prioritize webhook coverage for:
- conversation created
- customer replied
- teammate replied
- conversation closed
- tag changes
- assignment changes

If Help Scout emits more granular or differently named events, map those into these logical buckets.

## Hook Design

Suggested OpenClaw hook path:
- `/hooks/helpscout`

Suggested session strategy:
- session key per Help Scout conversation id
- example: `hook:helpscout:<conversationId>`

Why:
- keeps each support thread isolated
- lets the agent accumulate context per conversation
- avoids mixing unrelated customer issues

## Message Template Shape

Each inbound hook payload should be normalized into a compact message containing:
- event type
- conversation id
- mailbox
- assignee
- tags
- customer summary
- latest message summary
- actor type: customer or teammate
- timestamps

The agent should not receive the raw entire webhook blob if a smaller normalized payload is enough.

## Data Handling Rules

- Keep raw payload handling minimal
- Normalize before prompting when possible
- Do not duplicate full transcripts into durable memory
- Prefer storing conversation ids over sensitive customer details

## Fallback Plan

If webhook payloads are too sparse, inconsistent, or annoying:
- use webhooks as a trigger
- fetch full conversation details from Help Scout API
- then send a normalized summary into the support agent

## Good First Version

First version should only do:
- receive event
- verify Help Scout authenticity before trusting it
- classify thread
- append daily notes
- identify possible recurring pattern
- never send customer-facing output

## Important Real-World Note

Help Scout includes an `X-HelpScout-Signature` header for webhook verification.
That signature is HMAC-SHA1 over the raw request body, base64-encoded, using the webhook secret.

OpenClaw hooks are good for routing, but signature verification is best handled by a tiny verifier relay in front of OpenClaw if you want a production-grade setup.

## Later Upgrades

After observer mode proves useful, consider:
- internal summaries to a channel
- suggested tags
- suggested reply drafts
- escalation detection
- docs / FAQ recommendations
