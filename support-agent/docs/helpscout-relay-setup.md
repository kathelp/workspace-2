# Help Scout Relay Setup

This relay verifies Help Scout webhook signatures, normalizes the payload, and forwards observer events to OpenClaw.

## Files

- `scripts/helpscout_relay.rb`
- `scripts/Gemfile`

## Why this exists

Help Scout signs webhook requests with `X-HelpScout-Signature`.
OpenClaw hooks are good for routing, but signature verification is cleaner in a tiny relay in front.

## Required env vars

- `HELPSCOUT_WEBHOOK_SECRET`
- `OPENCLAW_HOOK_TOKEN`

## Optional env vars

- `PORT` - default `8789`
- `BIND` - default `127.0.0.1`
- `OPENCLAW_HOOK_URL` - default `http://127.0.0.1:18789/hooks/agent`
- `TARGET_AGENT_ID` - default `support`
- `LOG_JSON` - `1` for JSON logs

## Install

From `support-agent/scripts/`:

```bash
bundle install
```

## Run

```bash
HELPSCOUT_WEBHOOK_SECRET=... \
OPENCLAW_HOOK_TOKEN=... \
PORT=8789 \
BIND=127.0.0.1 \
ruby helpscout_relay.rb
```

## Help Scout webhook target

Point Help Scout at:

```text
http://YOUR-HOST:8789/helpscout
```

For real deployment, use HTTPS or put it behind a trusted reverse proxy / tunnel.

## What it forwards to OpenClaw

It sends a request to `/hooks/agent` with:
- `agentId: support`
- `sessionKey: hook:helpscout:<conversationId>`
- `deliver: false`

So the support agent stays internal and observer-only.

If you later want the relay to forward to a mapped path like `/hooks/helpscout` instead, the draft include file `hooks.include.json5` is ready as a starting point.

## Recommended first event subscriptions

- `convo.created`
- `convo.customer.reply.created`
- `convo.agent.reply.created`
- `convo.status`
- `convo.tags`
- `convo.assigned`

## Security notes

- Verify Help Scout signature before forwarding anything
- Keep `OPENCLAW_HOOK_TOKEN` private
- Prefer running the relay on a private host behind HTTPS
- Do not expose OpenClaw directly to arbitrary webhook traffic unless you really mean to
