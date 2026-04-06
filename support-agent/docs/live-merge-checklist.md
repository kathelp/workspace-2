# Live Merge Checklist

Use this when you want to make the support observer real.

## 1. Real config changes

Merge into live OpenClaw config:
- `support-agent/support-agent.include.json5`
- `support-agent/hooks.include.json5`

Or copy the relevant blocks into your existing `~/.openclaw/openclaw.json`.

## 2. Real secrets

Set real values for:
- `OPENCLAW_HOOK_TOKEN`
- `HELPSCOUT_WEBHOOK_SECRET`

Do not store them in workspace markdown files.

## 3. Start order

1. Gateway running with hooks enabled
2. Relay running
3. Help Scout webhook pointed at relay URL

## 4. Help Scout event subscriptions

Start with only:
- conversation created
- customer reply created
- agent reply created
- status updated
- tags updated
- assigned

## 5. First safety pass

Confirm:
- no customer-facing output
- no Help Scout mutations
- no uncontrolled durable storage of customer-specific data
- session isolation per conversation id

## 6. Only after that

Then consider:
- weekly summary output
- internal notifications
- suggested drafts
- suggested FAQ / playbook updates
