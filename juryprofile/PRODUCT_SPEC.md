# JuryProfile — Product Specification

**Version:** 0.1 (MVP)
**Date:** 2026-03-08
**Status:** Draft
**Author:** Kat (AI) + Garrett (Product Owner)

---

## Related Documents

- [[sme-conversation-notes]] — Nov 2025 email thread between Garrett, Lauren Kulp, and Kelly Dagger with domain insights
- [[compliance/README]] — Compliance framework overview and data classification
- [[compliance/soc2/controls]] — SOC-2 Trust Service Criteria mapping
- [[compliance/iso27001/controls]] — ISO 27001 Annex A control mapping

## Guiding Principles

1. SOC-2 + ISO 27001 compliance tracking from day 1
2. API-first — all functionality documented and exposed via API
3. 37signals Rails design patterns using the `rails_ai_agents` framework
4. Marketing website maintained alongside the app (product narrative synced with features)
5. Customer-facing support docs maintained alongside features with external significance
6. **Full backend test coverage** — no feature ships without comprehensive tests (models, requests, services, policies, jobs)

---

## Vision

Democratize jury selection intelligence. Today, jury consultants charge $10K–$100K+ per case and still can't profile a full 1,000-name summons list. JuryProfile uses identity resolution and AI to profile every juror, score them against the case, and serve as a real-time co-pilot during voir dire — at a fraction of the cost.

## Strategic Context

JuryProfile contracts identity resolution from **Launch Labs** (Focal Graph), making it a natural distribution channel for Launch Labs' core product. Flat-rate identity data pricing makes the unit economics favorable at scale.

---

## Target Market

- **Primary:** Mid-size defense law firms
- **Secondary/Eventual:** BigLaw defense practices
- **User Personas:**
  - **Lead Attorney** — manages jury selection strategy, makes strike decisions
  - **Associate/Paralegal** — assists in courtroom, logs juror responses, handles case setup
  - **Firm Administrator** — manages billing, users, firm settings

---

## MVP Features

### 1. Case Setup

**Description:** Attorney creates a case by entering a PACER case number. The system pulls available docket data (nature of claims, parties, dollar amounts, industry, plaintiff/defendant details). Attorney can review and edit the case summary.

**Key Details:**
- PACER Case Locator API or CourtListener/RECAP as data source
- Extracted fields: case title, nature of suit, parties, claims, key dates, jurisdiction
- Attorney can supplement with free-text case notes and strategy context
- Case serves as the "lens" through which all juror scoring is performed

**API Endpoints:**
- `POST /api/v1/cases` — create case from PACER number
- `GET /api/v1/cases/:id` — retrieve case details
- `PATCH /api/v1/cases/:id` — update case summary/notes
- `DELETE /api/v1/cases/:id` — archive case

### 2. Summons List / Venire List Upload

**Description:** Upload a jury summons list or venire list. Two distinct phases of jury selection require different handling:

- **Summons list** (weeks before trial): ~1,000 names, usually has addresses. 75% will never come into play. Available via simple request in 90% of counties.
- **Venire list** (day of trial, sometimes Thursday before Monday): Smaller subset, typically name + county only (no addresses). Speed is critical — minutes between receiving list and selection starting.

The system should pre-process the summons list so that when the venire list arrives, jurors can be cross-referenced instantly against already-resolved profiles.

**Key Details:**
- CSV parsing with flexible column mapping (handle variations in column names)
- Validation: required fields present, address parseable
- Batch submission to Launch Labs identity resolution API
- Progress tracking — show resolution status per juror (pending/resolved/unresolvable)
- Handle partial matches and confidence scores from identity platform

**API Endpoints:**
- `POST /api/v1/cases/:case_id/summons_lists` — upload CSV
- `GET /api/v1/cases/:case_id/summons_lists/:id` — list status + jurors
- `POST /api/v1/cases/:case_id/summons_lists/:id/resolve` — trigger identity resolution

### 3. Juror Profiles

**Description:** Enriched profiles built from identity resolution data. Each profile is scored against the case using AI analysis.

**Profile Data (from Launch Labs):**
- Demographics: age, gender (inferred)
- Location: address, neighborhood, property records
- Employment: employer, job title, industry, LinkedIn
- Social media: public posts, sentiment indicators
- Political: voter registration, political donations
- Legal: prior litigation involvement (as party or witness)
- Financial indicators: property ownership, estimated income range
- Education: schools, degrees
- **Household data:** other members of household, their profiles (Lauren confirmed household profiling is valuable)

