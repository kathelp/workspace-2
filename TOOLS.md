# TOOLS.md - Local Notes

## Todoist
- **Token file:** `.env.todoist`
- **API base:** `https://api.todoist.com/api/v1`
- **Email triage helper:** `scripts/gmail-todoist-triage.sh`
- **Projects:**
  - Inbox: `6g7Mf5J6p939RxX4`
  - Work: `6g7Mg937PG4P9g6V`
  - Follow-up: `6g7Mg93mCQHHwXmx`
  - Personal: `6g7Mg96MfRc5G2RQ`
- **Routing rules:**
  - `garrett@launchlabs.ai` emails -> **Work** project
  - Emails from real contacts/relationships needing a reply -> **Follow-up** project
  - **Cold outreach** (partnerships, sales pitches, services from strangers) -> **ignore entirely**, do not create tasks
  - Everything else -> triage to appropriate project
- **Task format:**
  - Always include Gmail thread link in description: `https://mail.google.com/mail/u/0/#inbox/<threadId>`

## Gmail (Work)
- **Primary inbox:** `garrett@launchlabs.ai`
- **Access tool:** `gog`
- **OAuth client JSON:** `/Users/kat/Documents/client_secret_391113707787-0v4gptds6gqn0juadh29s6db0quehoui.apps.googleusercontent.com.json`
- **Default usage:** `source .env && GOG_ACCOUNT=garrett@launchlabs.ai gog gmail search 'in:inbox -label:kat/reviewed -label:kat/todo-created newer_than:14d' --max 25 --json --no-input`
- **Keyring backend:** `file` via `GOG_KEYRING_PASSWORD` in local `.env`
- **Review labels:** `kat/reviewed`, `kat/todo-created`
- **Todoist triage:** `scripts/gmail-todoist-triage.sh`
- **Dry run:** `scripts/gmail-todoist-triage.sh 'in:inbox -label:kat/reviewed -label:kat/todo-created newer_than:14d'`
- **Create tasks:** `scripts/gmail-todoist-triage.sh 'in:inbox -label:kat/reviewed -label:kat/todo-created newer_than:14d' create`
- **Hourly runner:** `scripts/gmail-todoist-hourly.sh`

## TTS
- **Provider:** OpenAI (gpt-4o-mini-tts)
- **Voice:** Nova (female)
- **Mode:** tagged (voice when I choose, not every message)

## Notion (Launch Labs workspace)
- **Token:** macOS Keychain -> `NOTION_API_TOKEN` (account: launchlabs) + `.env.notion`
- **API version:** 2022-06-28
- **Agent Comms page:** `31ba1ae4-dc35-8005-b73f-e6b7eadc843c`
- **Routing:** Projects and substantial docs go here; ambiguous items -> Agent Comms page
- **Todoist is for short tasks only** - anything bigger goes to Notion

## Charges API (Billing)
- **Base URL:** `https://charges.launchlabs.ai`
- **Auth:** Query params `api_token` + `api_secret`
- **Token:** macOS Keychain -> `CHARGES_API_TOKEN` (account: launchlabs)
- **Secret:** macOS Keychain -> `CHARGES_API_SECRET` (account: launchlabs)
- **Endpoints:**
  - `GET /api/invoices` - usage-based invoices (currently returning 500)
  - `GET /api/invoices/:token` - single invoice by token
  - `GET /api/deal_invoices` - fixed rate + enterprise sale invoices
- **Docs:** `charges-api-docs.md` in workspace

## Pipedrive (CRM)
- **Token:** macOS Keychain -> `PIPEDRIVE_API_TOKEN` (account: launchlabs)
- **API base:** `https://api.pipedrive.com/v1`
- **Auth:** `?api_token=<token>` query param

## Cameras
- _(to be configured)_

## SSH
- _(to be configured)_

## Obsidian
- **Vault location:** `/Users/kat/Documents/gsync`
- **Workspace folder:** `/Users/kat/Documents/gsync/Kat Workspace`
- **Sync script:** `scripts/obsidian-sync.sh` - syncs workspace markdown files one-way into Obsidian

## Oura Ring
- **Token:** macOS Keychain -> `OURA_API_TOKEN` (account: oura)
- **API base:** `https://api.ouraring.com/v2`
- **Auth:** `Authorization: Bearer <token>` header
- **Key endpoints:**
  - `GET /usercollection/daily_sleep?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
  - `GET /usercollection/daily_activity?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
  - `GET /usercollection/daily_readiness?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
  - `GET /usercollection/heartrate?start_datetime=ISO&end_datetime=ISO`
  - `GET /usercollection/daily_spo2?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
  - `GET /usercollection/workout?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- **Discord channel:** #oura-ring (id: 1480736825558437918)
