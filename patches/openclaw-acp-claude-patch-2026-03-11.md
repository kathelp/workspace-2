# OpenClaw ACP Claude Patch - 2026-03-11

## Why this exists
Claude Code ACP spawns were failing from OpenClaw even though:
- `claude` was installed and on PATH
- `acpx` was enabled
- ACP config was enabled and pointed at `claude`

The initial error was:

`spawnedBy is only supported for subagent:* sessions`

## Root cause
In OpenClaw 2026.3.8, the ACP `sessions_spawn({ runtime: "acp" })` flow was patching newly created ACP sessions with:

```js
spawnedBy: requesterInternalKey
```

But gateway session validation only allows `spawnedBy` on `subagent:*` session keys.
ACP session keys look like:

```text
agent:claude:acp:<uuid>
```

So the ACP spawn path was structurally invalid and failed before Claude could run.

## Files patched
The live bundle code was duplicated across several built files under:

`/opt/homebrew/lib/node_modules/openclaw/dist`

The effective fix was to remove this line from the ACP spawn path everywhere it appeared:

```js
spawnedBy: requesterInternalKey,
```

Patched bundles included:
- `reply-DeXK9BLT.js`
- `plugin-sdk/reply-UQ7w3uFC.js`
- `plugin-sdk/dispatch-F_Zbttj6.js`
- `plugin-sdk/dispatch-BCrTbhbt.js`
- `plugin-sdk/dispatch-CJdFmoH9.js`
- `plugin-sdk/dispatch-CM4tRXYq.js`
- `plugin-sdk/dispatch-DwgTiP0N.js`
- `pi-embedded-jHMb7qEG.js`
- `pi-embedded-CrsFdYam.js`
- `compact-D3emcZgv.js`

## Outcome after patch
After patching and restarting the gateway:
- ACP spawn no longer failed on `spawnedBy`
- Non-threaded Claude ACP runs started working
- Discord DM thread-bound ACP still failed at the binding layer

This suggests the patch fixed the ACP runtime regression, while Discord DM thread binding remains a separate limitation/problem.

## Second issue found
Claude still failed initially in ACP with:

`ACP_TURN_FAILED: acpx exited with code 1`

Root cause:
- Non-interactive Claude runs were picking up a bad `ANTHROPIC_API_KEY`
- `claude -p ...` failed with `Invalid API key · Fix external API key`
- `env -u ANTHROPIC_API_KEY claude -p "say hi"` worked

Garrett fixed this in `.zshrc`.

## Practical notes
- If ACP breaks again after an OpenClaw upgrade, re-check whether this `spawnedBy` regression has returned.
- If Claude works interactively but not through ACP, check for stale env vars first, especially `ANTHROPIC_API_KEY`.
- Discord DM thread-binding for ACP appears separate from the core ACP runtime path.

## Suggested upstream fix
OpenClaw should not attach `spawnedBy` metadata to ACP session keys unless gateway validation explicitly supports ACP session types.
A better long-term fix is either:
1. allow `spawnedBy` for ACP sessions, or
2. stop setting it for ACP sessions and track requester ownership some other way.
