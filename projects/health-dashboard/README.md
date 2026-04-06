# Health Dashboard

File-based accountability dashboard for Garrett. Tracks daily health metrics against race-day goals. No database, no cloud dependency, no nonsense.

**Race goal:** Tar Heel 10 Miler — April 18, 2026

---

## Quick Start

### 1. Serve the dashboard locally

Browsers block `fetch()` from `file://` URLs, so you need a local HTTP server.

```bash
cd /path/to/health-dashboard
python3 -m http.server 8080
```

Then open: **http://localhost:8080/dashboard/**

Refresh the page anytime to see updated data.

---

### 2. Sync Oura data

#### First-time setup — store your Oura token

1. Go to https://cloud.ouraring.com/personal-access-tokens and create a personal access token.
2. Store it in macOS Keychain:

```bash
security add-generic-password -a oura -s OURA_API_TOKEN -w <your_token>
```

#### Run the sync

```bash
# Sync last 14 days (default)
python3 scripts/sync_oura.py

# Sync last 30 days
python3 scripts/sync_oura.py 30

# Preview what would change without saving
python3 scripts/sync_oura.py --dry-run
```

The script fetches:
- **Sleep score** — daily sleep quality (0–100)
- **Readiness score** — recovery readiness (0–100)
- **Resting heart rate** — from readiness contributors (most accurate)
- **HRV** — average HRV from individual sleep sessions (ms)
- **Time in bed** — computed from sleep session start/end timestamps
- **Steps** — from daily activity

It **never overwrites** fields you've manually set (weight, protein, run/lift, notes, etc.).

#### Optional: auto-sync via cron

```bash
# Edit crontab
crontab -e

# Add this line to sync every morning at 7 AM:
0 7 * * * cd /path/to/health-dashboard && python3 scripts/sync_oura.py >> /tmp/oura-sync.log 2>&1
```

---

### 3. Log manual data

Edit `data/health-data.json` directly. The entry format:

```jsonc
{
  "date": "2026-03-11",        // YYYY-MM-DD — required, unique
  "weightLbs": 193.5,          // weigh in each morning, null if skipped
  "sleepScore": 82,            // auto-filled by Oura sync
  "readinessScore": 88,        // auto-filled by Oura sync
  "restingHeartRate": 52,      // auto-filled by Oura sync
  "hrv": 48.2,                 // auto-filled by Oura sync (ms)
  "timeInBedHours": 7.5,       // auto-filled by Oura sync
  "inBedBy10": true,           // manual: were you in bed by 10 PM?
  "upBy6": true,               // manual: up by 6 AM?
  "proteinGrams": 190,         // manual: log daily protein
  "runMiles": 4.2,             // manual: 0 if no run, distance if yes
  "liftDone": true,            // manual: true/false
  "steps": 8432,               // auto-filled by Oura sync
  "raccoonIncident": null,     // manual: true if a raccoon ruined your day
  "notes": "Long run, felt good"
}
```

**Tip:** Add today's entry at the bottom of the `entries` array. The dashboard sorts by date automatically.

---

## Scoring Model

The dashboard calculates a **daily score (0–100%)** based on available data. Categories are only scored if data is present — missing fields reduce the possible denominator but don't penalize you for having an incomplete day.

| Category | Max Points | How it's scored |
|---|---|---|
| Sleep | 30 | `(sleepScore / 100) × 30` |
| Recovery | 25 | `(readinessScore / 100) × 25` |
| Exercise | 30 | Run day: +15 pts · Lift day: +15 pts |
| Protein | 15 | `min(logged / target, 1) × 15` |
| Schedule | 10 | Bed by 10: +5 pts · Up by 6: +5 pts |

**Score = earned ÷ possible × 100%**

Color thresholds:
- **Green (80%+):** On track
- **Yellow (60–79%):** Acceptable, room to improve
- **Red (<60%):** Below standard

The 7-day trend chart shows daily scores so you can spot patterns. To get a full denominator (all 100 points possible), you need Oura data synced + protein logged + sleep schedule logged.

---

## File Structure

```
health-dashboard/
├── README.md                  # this file
├── dashboard/
│   └── index.html             # single-file dashboard (HTML + CSS + JS)
├── scripts/
│   └── sync_oura.py           # Oura API sync script
└── data/
    └── health-data.json       # all data lives here
```

Everything is plain files. Back up `data/health-data.json` regularly (commit to git, iCloud, etc.).

---

## Targets

| Metric | Target |
|---|---|
| Weight | 180 lbs |
| Protein | 180g/day |
| Runs | 3×/week |
| Lifts | 3×/week |
| Bedtime | 10 PM |
| Wake | 6 AM |

**Non-negotiables:** Exercise and sleep. If the data says otherwise, fix it.

---

## Maintenance

- **Add new days manually** by appending to the `entries` array in `health-data.json`.
- **Run Oura sync** after any missed days to backfill Oura metrics.
- **Update targets** by editing `profile.goals` in `health-data.json`. The dashboard reads all values from the profile — no code changes needed.
- **The dashboard is a single HTML file** — edit `dashboard/index.html` to change layout, scoring weights, or color thresholds.

---

## Known Gaps

- `inBedBy10` / `upBy6` require manual logging. Could be derived from `bedtime_start` timestamps in `health-data.json` in a future iteration.
- No automated backup — commit `data/health-data.json` to git or sync it with iCloud.
- `raccoonIncident` is a first-class tracked field. Use accordingly.
