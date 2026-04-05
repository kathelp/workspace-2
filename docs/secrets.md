# Secrets Handling

This workspace uses a local-first secrets pattern.

## Rules

- Never commit real secrets to git.
- Never store API keys in `USER.md`, `MEMORY.md`, `SOUL.md`, `TOOLS.md`, or skill files.
- Use `.env` for local runtime secrets.
- Commit only `.env.example` with blank placeholders.
- Treat password manager entries as the source of truth.

## Where secrets should live

### Source of truth
Use a password manager like 1Password or Bitwarden for:
- API keys
- bot tokens
- recovery codes
- SSH notes
- service account metadata

### Local runtime
Use `/Users/kat/.openclaw/workspace/.env` for secrets needed on this machine.

Example:

```bash
cp .env.example .env
```

Then fill in the values manually.

## What not to do

Do not:
- paste secrets into chat unless absolutely necessary
- commit `.env`
- store raw secrets in markdown docs
- check in JSON credential exports
- store long-lived secrets in memory files

## Suggested workflow

1. Create or retrieve a credential in the password manager.
2. Add the needed value to `.env` locally.
3. Reference the environment variable in apps and scripts.
4. Rotate the credential in the password manager if it leaks.

## Naming convention

Use uppercase env vars, for example:
- `OPENAI_API_KEY`
- `GITHUB_TOKEN`
- `TODOIST_API_TOKEN`
- `DISCORD_BOT_TOKEN`

## Optional next step

If this grows messy, upgrade later to:
- `direnv` for per-directory loading
- macOS Keychain for machine-local retrieval
- 1Password CLI for just-in-time secret injection
