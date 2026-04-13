# Email + Todoist Workflow Summary

_Date: 2026-04-07_

## Purpose

This document summarizes the current live workflow for Gmail review, Todoist task creation, digest generation, and related automation.

## Gmail review model

### Core rule
Processed email is tracked using Gmail labels, not read/unread state.

Primary labels:
- `kat/reviewed` - already processed, do not review again
- `kat/todo-created` - a Todoist task was created from this email
- `kat/finance-routine` - routine finance/admin mail that should be summarized, not escalated
- `kat/read-later` - newsletters, app alerts, and low-priority items

### Inbox triage query
Default inbox triage excludes already-processed mail:
- `in:inbox -label:kat/reviewed -label:kat/todo-created newer_than:14d`

This prevents duplicate review and duplicate Todo creation.

### Sent mail context review
Recent sent mail is also scanned so outbound context informs future triage.

Sent review query:
- `in:sent -label:kat/reviewed newer_than:14d`

Sent threads reviewed for context are labeled `kat/reviewed` so they are not scanned repeatedly.

## What gets surfaced

### High-signal / actionable
These can create Todoist items or require attention:
- Banyan emails
- scorecard / earnout-related Google doc comments
- direct human follow-up from known contacts
- relationship / reply-needed threads
- true exception-style finance or security problems

### Finance routine
These are reviewed, labeled, and summarized rather than escalated individually:
- Mercury
- QuickBooks / Intuit routine updates
- Stripe receipts / payment notices
- Pilot, Mailjet, PayPal, ZenBusiness, Accrue routine admin mail

Routine finance items should generally not become tasks unless they imply real action.

### Read later
These are low-priority and not treated as active work:
- newsletters
- vendor marketing
- product updates
- app alerts such as Airbrake
- generic recruiting / promo traffic

### Cold solicitations
Obvious cold outreach can be archived during triage instead of lingering in inbox.

## Todoist behavior

### Projects in use
- **Work** (`6g7Mg937PG4P9g6V`) - actionable work items
- **Follow-up** (`6g7Mg93mCQHHwXmx`) - reply-needed / relationship items
- **For Kat** (`6gJVwj7Vvqp7X9wF`) - tasks Garrett assigns directly to me

### Todo creation rules
A Todoist task should only be created when there is actual action, such as:
- a decision required
- a deadline
- a reply needed
- an approval needed
- concrete follow-through required

Routine notifications should not become tasks.

### Todo content format
Email-created Todoist tasks include:
- sender
- subject
- date
- Gmail thread ID
- direct Gmail thread link
- reason the task was created

## Todoist operating rules
- Check Todoist regularly
- If Garrett leaves an instruction in a Todoist comment, carry it out
- If Garrett adds a task in **For Kat**, treat it as mine to do
- If Garrett leaves a Todoist comment telling me to ignore, skip, remove, delete, or close a task, remove that task after I have seen it

## Frequency of checks

### Hourly inbox triage
Live cron schedule:
- `33 * * * * cd /Users/kat/.openclaw/workspace && ./scripts/gmail-todoist-hourly.sh`

This runs:
- inbox triage against unreviewed inbox mail
- sent-mail context review against unreviewed sent mail

### Email digests
Live cron schedule:
- `0 6 * * *` - digest run
- `0 12 * * *` - digest run
- `0 15 * * *` - digest run

Digest script:
- `scripts/gmail-digest.py`

### Daily memory sync
Live cron schedule:
- `15 6 * * * cd /Users/kat/.openclaw/workspace && ./scripts/daily-memory-sync.sh`

## Digest contents
Current digest is designed to post into Discord `#daily-digests`.

Target channel ID:
- `1491060915385405441`

Digest includes:
- actionable / high-signal items, when present
- Todo items created for Garrett, when those still map to active Todoist tasks
- finance routine summary
- application alerts summary, when present

Digest should only ask Garrett for more context when it is genuinely needed.

## Current delivery status
- Digest generation works
- Discord channel posting works via OpenClaw CLI message send
- Current posting path was manually validated to `#daily-digests`

## Key behavior notes
- Do not review emails twice once `kat/reviewed` is present
- Preserve `kat/todo-created` when tasks are created
- Use sent-mail review to improve context on active threads
- Prefer summary lanes over interruption for finance/admin noise
- Archive obvious cold solicitations when appropriate

## Relevant scripts
- `scripts/gmail-todoist-triage.sh`
- `scripts/gmail-todoist-hourly.sh`
- `scripts/gmail-digest.py`
- `scripts/obsidian-sync.sh`

## Source references
- Reviewed-label and task-context behavior: Source: memory/2026-04-06-cron-path.md#L146-L161
- Todoist standing policy: Source: memory/2026-04-07-todoist-policy.md#L26-L81
- Mercury routine-noise rule: Source: memory/2026-03-13.md#L1-L10
