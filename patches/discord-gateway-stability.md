# Discord Gateway Stability Patch

## Issue
https://github.com/openclaw/openclaw/issues/14703

Discord WebSocket zombie reconnect loop causes gateway instability.

## Root Cause Analysis
Three layers interact to create the loop:

1. **Carbon GatewayPlugin** (`@buape/carbon`) — handles WebSocket reconnects with exponential backoff.
   OpenClaw configures `maxAttempts: 50`, `baseDelay: 1000`, `maxDelay: 30000`.

2. **OpenClaw Channel Manager** (`server-channels.ts`) — auto-restarts failed channels.
   `MAX_RESTART_ATTEMPTS: 10`, exponential backoff 5s→5min.

3. **Health Monitor** (`channel-health-monitor.ts`) — checks every 5min, restarts unhealthy channels.
   Max 10 restarts/hour, cooldown between restarts.

**The loop**: When health monitor restarts a channel, it calls `resetRestartAttempts()`,
which resets the channel manager's counter. This means the 10-attempt limit never triggers
a permanent stop. Combined with Carbon's 50-attempt limit being reset on each fresh start,
you get an infinite restart cycle.

## Patches Applied
1. **Health monitor**: Reduced `maxRestartsPerHour` from 10 → 4 (circuit breaker)
2. **Channel restart policy**: Increased initial backoff from 5s → 15s, max from 5min → 10min
3. **Carbon reconnect**: Reduced `maxAttempts` from 50 → 10 (fail faster, let health monitor decide)

## Files Modified
- `dist/gateway-cli-C2ZZYgwu.js` — channel restart policy + health monitor defaults
- `dist/gateway-cli-CbAOelvx.js` — same (duplicate build artifact)
- `dist/reply-DeXK9BLT.js` — Carbon GatewayPlugin maxAttempts
- `dist/plugin-sdk/discord.js` — Carbon GatewayPlugin maxAttempts (plugin SDK copy)

## Re-apply After Updates
These patches modify compiled dist files and will be overwritten by `npm update`.
Run: `bash ~/.openclaw/workspace/patches/apply-discord-patch.sh`
