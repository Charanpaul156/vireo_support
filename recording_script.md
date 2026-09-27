# 3-minute screen-recording script

## 0:00–0:30 — What I built
“Vireo asked for automated ticket categorisation plus monthly category and team volume trends to inform staffing and operational routing. I built a local, lightweight Streamlit tool. It ingests tickets.csv, filters strictly to the Jan 2025 through Jun 2026 window (11,641 tickets), categorises each customer opening message, and exports decision confidence and method metadata so the classification is auditable and transparent.”

## 0:30–1:15 — Prompt / categorisation approach
“I used an issue-first taxonomy directly grounded in Vireo's Customer Support Operating Policy: Billing & Payments, Delivery & Shipping, Returns & Refunds, Connectivity, Charging & Battery, App & Firmware, Product Enquiry, Audio Quality, Warranty & Repair, Account & Login, and Other.”

“I deliberately did not use an external cloud LLM API because no API key was provided and client ticket data should remain private and reproducible. The classifier is 100% deterministic and API-free: prioritized contextual regex rules take precedence, with the bot intake tag retained only as a fallback, and unresolved tickets flagged for human review.”

## 1:15–2:00 — What changed between versions & QA results
“The initial version treated words like ‘speaker’ and ‘refund’ in isolation. That caused false positives: for example, customers mentioning the ‘Orbit speaker’ during delivery or pickup issues were miscategorized as Audio Quality, and delivery delays demanding a refund were mislabeled as Returns.”

“I refined the rules to use contextual matching for product references and enforced precedence so primary fulfilment issues win. On our fixed 60-ticket analyst-reviewed QA sample, accuracy increased to 55 out of 60 correct, or 91.7%. The five remaining errors are mixed-intent inquiries involving app navigation.”

## 2:00–2:35 — Business finding & operating target
“For the staffing decision: Chat Frontline is the largest absolute Tier-1 queue at 3,030 tickets (26.0%), followed by Billing at 2,425 (20.8%). But Chat has 15 rostered agents while Billing has only 4. That means Billing handled 33.7 tickets per agent per month over the 18-month window, rising to 40.9 in the current helpdesk—nearly three times the workload of Chat Frontline.”

“More importantly, there is a strong process defect: in the current helpdesk, 32% of Billing tickets have at least one transfer, and 77% of those transferred tickets have notes explicitly naming Logistics. Customers are contacting Billing for courier tracking. I set a concrete target to reduce Billing's transfer rate from 32% to 20%, which avoids an estimated 235 transfers per year, saving approximately ₹71,700 annually in transfer re-handling costs.”

## 2:35–3:00 — What was discarded & data caveats
“I excluded 139 pre-window rows from 2024. I also discarded cross-system handle time because 2,379 legacy tickets had resolution timestamps earlier than creation; the policy explains Freshdesk resolution was reconstructed from UTC while the helpdesk displays IST. I kept Tier 2 Escalations separate from Tier 1 volume per policy. Finally, because submission-form.md was missing from the supplied pack, I documented its omission in submission_notes.md rather than fabricating form fields.”

