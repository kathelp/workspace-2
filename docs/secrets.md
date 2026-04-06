# Secrets Handling

This workspace uses a simple local-first secrets pattern.

## Recommended model

- **1Password** is the source of truth.
- **`.env`** is the local runtime file on this machine.
- Real secrets never go in git, memory files, or docs.

This is a pragmatic setup for OpenClaw and local agent workflows.

## Rules

- Never commit real secrets to git.
- Never store API keys in `USER.md`, `MEMORY.md`, `SOUL.md`, `TOOLS.md`, or skill files.
- Use `.env` for local runtime secrets.
- Commit only `.env.example` with blank placeholders.
- Keep the real values in 1Password and copy them into `.env` when needed.

## Where secrets should live

### Source of truth
Use 1Password for:
- API keys
- bot tokens
- recovery codes
- SSH notes
- service account metadata

### Local runtime
Use `/Users/kat/.openclaw/workspace/.env` for workspace-local secrets.

Create it with:

```bash
cd /Users/kat/.openclaw/workspace
cp .env.example .env
```

Then fill in the values manually from 1Password.

For OpenClaw service-level config, use:

`/Users/kat/.openclaw/.env`

That file should contain any environment variables referenced by `/Users/kat/.openclaw/openclaw.json`.

## OpenClaw wrapper

If `openclaw.json` uses environment variable references like `${DISCORD_BOT_TOKEN}` or `${OPENCLAW_GATEWAY_TOKEN}`, load them through the wrapper script:

```bash
/Users/kat/.openclaw/workspace/scripts/openclaw-gateway-with-env restart
/Users/kat/.openclaw/workspace/scripts/openclaw-gateway-with-env status
```

The wrapper sources:

`/Users/kat/.openclaw/.env`

before calling:

```bash
openclaw gateway <command>
```

## Suggested workflow

1. Create or update a credential in 1Password.
2. Copy the current value into `.env` locally.
3. For OpenClaw config-backed service secrets, also place the needed values in `/Users/kat/.openclaw/.env`.
4. Restart any tool or process that needs the updated value.
5. If a secret leaks, rotate it in 1Password and update the local env file.

## What not to do

Do not:
- paste secrets into chat unless absolutely necessary
- commit `.env`
- store raw secrets in markdown docs
- check in JSON credential exports
- store long-lived secrets in memory files
- print secrets in shell output or logs

## Naming convention

Use uppercase env vars, for example:
- `OPENAI_API_KEY`
- `GITHUB_TOKEN`
- `TODOIST_API_TOKEN`
- `DISCORD_BOT_TOKEN`
- `OPENCLAW_GATEWAY_TOKEN`

## Files in this workspace

Committed:
- `.env.example`
- `docs/secrets.md`
- `.gitignore`
- `scripts/openclaw-gateway-with-env`

Local only:
- `.env`
- `/Users/kat/.openclaw/.env`

## Security tradeoff

This setup stores plaintext secrets in local `.env` files on the machine.
That is acceptable here if:
- the Mac is trusted
- FileVault is enabled
- the account is protected well
- env files stay out of git

## Optional future upgrades

If this grows messy later, upgrade to:
- `direnv` for per-directory loading
- macOS Keychain for machine-local retrieval
- 1Password CLI for targeted just-in-time injection
