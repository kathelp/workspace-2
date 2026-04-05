# Secrets Handling

This workspace uses a local-first secrets pattern.

## Rules

- Never commit real secrets to git.
- Never store API keys in `USER.md`, `MEMORY.md`, `SOUL.md`, `TOOLS.md`, or skill files.
- Use `.env` for local runtime secrets when needed.
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
You have two good local runtime options.

#### Option A - Plain local `.env`
Use `/Users/kat/.openclaw/workspace/.env` for secrets needed on this machine.

Example:

```bash
cp .env.example .env
```

Then fill in the values manually.

#### Option B - 1Password CLI, recommended
Use 1Password references in `/Users/kat/.openclaw/workspace/.env.1password` and inject values at runtime.

Example setup:

```bash
cp .env.1password.example .env.1password
```

Then replace the example vault and item paths as needed.

Run commands with just-in-time secret injection:

```bash
scripts/with-secrets <command>
```

Example:

```bash
scripts/with-secrets openclaw status
```

This wrapper uses:

```bash
op run --env-file=.env.1password -- <command>
```

## 1Password CLI setup

Install the CLI:

```bash
brew install 1password-cli
```

Sign in:

```bash
op signin
```

If the 1Password desktop app is installed, the CLI can usually integrate with it.

## Secret reference format

1Password references look like this:

```bash
op://Private/OpenClaw Workspace/openai_api_key
```

These are references to secrets, not the secret values themselves.

## What not to do

Do not:
- paste secrets into chat unless absolutely necessary
- commit `.env`
- commit `.env.1password` unless you are comfortable exposing vault/item names
- store raw secrets in markdown docs
- check in JSON credential exports
- store long-lived secrets in memory files
- print secrets in shell output or logs

## Suggested workflow

1. Create or retrieve a credential in 1Password.
2. Add a reference to `.env.1password`, or place the value in `.env` if needed.
3. Run tools through `scripts/with-secrets` when using 1Password CLI.
4. Rotate the credential in 1Password if it leaks.

## Naming convention

Use uppercase env vars, for example:
- `OPENAI_API_KEY`
- `GITHUB_TOKEN`
- `TODOIST_API_TOKEN`
- `DISCORD_BOT_TOKEN`

## Files in this workspace

Committed:
- `.env.example`
- `.env.1password.example`
- `docs/secrets.md`
- `scripts/with-secrets`

Local only:
- `.env`
- `.env.1password`

## Optional future upgrades

If this grows messy, upgrade later to:
- `direnv` for per-directory loading
- macOS Keychain for machine-local retrieval
- more targeted wrapper scripts for common services
