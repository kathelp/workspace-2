# Workflow Review Plan

_Date: 2026-04-06_
_Owner: Kat_

## Why this exists

Garrett's bottleneck is not lack of tools. It is that too many low-signal inputs still compete with the few things that actually require judgment, decision-making, or follow-through.

The goal of this plan is simple:
- reduce daily attention fragmentation
- convert noise into summaries
- surface only high-signal decisions
- connect inbox + calendar + notes into a usable operating system

## What I observed

### Inbox pattern
The inbox still contains a large volume of:
- Mercury ACH notifications
- Intuit / payroll receipts and reminders
- finance status emails
- newsletters and promotional mail
- recruiting / jobs spam
- vendor marketing

The actionable items are comparatively rare, but high value when they appear:
- policy / fee changes
- reconnect / compliance tasks
- direct human follow-up
- relationship obligations
- true exceptions in finance or operations
- Banyan and other genuinely relevant business communication

### Workflow pattern
Current docs and notes already point to the real weakness:
- triage consistency
- follow-up consistency
- strategic thinking living separately from daily operational inputs

That means the problem is not understanding what matters. The problem is routing and review discipline.

### Calendar pattern
Calendar review could not be completed because the current Google setup appears to be missing calendar scope permissions.

That is not just a tooling hiccup. It means the system cannot reliably support planning and prep right when it matters.

## Core diagnosis

The current workflow asks Garrett to manually distinguish between:
- noise
- useful reference material
- operational exceptions
- genuine decisions
- actual follow-up work

That is a bad use of executive attention.

The system should do most of that sorting before Garrett ever sees it.

## Design principles

1. Garrett should not be the router
2. Routine finance activity should become summaries, not interruptions
3. Human follow-up and decisions should be isolated into a short queue
4. Calendar should drive prep, not just reflect commitments
5. Tasks should only exist when there is real action, owner, or deadline
6. Weekly review should prune drift before it compounds

## Target workflow

### Lane 1: Decision / reply / relationship
This lane includes:
- emails that need Garrett's judgment
- direct replies from important humans
- Banyan communication
- partner / customer communication
- approvals, commitments, and deadlines
- relationship obligations

Output:
- surfaced quickly
- summarized clearly
- converted to task only if actual follow-up is required

### Lane 2: Finance / compliance / ops
This lane includes:
- Mercury notifications
- payroll notifications
- QuickBooks receipts
- account charges and deposits
- vendor admin
- compliance and reconnect tasks

Output:
- routine items batched into daily or weekly summaries
- only exceptions escalated individually

Exception examples:
- overdue taxes
- failed or suspicious withdrawals
- account reconnect requirements
- fee changes
- balances, payment failures, or compliance issues

### Lane 3: Noise / read later
This lane includes:
- newsletters
- marketing blasts
- recruiting spam
- generic updates
- low-value vendor outreach

Output:
- auto-labeled
- archived or moved to read-later review
- no immediate attention required

## Concrete improvements

### 1. Gmail lane system
Create and use labels such as:
- `kat/high-signal`
- `kat/reply-needed`
- `kat/finance-routine`
- `kat/finance-exception`
- `kat/read-later`

Desired behavior:
- high-signal and reply-needed stay visible
- finance-routine gets summarized, not escalated
- finance-exception gets surfaced quickly
- read-later is removed from decision space

### 2. Decision queue
Maintain one short queue containing only things Garrett actually needs to decide.

Examples:
- approve or respond
- choose direction
- accept / decline / RSVP
- handle relationship follow-up
- resolve exception item

This queue should stay short. If it gets long, routing is failing.

### 3. Daily digest
A short daily digest should include only:
- reply-needed items
- decision-needed items
- deadlines
- operational exceptions
- tomorrow's calendar prep

It should not include every routine financial event.

### 4. Weekly finance digest
Instead of interrupting the week with drip-by-drip notifications, finance/admin updates should be condensed into a single digest, including:
- notable deposits
- notable withdrawals
- taxes / payroll anomalies
- items requiring review
- compliance / reconnect reminders

### 5. Waiting-on tracker
Create a lightweight list for external dependencies and follow-up threads.

Use it for:
- important unanswered emails
- pending approvals
- partner replies
- vendor tasks not yet resolved

This prevents important threads from disappearing after first review.

### 6. Calendar as prep system
Once calendar scope is fixed, the calendar workflow should produce two useful views:
- next 48 hours: hard commitments
- next 7 days: meetings requiring prep

For prep-needed meetings, capture:
- purpose
- owner
- required document / agenda
- next step before meeting

If a meeting has no prep artifact and no clear purpose, it probably should not consume attention.

### 7. Protected attention blocks
Default operating rhythm:
- morning: 20-30 minute triage block
- later in day: 20 minute admin cleanup block
- everything else protected for execution, revenue, product, or leadership work

This matters because inbox spillage expands to fill the day if not boxed in.

## Execution plan

## Phase 1 - This week

### Goal
Create routing clarity and remove obvious attention leaks.

### Actions
1. Fix Google Calendar auth scope so calendar review actually works.
2. Implement Gmail labels and filters for the lane system.
3. Tighten agent triage rules so routine finance messages are summarized, not surfaced one by one.
4. Tighten Todoist creation rules:
   - only create tasks when there is a real decision, deadline, reply, approval, or concrete follow-through
5. Define the first version of the decision queue.

### Success criteria
- fewer inbox items compete for attention
- routine finance activity no longer surfaces individually unless exceptional
- only genuinely actionable items become tasks

## Phase 2 - Next 7 days

### Goal
Replace raw inbox review with structured summaries.

### Actions
1. Build a daily digest for:
   - reply-needed
   - decision-needed
   - deadlines / exceptions
   - calendar prep
2. Build a weekly finance digest.
3. Create a lightweight waiting-on tracker tied to meaningful email threads.
4. Review whether any recurring senders should be fully downgraded or filtered harder.

### Success criteria
- Garrett reads a short decision summary, not a pile of notifications
- follow-up risk is reduced
- admin review becomes batchable

## Phase 3 - Ongoing operating cadence

### Goal
Make the workflow self-maintaining.

### Cadence
- Daily morning: inbox + calendar review with only high-signal output
- Daily midday or afternoon: short decision queue review
- Weekly: workflow review and stale follow-up audit
- Monthly: prune recurring noise, review filters, and tighten rules

### Success criteria
- inbox becomes a collection surface, not a work surface
- important follow-up no longer leaks
- calendar prep becomes predictable
- Garrett spends more time on real work and fewer micro-decisions

## Blunt summary

The main fix is not "be more organized."

The main fix is to stop escalating trivia to Garrett.

This workflow should aggressively route noise away, compress routine information into summaries, and preserve Garrett's attention for decisions, relationships, and execution.

## Recommended next implementation order

1. Fix calendar auth
2. Implement Gmail lane labels and filters
3. Add daily decision digest
4. Add weekly finance digest
5. Add waiting-on tracker
6. Review results after one week and tighten further
