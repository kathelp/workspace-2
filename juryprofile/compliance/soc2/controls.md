# SOC-2 Trust Service Criteria — Control Mapping

**Related:** [[PRODUCT_SPEC]] | [[compliance/README]] | [[compliance/iso27001/controls]]

**Status:** Initial framework — controls will be populated as features are built.

---

## CC1 — Control Environment

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| CC1.1 | Commitment to integrity and ethical values | Code of conduct, data handling policy | 🔲 Not started |
| CC1.2 | Board/management oversight | Security review process in build workflow | 🔲 Not started |

## CC2 — Communication & Information

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| CC2.1 | Internal communication of security policies | SECURITY.md in repo, onboarding docs | 🔲 Not started |
| CC2.2 | External communication (privacy policy, ToS) | Marketing site + in-app | 🔲 Not started |

## CC3 — Risk Assessment

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| CC3.1 | Risk identification process | Threat model per feature (security-agent) | 🔲 Not started |
| CC3.2 | Fraud risk assessment | RBAC, audit logs, anomaly detection | 🔲 Not started |

## CC4 — Monitoring Activities

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| CC4.1 | Ongoing monitoring | Application monitoring, error tracking | 🔲 Not started |
| CC4.2 | Deficiency remediation | Issue tracking, SLA for security issues | 🔲 Not started |

## CC5 — Control Activities

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| CC5.1 | Logical access controls | Devise auth, Pundit RBAC, firm tenancy | 🔲 Not started |
| CC5.2 | Infrastructure security | VPC, security groups, encryption | 🔲 Not started |
| CC5.3 | Change management | Git workflow, PR reviews, CI/CD | 🔲 Not started |

## CC6 — Logical & Physical Access

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| CC6.1 | Access provisioning | Invitation flow, role assignment | 🔲 Not started |
| CC6.2 | Access revocation | User deactivation, session management | 🔲 Not started |
| CC6.3 | Authentication mechanisms | Devise + MFA (future) | 🔲 Not started |
| CC6.6 | Encryption of data in transit | TLS 1.2+ enforced | 🔲 Not started |
| CC6.7 | Encryption of data at rest | AES-256 for PII fields, encrypted DB backups | 🔲 Not started |

## CC7 — System Operations

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| CC7.1 | Vulnerability management | Bundler Audit, Brakeman, dependency scanning | 🔲 Not started |
| CC7.2 | Incident detection & response | Logging, alerting, incident response playbook | 🔲 Not started |
| CC7.3 | Recovery procedures | Backup strategy, disaster recovery plan | 🔲 Not started |

## CC8 — Change Management

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| CC8.1 | Change authorization | PR approval workflow, CI gates | 🔲 Not started |

## CC9 — Risk Mitigation (Vendors)

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| CC9.1 | Vendor risk assessment | Launch Labs, PACER, Stripe, AI provider | 🔲 Not started |
| CC9.2 | Vendor monitoring | SLA tracking, security review cadence | 🔲 Not started |

---

## Additional Criteria

### Availability (A1)

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| A1.1 | System availability commitments | SLA definition, uptime monitoring | 🔲 Not started |
| A1.2 | Disaster recovery | Multi-AZ deployment, backup/restore testing | 🔲 Not started |

### Confidentiality (C1)

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| C1.1 | Confidential data identification | Data classification (see compliance/README) | 🔲 Not started |
| C1.2 | Confidential data disposal | Retention policy, secure deletion | 🔲 Not started |

### Privacy (P1-P8)

| Control ID | Description | Implementation | Status |
|-----------|-------------|----------------|--------|
| P1.1 | Privacy notice | Privacy policy on marketing site | 🔲 Not started |
| P3.1 | Personal information collection | Minimization — only collect what's needed | 🔲 Not started |
| P4.1 | Use of personal information | Purpose limitation — jury selection only | 🔲 Not started |
| P6.1 | Data retention & disposal | Retention schedule per data classification | 🔲 Not started |
| P8.1 | Data subject rights | Access, correction, deletion requests | 🔲 Not started |
