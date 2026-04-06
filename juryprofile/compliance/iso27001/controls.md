# ISO 27001 Annex A — Control Mapping

**Related:** [[PRODUCT_SPEC]] | [[compliance/README]] | [[compliance/soc2/controls]]

**Status:** Initial framework — controls populated as features are built.
**Standard:** ISO/IEC 27001:2022

---

## A.5 — Organizational Controls

| Control | Description | Implementation | Status |
|---------|-------------|----------------|--------|
| A.5.1 | Information security policies | SECURITY.md, compliance docs | 🔲 Not started |
| A.5.2 | Information security roles | Role definitions in firm management | 🔲 Not started |
| A.5.8 | Information security in project management | Security-agent in build workflow | 🔲 Not started |

## A.6 — People Controls

| Control | Description | Implementation | Status |
|---------|-------------|----------------|--------|
| A.6.1 | Screening | Background checks for team (operational) | 🔲 Not started |
| A.6.3 | Information security awareness | Security training docs | 🔲 Not started |

## A.7 — Physical Controls

| Control | Description | Implementation | Status |
|---------|-------------|----------------|--------|
| A.7.1 | Physical security perimeters | AWS data center controls (inherited) | 🔲 Not started |

## A.8 — Technological Controls

| Control | Description | Implementation | Status |
|---------|-------------|----------------|--------|
| A.8.1 | User endpoint devices | Session management, timeout policies | 🔲 Not started |
| A.8.2 | Privileged access rights | Admin role restrictions, audit logging | 🔲 Not started |
| A.8.3 | Information access restriction | Pundit policies, firm tenancy isolation | 🔲 Not started |
| A.8.5 | Secure authentication | Devise + strong password policy + MFA (future) | 🔲 Not started |
| A.8.7 | Protection against malware | Dependency scanning, input sanitization | 🔲 Not started |
| A.8.9 | Configuration management | Infrastructure as Code, env management | 🔲 Not started |
| A.8.10 | Information deletion | Data retention policy, secure deletion | 🔲 Not started |
| A.8.11 | Data masking | PII masking in logs, non-prod environments | 🔲 Not started |
| A.8.12 | Data leakage prevention | Output sanitization, API response filtering | 🔲 Not started |
| A.8.15 | Logging | Structured audit logging for all sensitive operations | 🔲 Not started |
| A.8.16 | Monitoring activities | Application + infrastructure monitoring | 🔲 Not started |
| A.8.24 | Use of cryptography | TLS 1.2+, AES-256 at rest, key management | 🔲 Not started |
| A.8.25 | Secure development lifecycle | TDD workflow, security-agent review, Brakeman | 🔲 Not started |
| A.8.26 | Application security requirements | Input validation, OWASP top 10 coverage | 🔲 Not started |
| A.8.28 | Secure coding | Rubocop security rules, strong params, CSRF | 🔲 Not started |

---

## Statement of Applicability (SoA)

The full SoA will be maintained as the system matures. Controls marked N/A will be documented with justification.

## Risk Register

A risk register will be maintained in `compliance/risk-register.md` once the initial threat model is complete.
