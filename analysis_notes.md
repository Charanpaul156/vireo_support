# Vireo Audio — Analysis Notes

## Scope
- Analysis window: 1 Jan 2025 through 30 Jun 2026 inclusive (18 months).
- 11,641 tickets included.
- 139 rows dated before 1 Jan 2025 excluded.
- No duplicate ticket IDs found.

## Team Volume & Workload by Timeframe
### Full 18-Month Period (Jan 2025 – Jun 2026)
| First-assigned team | Tickets | Share | Roster agents | Tickets/agent/month (18 mo)* |
|---|---:|---:|---:|---:|
| Chat Frontline | 3,030 | 26.0% | 15 | 11.2 |
| Billing | 2,425 | 20.8% | 4 | 33.7 |
| Logistics | 1,905 | 16.4% | 5 | 21.2 |
| Email Frontline | 1,807 | 15.5% | 7 | 14.3 |
| Returns Desk | 1,049 | 9.0% | 3 | 19.4 |
| Voice Frontline | 900 | 7.7% | 4 | 12.5 |
| Escalations & Warranty (Tier 2)** | 525 | 4.5% | 6 | 4.9 |

\*Simple roster-based workload indicator (total tickets / rostered headcount / 18 months); not a productivity measure.
\**Tier 2 is certified, handles multi-touch complex cases measured in days, and is held separate from Tier 1 volume comparisons per Policy Section 6.

### Current-Helpdesk Period (14 Sep 2025 – 30 Jun 2026, ~9.5 months)
Transfers and granular hand-off data exist only in the current helpdesk system (7,728 tickets total):
- **Billing**: 1,558 tickets across 4 rostered agents $\rightarrow$ **40.9 tickets/agent/month**.
- **Chat Frontline**: 2,063 tickets across 15 rostered agents $\rightarrow$ **14.5 tickets/agent/month**.

## Billing Routing Signal & Avoided Transfer Estimate
Measured on current-helpdesk rows only (transfers were not recorded in legacy Freshdesk):
- Billing tickets: 1,558
- Tickets with $\ge$ 1 transfer: 498 (32.0% transfer rate)
- Total transfer events: 632
- 384 of 498 transferred Billing tickets (77.1%) have an explicit non-Billing destination in agent closing notes.
- 365 explicitly name Logistics (misrouted delivery status/tracking requests).
- Vireo policy standard (Section 4): ₹305 per internal transfer.

### Operating Target & Annualized Cost Estimate
- Target: Reduce Billing transfer rate from **32.0% to 20.0%** ($\Delta = 12.0\%$).
- Annualized Billing run-rate: ~1,965 tickets/year (1,558 / 9.52 months $\times$ 12).
- Annualized avoided transfers: ~235 transfers/year.
- Estimated annualized transfer handling cost avoidance: **~₹71,700/year** (235 $\times$ ₹305).
- *Caveat*: This is an annualized planning estimate derived from the post-migration run-rate to establish an operational process target, not a guaranteed cash saving.

## SLA Signal
Current-helpdesk tickets:
- 7,728 tickets
- 839 first-response breaches (10.9% breach rate)
- Each first-response breach triggers a ₹350 store credit under policy Section 3.

*Timestamp caveat*: 2,379 legacy tickets have `resolved_at` earlier than `created_at`. As documented in Policy Section 9, legacy resolution timestamps were reconstructed from UTC event logs whereas the helpdesk displays IST (+05:30). Consequently, cross-system handle time cannot be reliably compared.

## Categorisation QA
A fixed 60-ticket sample was evaluated against analyst-reviewed gold labels (random seed 999).
- **55 / 60 matched the classifier (91.7% accuracy)**.
- Contextual matching for product terms like "Orbit speaker" eliminated the earlier false positive where return requests were tagged as Audio Quality.
- The 5 remaining errors are mixed-intent inquiries (e.g. customers reporting address typos or pickup dates framed around "in app" navigation).
- This sample demonstrates transparent rule behavior and is exposed with confidence scores for human auditing.

