# SME Conversation Notes — Nov 5-17, 2025

**Related:** [[PRODUCT_SPEC]] | [[compliance/README]]

Email thread between Garrett, Lauren Kulp (jury consultant), and Kelly Dagger (trial attorney).

---

## Lauren's Existing Tool: JurorPulse

- Lauren and Ashlyn built a **custom GPT called JurorPulse**
- Inputs: complaint, summary PowerPoint, prep call notes with attorney/client, background research on parties
- Produces a juror assessment report (3 sample reports were shared)
- Iterates after every trial — still improving
- Suggests something like JurorPulse output could inform data points to highlight per juror

## Jury Selection Process (from Lauren)

- **Summons → venire is 100% random** (pool filters to who showed up, randomly shuffled to courtrooms)
- Sometimes get additional venire lists or "sloppy seconds" from other trials
- **75% of summons list will never come into play**
- **Summons list:** Available weeks before trial in 90% of counties. Free, simple email request. Some counties more cumbersome/costly but cheap overall.
- **Venire list:** Comes day-of in 90% of cases, **minutes before selection**. In a few places, available Thursday before Monday selection.
- **Summons lists usually have addresses; venire lists typically do NOT**
- Zip code always available or easily found
- **Entire household profiling is valuable** (Lauren's input)

## Existing Competitors (Lauren has trialed most)

- **Momus Analytics** (momusanalytics.com) — juror management platform + voter records + social media links. Best Lauren has found but leaves a lot to be desired.
- **Juror Search** (jurorsearch.com) — juror management platform only. Second best.
- **Pipl** (pipl.com) — data product. Didn't provide enough for Lauren to trial. Garrett found their data "very unreliable" from past investigation.
- **None** are anywhere near a comprehensive juror data source.

## Design Consensus

- **Users should get value without pre-work** (broaden subscription, improve retention) — only power users would want to add their own context
- **Power user mode** for attorneys who lean in + jury consultants become customers too
- **Modular AI over discrete tasks** with relevant data we control > heap of information approach
- JurorPulse-like reports on each venire member makes sense as output format
- AI should summarize info for a person and compare/contrast with ideal juror persona (Garrett)

## Ethics & Legal

- **NC State Bar 2024 Formal Ethics Opinion #2:** <https://www.ncbar.gov/for-lawyers/ethics/adopted-opinions/2024-formal-ethics-opinion-1/?opinionSearchTerm=use+of%25>
- Kelly: **"We will not be able to sell anything to law firms without tackling this piece at the very beginning"**
- Garrett: Compliance/data policy maturity needed earlier than usual. Doing it early creates a **competitive moat**.
- Kelly: No opinions found specifically on AI for juror research (as of Nov 2025)
- **Privileged info feeding into AI flagged as potential issue** — needs guardrails

## Garrett's Early Prototype

- Ran summons list against single data source → matched ~60%
- Has more data sources available (Launch Labs)
- Attribute data spreadsheet shared: <https://docs.google.com/spreadsheets/d/1gmz6VoRJToXCe9q8AF0AoQe6KWZ3FlapdddAYLMCNKY/edit?usp=sharing>

## Sample Data Shared

- **Holliday Post Voir Dire Report** (PDF) — sample of Lauren's current output
- **Venire List** (PDF) — from actual trial, corresponds to Holliday case
- **Sample Jury Summons List** (XLSX) — county format example
- **Google Drive folder** with more venire lists from different counties/formats: <https://drive.google.com/drive/folders/1X5VIOTkW7zEj_xvproAF1nKoqcT4AQAG?usp=sharing>
- **Whimsical design** (Garrett's initial flow): <https://whimsical.com/jury-intelligence-design-2XDW9Q8ncJcab6VVsTg5uG>

## Key Implications for Product Spec

1. **Two-phase input matters:** Summons list (weeks before, with addresses) vs. venire list (day-of, names + county only). Product must handle both.
2. **Speed is critical for venire list:** Minutes between receiving the list and selection starting. Pre-processing summons list makes venire-day faster (cross-reference).
3. **Household profiling** should be included in enrichment.
4. **JurorPulse-style output** is the proven format — our AI scoring should produce something similar per juror.
5. **Competitor landscape is weak** — no comprehensive data source exists. Launch Labs data is the differentiator.
6. **Ethics compliance is a day-1 requirement** and a selling point / moat.
7. **Privileged info handling** needs clear guardrails (what goes into AI, what doesn't).
