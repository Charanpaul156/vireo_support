# To: Priya Raman, Head of Customer Experience
## Subject: Vireo support volume, routing and the next two hires

### 1. Factual Volume Finding (Jan 2025 – Jun 2026)
The export contains **11,641 tickets in the 18-month analysis window** (excluding 139 pre-2025 records). By first-assigned team, **Chat Frontline is the largest absolute queue (3,030 tickets; 26.0%)**, followed by Billing (2,425; 20.8%), Logistics (1,905; 16.4%), Email Frontline (1,807; 15.5%), Returns Desk (1,049; 9.0%), and Voice Frontline (900; 7.7%). 

*Note on Tier 2*: Escalations & Warranty handled 525 tickets (4.5%). Per Section 6 of the Customer Support Operating Policy, Tier 2 manages multi-touch cases measured in days and is held strictly separate from Tier 1 volume comparisons.

### 2. Workload per Headcount by Timeframe
Raw queue volume does not reflect individual workload because team sizes differ substantially:
- **Full 18-month window**: Chat Frontline has 15 rostered agents (**11.2 tickets/agent/month**), whereas Billing has only 4 rostered agents (**33.7 tickets/agent/month**).
- **Current helpdesk period (post-14 Sep 2025, ~9.5 months)**: Billing workload rose to **40.9 tickets/agent/month**, compared to **14.5** for Chat Frontline. On a per-head basis, Billing carries nearly triple the workload of Chat.

### 3. Routing & Process Finding (The Billing Hand-Off Signal)
In the current helpdesk system (where transfers are tracked), Billing received 1,558 tickets:
- **498 tickets (32.0%) required at least one transfer** (632 total transfer events).
- In agent closing notes, **384 of those 498 transferred tickets (77.1%) explicitly name a non-Billing destination**, and **365 explicitly name Logistics**. Customers are repeatedly contacting Billing for delivery tracking and courier status because of early intake confusion.

### 4. Financial Implication & Business Target
Under Policy Section 4, internal transfers cost **₹305 per transfer** in administrative re-handling.

> **Operational Target: Reduce Billing's transfer rate from 32% to 20%.**

- Based on Billing's annualized run-rate (~1,965 tickets/year), achieving this 20% target would avoid approximately **235 unnecessary hand-offs per year**.
- This yields an **estimated annualized transfer cost avoidance of ~₹71,700/year** (235 $\times$ ₹305). *This is an annualized planning estimate to guide intake optimization, not guaranteed cash savings.*
- Separately, **10.9% of tickets breach first-response SLA targets** in the current helpdesk, automatically issuing ₹350 store credits. Fixing routing will reduce queue latency and credit exposure.

### 5. Categorisation & Tooling Finding
Intake bot tagging is noisy, often dumping fulfilment and delivery complaints into "Billing & Payments" or "Other". A contextual text-first classifier moves these directly into delivery and return workflows. On an analyst-reviewed **60-ticket QA sample, 55 were classified correctly (91.7%)**. The tool exposes confidence scores so lower-confidence tickets can be reviewed before routing.

### 6. Staffing Recommendation for the Next Two Hires
- If the mandate is strictly **largest total Tier-1 volume**, hire for **Chat Frontline**.
- If the mandate is **workload relief per agent**, hire for **Billing**.
- **Recommended Strategy**: Do not treat volume in isolation. First, correct the intake bot rules to route the ~365 misplaced logistics inquiries directly to Logistics, reducing Billing's transfer overhead. Then, review post-fix ticket loads to allocate the two headcount where genuine operational backlog remains.

### 7. Data Limitations & Caveats
1. **Excluded Rows**: 139 records created prior to 1 Jan 2025 were excluded from the analysis window.
2. **Handle Time Inconsistency**: 2,379 legacy rows show resolution timestamps earlier than creation timestamps. As explained in Policy Section 9, legacy Freshdesk resolution timestamps were reconstructed from UTC logs while the helpdesk exports in IST (+05:30). Cross-system handle time was therefore excluded as a staffing metric.

