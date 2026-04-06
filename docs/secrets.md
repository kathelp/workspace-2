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
Use `/Users/kat/.openclaw/workspace/.env` for secrets needed on this machine.

Create it with:

```bash
cp .env.example .env
```

Then fill in the values manually from 1Password.

## Suggested workflow

1. Create or update a credential in 1Password.
2. Copy the current value into `.env` locally.
3. Restart any tool or process that needs the updated value.
4. If a secret leaks, rotate it in 1Password and update `.env`.

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

## Files in this workspace

Committed:
- `.env.example`
- `docs/secrets.md`
- `.gitignore`

Local only:
- `.env`

## Security tradeoff

This setup stores plaintext secrets in `.env` on the local machine.
That is acceptable here if:
- the Mac is trusted
- FileVault is enabled
- the account is protected well
- `.env` stays out of git

## Optional future upgrades

If this grows messy later, upgrade to:
- `direnv` for per-directory loading
- macOS Keychain for machine-local retrieval
- 1Password CLI for targeted just-in-time injection
