# Vireo Audio — AI-assisted Support Categoriser

## What it does

- Reads `tickets.csv`.
- Restricts analysis to the stated Jan 2025–Jun 2026 window (11,641 tickets in scope).
- Auto-categorises tickets from the customer's opening message using contextual text-matching rules.
- Uses explicit text evidence first and the existing intake tag only as a fallback.
- Shows monthly category and first-assigned-team volumes.
- Exports the classified dataset with decision confidence and classification method.

## Expected input data layout

The tool and evidence script look for `tickets.csv` in any of the following standard locations:
1. As a CLI argument: `python make_outputs.py path/to/tickets.csv`
2. Environment variable: `TICKETS_CSV=path/to/tickets.csv`
3. Project root: `./tickets.csv`
4. Tool directory: `./vireo_support_tool/tickets.csv`
5. Parent directory: `../tickets.csv` (or any `*tickets*.csv` downloaded in the parent folder)

## Run the interactive Streamlit app

Requires Python 3.10+.

```bash
# From the project root or vireo_support_tool directory:
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r vireo_support_tool/requirements.txt
cd vireo_support_tool
streamlit run app.py
```

Then upload `tickets.csv` through the Streamlit interface.

## Regenerate evidence and QA artifacts

To regenerate all deliverables (`evidence/classified_tickets.csv`, `evidence/monthly_category.png`, `evidence/monthly_team.png`, `evidence/metrics.json`, and `evidence/qa_sample.csv`):

```bash
# From the project root:
python make_outputs.py
# Or specify tickets.csv path explicitly:
python make_outputs.py path/to/tickets.csv
```

## Design choice

The task pack does not provide an external LLM API key, so this tool is deliberately API-free, fully auditable, and 100% reproducible. It uses a prioritized contextual text-rule cascade derived from Vireo's Customer Support Operating Policy, retaining the exported bot tag only as a fallback.

`decision_confidence` is a heuristic score (0.90 for explicit text rule, 0.55 for intake tag fallback, 0.30 for unresolved), highlighting low-confidence tickets for human supervisory review.

## Scope decision

Tier 2 (`Escalations & Warranty`) is displayed in the team chart for completeness but held separate from Tier 1 volume comparisons, per Section 6 of the Vireo Customer Support Operating Policy.

