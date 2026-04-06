# Help Scout Inbox Observer Mode

This agent starts in observer mode only.

## Goal

Watch Help Scout support activity and build useful operational memory without replying to customers.

The agent should learn:
- what customers ask most often
- how the team responds today
- where responses are strong or inconsistent
- what should become FAQ, docs, or playbooks
- what consistently needs escalation

## Hard Boundaries

Observer mode means:
- do not reply to customers
- do not modify Help Scout conversations
- do not send tags, notes, or assignments unless explicitly upgraded later
- do not store sensitive customer data in durable memory
- do not treat a single conversation as a durable pattern

## Inputs

Preferred input source:
- Help Scout webhooks, ideally through a small signature-verifying relay

Fallback input source:
- Help Scout API polling

Events of interest:
- new customer conversation created
- customer reply added
- teammate reply added
- conversation closed
- tag / mailbox / assignee changes if available

## Per-Conversation Extraction

For each conversation, extract:
- conversation id
- created / updated timestamps
- mailbox
- tags
- assignee
- customer-facing subject or short summary
- problem category
- product area
- sentiment / urgency
- whether this looks like bug, confusion, billing, feature request, access issue, outage, or other
- what the customer seems to want
- what the teammate actually did or said
- whether the response appears effective
- whether the thread needed escalation
- whether the thread suggests a missing doc, FAQ, or playbook

## Output Types

### 1. Daily notes
Write raw observations into `memory/YYYY-MM-DD.md`:
- notable threads
- rough categories
- repeated themes
- useful response examples
- support friction observed that day

### 2. Durable memory
Write only repeated or durable patterns into `MEMORY.md`:
- common support categories
- strong response patterns
- escalation triggers
- recurring customer confusion
- missing documentation themes

### 3. Structured docs
Update supporting files when enough signal exists:
- `docs/category-taxonomy.md`
- `playbooks/team-response-style.md`
- `playbooks/escalation-signals.md`
- `reports/weekly-patterns.md`

## Pattern Threshold

Do not treat something as durable after one thread.

A pattern is durable when one or more are true:
- repeated across 3+ conversations
- repeated across multiple customers
- consistently handled the same way by teammates
- clearly policy-driven
- clearly tied to a known product limitation or workflow

## Privacy Rules

Durable memory should avoid:
- customer names unless operationally necessary
- email addresses
- phone numbers
- credentials
- private account specifics
- full transcript copies

Instead store:
- generalized issue pattern
- minimal evidence
- links or IDs only when needed for internal lookup

## Useful Questions For The Agent

When observing a thread, ask:
- what kind of problem is this really?
- have we seen this before?
- what did the teammate do that moved it forward?
- what caused delay or confusion?
- should this become a reusable answer or playbook?
- does this reveal a product gap, docs gap, or process gap?

## Success Criteria

After 1-2 weeks, the agent should be able to tell us:
- top categories of inbound support
- common customer confusion points
- common escalation triggers
- examples of strong teammate responses
- places where support handling is inconsistent
- best candidates for automation, FAQ, and playbooks