**AI Scoring:**
- Score: 1–10 scale (1 = strongly unfavorable, 10 = strongly favorable)
- Rationale: 2–3 sentence explanation referencing specific profile data points
- Confidence: high/medium/low based on profile completeness
- Key factors: top 3 factors influencing the score (positive and negative)

**API Endpoints:**
- `GET /api/v1/cases/:case_id/jurors` — list all jurors with scores
- `GET /api/v1/cases/:case_id/jurors/:id` — full juror profile + score detail
- `POST /api/v1/cases/:case_id/jurors/:id/rescore` — trigger rescore (after new data)

### 4. Jury Pool Dashboard

**Description:** Primary interface for reviewing the jury pool. Ranked list of jurors with scores, filterable and sortable. Real-time sync across all users on the case.

**Key Details:**
- Default sort: score descending (most favorable first)
- Filters: score range, confidence level, key factors, resolution status
- Color coding: green (favorable 7-10), yellow (neutral 4-6), red (unfavorable 1-3)
- Click into individual juror for full profile view
- Real-time updates via Turbo Streams / WebSockets — when paralegal logs data, attorney sees it immediately
- Manual score override: attorney can adjust score with a note explaining why

**UI Considerations:**
- Must work well on laptop screens (courtroom use)
- Fast, responsive — no waiting during voir dire
- Clear visual hierarchy — attorney needs to make quick decisions

### 5. Voir Dire Mode

**Description:** The killer feature. Real-time jury selection co-pilot used during voir dire proceedings.

**Key Details:**

**Question Generation:**
- AI generates 3–5 suggested voir dire questions per juror based on:
  - The case specifics (nature of claims, industry, parties)
  - The juror's profile (employment, social data, potential biases)
  - Identified risk factors or areas of concern
- Each question includes:
  - The question text
  - 3–5 multiple-choice response options (ranging from favorable to unfavorable)
  - Why this question matters (brief context for the attorney)
- Attorney can also maintain a custom question bank that applies across jurors

**Live Response Capture:**
- Attorney or paralegal selects the juror's actual response from the multiple-choice options
- Can also add free-text notes per question
- Response is submitted → triggers real-time score reprocessing
- Updated score + revised rationale displayed immediately

**Voir Dire Dashboard:**
- Shows current juror being questioned prominently
- Queue of upcoming jurors
- Running tally: accepted, struck for cause, peremptory strikes remaining
- Quick-strike button: mark juror as struck (for cause or peremptory)

**API Endpoints:**
- `GET /api/v1/cases/:case_id/jurors/:id/questions` — get suggested questions
- `POST /api/v1/cases/:case_id/jurors/:id/responses` — log juror response
- `GET /api/v1/cases/:case_id/voir_dire/status` — voir dire session state
- `PATCH /api/v1/cases/:case_id/jurors/:id/strike` — mark juror as struck

### 6. Firm & User Management

**Description:** Multi-tenant architecture. Firms subscribe, users belong to firms.

**Key Details:**
- Devise authentication with firm-scoped access
- Roles: firm_admin, attorney, associate (paralegal maps to associate)
- Firm admin manages users, billing, settings
- All case data scoped to firm — strict tenant isolation
- Invitation flow for adding users to a firm

**API Endpoints:**
- `POST /api/v1/auth/sign_in` — authenticate
- `POST /api/v1/auth/sign_up` — register firm + first admin user
- `GET /api/v1/firm/users` — list firm users
- `POST /api/v1/firm/users/invite` — invite user to firm
- `PATCH /api/v1/firm/users/:id` — update role

### 7. Training Mode / Mock Trial

**Description:** New users can practice with the application using a mock trial scenario before using it in a real courtroom. Critical for learning the voir dire co-pilot interface without pressure.

**Key Details:**
- Pre-loaded mock case with realistic docket data (fictional case)
- Sample venire list with resolved profiles (representative mix of demographics, risk factors)
- Practice voir dire questions and response logging
- All the same UI/UX as live mode, but clearly marked as "Training"
- Users can reset and repeat the training as needed
- No billing impact — training data doesn't count toward case limits
- Could gamify with scoring on how well they use the tool

**Why Critical:**
- Voir dire happens in real-time with minutes to make decisions
- Users need muscle memory on the interface before high-stakes use
- Reduces support burden and user anxiety
- Demonstrates full product value during onboarding

**API Endpoints:**
- `GET /api/v1/training/cases` — list available mock cases
- `POST /api/v1/training/cases/:id/start` — begin training session
- Training sessions use same API structure as real cases but scoped differently

