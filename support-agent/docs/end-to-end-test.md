# End-to-End Test Plan

This tests the full observer pipeline:

1. fake Help Scout webhook
2. Ruby verifier relay
3. OpenClaw hook endpoint
4. support agent session update

## Prerequisites

- OpenClaw gateway running
- support agent config merged into real config
- hooks enabled in real config
- relay env vars available

## Recommended env vars

```bash
export OPENCLAW_HOOK_TOKEN='replace-with-strong-token'
export HELPSCOUT_WEBHOOK_SECRET='replace-with-strong-secret'
export OPENCLAW_HOOK_URL='http://127.0.0.1:18789/hooks/agent'
export TARGET_AGENT_ID='support'
```

## 1. Install relay dependency

```bash
cd ~/.../support-agent/scripts
bundle install
```

## 2. Start the relay

```bash
cd ~/.../support-agent/scripts
HELPSCOUT_WEBHOOK_SECRET="$HELPSCOUT_WEBHOOK_SECRET" \
OPENCLAW_HOOK_TOKEN="$OPENCLAW_HOOK_TOKEN" \
OPENCLAW_HOOK_URL="$OPENCLAW_HOOK_URL" \
TARGET_AGENT_ID="$TARGET_AGENT_ID" \
ruby helpscout_relay.rb
```

Relay default listen address:
- `127.0.0.1:8789`

## 3. Send a fake Help Scout webhook

```bash
cd ~/.../support-agent/scripts
HELPSCOUT_WEBHOOK_SECRET="$HELPSCOUT_WEBHOOK_SECRET" \
ruby test_helpscout_relay.rb
```

Expected result:
- relay returns HTTP 202
- OpenClaw receives `/hooks/agent` call
- support agent gets a session key like `hook:helpscout:12345`
- no customer-facing message is sent

## 4. Validate in OpenClaw

Check that:
- a `support` agent session exists for the conversation
- daily note files were updated if the agent chose to write
- no outbound message was delivered

## Troubleshooting

### 401 invalid_signature
- `HELPSCOUT_WEBHOOK_SECRET` mismatch between sender and relay

### 502 openclaw_forward_failed
- wrong `OPENCLAW_HOOK_TOKEN`
- hooks not enabled
- gateway not running
- wrong `OPENCLAW_HOOK_URL`

### no useful memory updates
- expected on the first event sometimes
- the agent may choose not to write durable memory for one isolated thread
