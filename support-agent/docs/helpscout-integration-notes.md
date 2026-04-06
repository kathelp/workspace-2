# Help Scout Integration Notes

Based on Help Scout developer docs reviewed on 2026-03-14.

## What Help Scout Gives Us

Help Scout supports webhooks and the webhook payload for conversation events is the v2 Conversation object.

Useful webhook events for observer mode:
- `convo.created`
- `convo.customer.reply.created`
- `convo.agent.reply.created`
- `convo.status`
- `convo.tags`
- `convo.assigned`
- `convo.note.created`
- `convo.moved`
- `convo.merged`

Each webhook includes headers:
- `X-HelpScout-Event`
- `X-HelpScout-Signature`

The signature is an HMAC-SHA1 over the raw request body, base64-encoded, using the webhook secret.

## Why This Is Good For Us

This is enough to build a passive observer agent without polling as the primary path.

We can:
- receive the event
- verify it
- normalize the conversation data
- route it to the `support` agent
- maintain one OpenClaw session per Help Scout conversation id

## Recommended First-Version Event Scope

Start with only:
- `convo.created`
- `convo.customer.reply.created`
- `convo.agent.reply.created`
- `convo.status`
- `convo.tags`
- `convo.assigned`

Ignore the rest initially.

## Recommended Session Key

Use one session per Help Scout conversation:
- `hook:helpscout:<conversationId>`

That keeps context isolated and lets the agent watch a thread evolve.

## Conversation Fields Worth Normalizing

Useful fields from the conversation object include:
- `id`
- `number`
- `subject`
- `preview`
- `mailboxId`
- `status`
- `type`
- `source.type`
- `source.via`
- `createdAt`
- `userUpdatedAt`
- `customerWaitingSince.time`
- `assignee`
- `createdBy`
- `primaryCustomer`
- `tags`
- `customFields`
- `_embedded.threads` when available

## Authentication / Enrichment

Help Scout Inbox API v2 uses OAuth 2.
For an internal integration, Client Credentials flow appears to be the right fit.

API base:
- `https://api.helpscout.net/v2`

Use API enrichment only if the webhook payload turns out to be too sparse for real classification.

## First-Version Recommendation

Do not enrich with API calls yet unless necessary.
The webhook conversation object is probably enough to start classification and pattern logging.

## Sources
- Help Scout Developers: Webhooks
- Help Scout Developers: Inbox API 2.0
- Help Scout Developers: Get Conversation
- Help Scout Developers: Authentication