### 8. Subscription & Billing

**Description:** Firm-level subscriptions tiered by case volume.

**Proposed Tiers:**
- **Starter:** Up to 5 active cases/month
- **Professional:** Up to 20 active cases/month
- **Enterprise:** Unlimited + dedicated support

**Key Details:**
- Stripe integration for billing
- Self-serve signup and upgrade
- Usage tracking: active cases per billing period
- Overage handling: soft limit with notification, then hard block

**API Endpoints:**
- `GET /api/v1/firm/subscription` — current plan + usage
- `POST /api/v1/firm/subscription` — create/change subscription
- `GET /api/v1/firm/invoices` — billing history

---

## Not in MVP (Future Roadmap)

| Feature | Priority | Notes |
|---------|----------|-------|
| Full PACER docket search/browse | High | MVP is case number lookup only |
| Ripple scoring | High | One juror's response flags similar jurors — needs consultant input |
| PDF/print export | High | Courtroom printout of jury pool + scores |
| Historical case analytics | Medium | "In cases like this, jurors with profile X voted..." |
| Juror comparison view | Medium | Side-by-side juror profiles for strike decisions |
| Custom scoring models | Medium | Firm-specific weighting of profile factors |
| Mobile app | Low | Tablet use in courtroom |
| Integration with case management software | Low | Clio, MyCase, etc. |

---

## Technical Architecture

### Stack

- **Framework:** Ruby on Rails 8.x (37signals patterns)
- **Frontend:** Hotwire (Turbo + Stimulus), Tailwind CSS, ViewComponents
- **Database:** PostgreSQL
- **Real-time:** Turbo Streams over WebSockets (ActionCable)
- **Background Jobs:** Solid Queue (Rails 8 default)
- **Auth:** Devise + firm-scoped tenancy
- **Billing:** Stripe (via pay gem or direct API)
- **AI:** OpenAI API (or Anthropic) for juror scoring + question generation
- **Identity Resolution:** Launch Labs API (mocked in development)
- **Docket Data:** PACER Case Locator API / CourtListener RECAP
- **Deployment:** Docker → AWS (ECS or EKS), designed for multi-datacenter

### Monorepo Structure

```
juryprofile/
├── app/                          # Rails application
│   ├── controllers/
│   │   ├── api/v1/               # API controllers
│   │   └── web/                  # Web controllers (Turbo/HTML)
│   ├── models/
│   ├── services/                 # Business logic services
│   │   ├── identity/             # Launch Labs API integration
│   │   ├── docket/               # PACER integration
│   │   ├── scoring/              # AI scoring engine
│   │   └── billing/              # Stripe integration
│   ├── components/               # ViewComponents
│   ├── javascript/controllers/   # Stimulus controllers
│   ├── policies/                 # Pundit policies
│   └── jobs/                     # Background jobs
├── compliance/                   # SOC-2 + ISO 27001 controls
│   ├── soc2/
│   │   ├── controls.md
│   │   └── evidence/
│   ├── iso27001/
│   │   ├── controls.md
│   │   └── evidence/
│   └── README.md
├── docs/                         # Customer-facing support docs
│   ├── getting-started.md
│   ├── api/
│   │   └── openapi.yaml          # OpenAPI spec
│   └── guides/
├── marketing/                    # Marketing website
│   ├── pages/
│   ├── assets/
│   └── README.md
├── spec/                         # Tests
├── config/
├── db/
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Key Domain Models

```
Firm
  has_many :users
  has_many :subscriptions
  has_many :cases

User
  belongs_to :firm
  has_many :cases (through firm)
  enum :role, [:firm_admin, :attorney, :associate]

Case
  belongs_to :firm
  has_many :summons_lists
  has_many :jurors, through: :summons_lists
  has_one :docket
  # pacer_case_number, title, nature_of_suit, summary, notes

Docket
  belongs_to :case
  # raw_data (JSON), parties, claims, jurisdiction, key_dates

SummonsList
  belongs_to :case
  has_many :jurors
  # file metadata, upload status

Juror
  belongs_to :summons_list
  has_one :profile
  has_many :scores
  has_many :questions
  has_many :responses
  # first_name, last_name, address, county, status

Profile
  belongs_to :juror
  # enriched identity data (JSON), resolution_confidence, resolved_at

Score
  belongs_to :juror
  # value (1-10), rationale, confidence, key_factors, version, scored_at

