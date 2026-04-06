# JuryProfile — Compliance Framework

**Related:** [[PRODUCT_SPEC]] | [[docs/sme-conversation-notes]]

This directory tracks SOC-2 and ISO 27001 compliance controls from day 1.

## Structure

```
compliance/
├── soc2/
│   ├── controls.md        # SOC-2 Trust Service Criteria mapping
│   └── evidence/           # Evidence artifacts per control
├── iso27001/
│   ├── controls.md        # ISO 27001 Annex A control mapping
│   └── evidence/           # Evidence artifacts per control
└── README.md              # This file
```

## Approach

Every feature PR should reference applicable compliance controls. The security-agent in our build workflow will validate that:

1. New data models classify data sensitivity (PII, confidential, internal, public)
2. Access controls are implemented and tested (Pundit policies)
3. Audit logging is in place for sensitive operations
4. Encryption requirements are met
5. Input validation prevents injection/manipulation

## Data Classification

| Classification | Description | Examples |
|---------------|-------------|---------|
| **PII-Sensitive** | Juror personally identifiable information | Names, addresses, social profiles, political data |
| **Confidential** | Attorney work product, case strategy | Case notes, scoring adjustments, strike decisions |
| **Internal** | Firm operational data | User accounts, billing, usage metrics |
| **Public** | Publicly available information | PACER docket data, published case details |

## Compliance Contacts

- **Security Lead:** TBD
- **Compliance Officer:** TBD
- **External Auditor:** TBD (engage before first customer)
