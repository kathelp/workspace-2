# TOOLS.md - Local Notes

## Todoist
- **Token file:** `.env.todoist`
- **API base:** `https://api.todoist.com/api/v1`
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

## Proton Mail (Personal)
- **Account:** rgroach@pm.me
- **Access:** Proton Mail Bridge -> IMAP on localhost:1143 (STARTTLS)
- **Creds:** macOS Keychain -> `PROTON_BRIDGE_PASSWORD` (account: rgroach@pm.me)
- **Folders of note:** INBOX, Folders/github, Folders/gmail
- **Requires:** Proton Mail Bridge running (`/Applications/Proton Mail Bridge.app`)

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
- **Vault location:** `/Users/kat/Documents/obsidian/G`
- **Sync script:** `scripts/obsidian-sync.sh` - syncs all workspace .md files with backlinks

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