Question
  belongs_to :juror
  has_many :response_options
  has_one :response
  # text, context, source (ai_generated | custom_bank), position

ResponseOption
  belongs_to :question
  # text, sentiment_weight, position

Response
  belongs_to :question
  belongs_to :response_option (optional)
  belongs_to :recorded_by (User)
  # free_text_notes, recorded_at

QuestionBank
  belongs_to :firm
  has_many :questions (template questions)
  # name, description

TrainingCase
  # Mock case data for user training
  # title, description, mock_docket_data (JSON), created_at

TrainingJuror
  belongs_to :training_case
  # Mock juror profiles for practice
  # first_name, last_name, mock_profile_data (JSON), position
```

---

## Compliance Framework

### SOC-2 Trust Service Criteria (tracked from day 1)

| Category | Relevance | MVP Controls |
|----------|-----------|-------------|
| **Security** | Critical — PII data, legal data | Encryption at rest + transit, RBAC, audit logging, pen testing |
| **Availability** | High — courtroom use requires uptime | Health checks, monitoring, incident response plan |
| **Processing Integrity** | High — scoring accuracy matters | Input validation, AI output logging, score versioning |
| **Confidentiality** | Critical — attorney-client adjacent data | Tenant isolation, access controls, data classification |
| **Privacy** | Critical — juror PII | Data retention policies, consent framework, minimization |

### ISO 27001 Annex A Controls (key areas)

- A.5: Information security policies
- A.6: Organization of information security
- A.8: Asset management (data classification)
- A.9: Access control (RBAC, MFA)
- A.10: Cryptography (encryption standards)
- A.12: Operations security (logging, monitoring)
- A.14: System development security (secure SDLC — our agent workflow enforces this)
- A.18: Compliance (legal, regulatory)

Detailed control mappings will be maintained in `/compliance/`.

---

## Build Plan — Feature Sequence

Building in this order to get the pipeline working end-to-end first:

| # | Feature | Dependency | Est. PRs |
|---|---------|-----------|----------|
| 1 | Rails scaffold + Devise auth + firm tenancy | None | 3-5 |
| 2 | Case setup + PACER integration | Auth | 3-4 |
| 3 | Summons list upload + CSV parsing | Cases | 2-3 |
| 4 | Identity resolution integration (mocked) | Summons lists | 2-3 |
| 5 | Juror profiles + AI scoring engine | Profiles | 3-5 |
| 6 | Jury pool dashboard | Scoring | 3-4 |
| 7 | Voir dire mode + question generation | Dashboard | 4-6 |
| 8 | Live response capture + real-time reprocessing | Voir dire | 3-4 |
| 9 | Training mode / mock trial | Voir dire + scoring | 2-3 |
| 10 | Stripe billing + subscription tiers | Auth/Firm | 2-3 |
| 11 | Marketing landing page | None (parallel) | 2-3 |
| 12 | Support docs (getting started, API) | Features 1-9 | 2-3 |

**Estimated total: ~32-48 PRs for MVP**

---

## Open Questions

1. **NC Bar Ethics Opinion #2 (2024)** — Kelly flagged this as the starting point: <https://www.ncbar.gov/for-lawyers/ethics/adopted-opinions/2024-formal-ethics-opinion-1/>. Need to review and build compliance around it. Kelly: "We will not be able to sell anything to law firms without tackling this piece at the very beginning."
2. **Privileged info handling** — What case info can safely flow into AI scoring? Attorney work product, client communications, and strategy notes may be privileged. Need clear guardrails on what goes in vs. what doesn't.
3. **FCRA applicability** — identity data used for jury selection may or may not trigger FCRA obligations. Legal review needed.
4. **Ripple scoring** — should one juror's response update scores for similar jurors? Defer to consultant.
5. **Data retention** — how long to keep juror PII after a case concludes? Compliance implication.
6. **AI model selection** — OpenAI vs Anthropic vs self-hosted for scoring. Latency and accuracy tradeoffs.
7. **PACER costs** — PACER charges $0.10/page. Need to understand cost implications for docket pulls.

---

## Validation Plan

- **Jury consultant review** of AI scoring logic and question generation
  - Lauren Kulp — Tandem Legal Solutions (lauren@tandemlegalsolutions.com)
- **Trial attorney feedback** on dashboard + voir dire UX
  - Kelly Dagger — Ellis & Winters (kelly.dagger@elliswinters.com)
- **Training mode validation** — test the mock trial experience with new users to ensure it properly prepares them for real courtroom use
- **Pilot program** with 2-3 firms before general availability
