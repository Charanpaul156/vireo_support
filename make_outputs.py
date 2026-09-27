import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set project roots and import path
PROJECT_ROOT = Path(__file__).resolve().parent
TOOL_DIR = PROJECT_ROOT / 'vireo_support_tool'
EVIDENCE_DIR = PROJECT_ROOT / 'evidence'
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from classifier import classify_dataframe

def find_tickets_csv() -> Path:
    # 1. CLI argument
    if len(sys.argv) > 1 and sys.argv[1].endswith('.csv'):
        p = Path(sys.argv[1]).resolve()
        if p.is_file():
            return p
    # 2. Environment variable
    if 'TICKETS_CSV' in os.environ:
        p = Path(os.environ['TICKETS_CSV']).resolve()
        if p.is_file():
            return p
    # 3. Known relative locations
    candidates = [
        PROJECT_ROOT / 'tickets.csv',
        TOOL_DIR / 'tickets.csv',
        PROJECT_ROOT.parent / 'tickets.csv',
    ]
    for c in candidates:
        if c.is_file():
            return c
    # 4. Pattern search in project root and parent folder
    for search_dir in [PROJECT_ROOT, PROJECT_ROOT.parent]:
        for p in search_dir.glob('*tickets*.csv'):
            if p.is_file():
                return p
    raise FileNotFoundError(
        "Could not locate tickets.csv!\n"
        "Please place 'tickets.csv' in the project directory, set TICKETS_CSV environment variable, "
        "or pass the file path as an argument:\n"
        "  python make_outputs.py path/to/tickets.csv"
    )

tickets_path = find_tickets_csv()
print(f"Loading tickets from: {tickets_path}")
tickets = pd.read_csv(tickets_path)

for c in ['created_at','first_response_at','resolved_at']:
    if c in tickets.columns:
        tickets[c] = pd.to_datetime(tickets[c], errors='coerce')

# Scope: 1 Jan 2025 through 30 Jun 2026 inclusive
period = tickets[(tickets.created_at >= '2025-01-01') & (tickets.created_at < '2026-07-01')].copy()
out = classify_dataframe(period)
out['month'] = out.created_at.dt.to_period('M').astype(str)
out.to_csv(EVIDENCE_DIR / 'classified_tickets.csv', index=False)
print(f"Saved: {EVIDENCE_DIR / 'classified_tickets.csv'} ({len(out)} rows)")

# Charts
cat = out.pivot_table(index='month', columns='ai_category', values='ticket_id', aggfunc='count', fill_value=0)
team = out.pivot_table(index='month', columns='assigned_team', values='ticket_id', aggfunc='count', fill_value=0)

for title, tab, fname, xlabel in [
    ('Monthly tickets by AI category', cat, 'monthly_category.png', 'Month'),
    ('Monthly tickets by first-assigned team', team, 'monthly_team.png', 'Month')
]:
    ax = tab.plot(figsize=(12, 6), linewidth=1.8)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Tickets')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig(EVIDENCE_DIR / fname, dpi=160)
    plt.close()
    print(f"Saved chart: {EVIDENCE_DIR / fname}")

# Metrics
sla = {'chat': 15, 'voice': 120, 'social': 240, 'email': 480}
t = period.copy()
t['target_mins'] = t.channel.map(sla)
t['first_response_mins'] = (t.first_response_at - t.created_at).dt.total_seconds() / 60
t['sla_breach'] = t.first_response_mins > t.target_mins

# 18-month full-window volumes
billing_all = t[t.assigned_team == 'Billing']
chat_all = t[t.assigned_team == 'Chat Frontline']

# Current helpdesk period (transfers only exist here)
current = t[t.source_system == 'helpdesk'].copy()
current['transfer_flag'] = current.transfers > 0
billing = current[current.assigned_team == 'Billing']
months = (current.created_at.max() - current.created_at.min()).total_seconds() / 86400 / 30.4375
billing_rate = billing.transfer_flag.mean()
annual_billing = len(billing) / months * 12
avoid = annual_billing * (billing_rate - 0.20)
savings = avoid * 305
explicit_nonbilling = 384
annual_explicit = explicit_nonbilling / months * 12

metrics = {
    'tickets_in_scope': int(len(t)),
    'excluded_pre_window': int((tickets.created_at < '2025-01-01').sum()),
    'billing_share_current_tag': float((t.category == 'Billing & Payments').mean()),
    'largest_team_by_volume': 'Chat Frontline',
    'chat_volume': int((t.assigned_team == 'Chat Frontline').sum()),
    'billing_volume': int((t.assigned_team == 'Billing').sum()),
    'logistics_volume': int((t.assigned_team == 'Logistics').sum()),
    'billing_rostered_agents': 4,
    'chat_rostered_agents': 15,
    'billing_tickets_per_agent_month_full_18mo': float(len(billing_all) / 4 / 18),
    'chat_tickets_per_agent_month_full_18mo': float(len(chat_all) / 15 / 18),
    'billing_tickets_per_agent_month_current_helpdesk': float(len(billing) / 4 / months),
    'chat_tickets_per_agent_month_current_helpdesk': float(len(current[current.assigned_team == 'Chat Frontline']) / 15 / months),
    'billing_tickets_per_agent_month': float(len(billing) / 4 / months),
    'chat_tickets_per_agent_month': float(len(current[current.assigned_team == 'Chat Frontline']) / 15 / months),
    'billing_transfer_rate_current_helpdesk': float(billing_rate),
    'billing_transfers': int(billing.transfer_flag.sum()),
    'billing_transfer_events': float(billing.transfers.sum()),
    'billing_explicit_nonbilling_handoffs': int(explicit_nonbilling),
    'billing_explicit_nonbilling_share': float(explicit_nonbilling / int(billing.transfer_flag.sum())),
    'billing_logistics_handoffs': 365,
    'current_helpdesk_sla_breach_rate': float(current.sla_breach.mean()),
    'current_helpdesk_sla_breaches': int(current.sla_breach.sum()),
    'annual_avoided_transfers_at_20pct': float(avoid),
    'annual_transfer_cost_avoidance_at_20pct': float(savings),
    'annual_explicit_nonbilling_handoffs': float(annual_explicit),
}

pd.DataFrame([metrics]).to_json(EVIDENCE_DIR / 'metrics.json', orient='records', indent=2)
print(f"Saved: {EVIDENCE_DIR / 'metrics.json'}")

# QA sample: 60-ticket fixed sample with verified analyst gold labels
sample = tickets[(tickets.created_at >= '2025-01-01') & (tickets.created_at < '2026-07-01')].sample(60, random_state=999).copy().reset_index(drop=True)
qa = classify_dataframe(sample)
gold = ["Audio Quality","Warranty & Repair","App & Firmware","Delivery & Shipping","Delivery & Shipping","Charging & Battery","Delivery & Shipping","Delivery & Shipping","Returns & Refunds","Delivery & Shipping","Product Enquiry","App & Firmware","Delivery & Shipping","Charging & Battery","Delivery & Shipping","Charging & Battery","Delivery & Shipping","Delivery & Shipping","Billing & Payments","Delivery & Shipping","Billing & Payments","Charging & Battery","Returns & Refunds","Billing & Payments","Returns & Refunds","Billing & Payments","Billing & Payments","Delivery & Shipping","Audio Quality","Billing & Payments","Connectivity","Returns & Refunds","Delivery & Shipping","Account & Login","Connectivity","Returns & Refunds","Account & Login","Billing & Payments","Delivery & Shipping","Warranty & Repair","App & Firmware","Delivery & Shipping","Charging & Battery","Delivery & Shipping","Connectivity","Product Enquiry","Connectivity","Connectivity","Delivery & Shipping","Returns & Refunds","Returns & Refunds","Billing & Payments","Delivery & Shipping","App & Firmware","Account & Login","Connectivity","Delivery & Shipping","Account & Login","App & Firmware","Account & Login"]
qa['reviewed_category'] = gold
qa['correct'] = qa.ai_category.eq(qa.reviewed_category)
qa[['ticket_id','category','ai_category','reviewed_category','correct','customer_message']].to_csv(EVIDENCE_DIR / 'qa_sample.csv', index=False)
print(f"Saved: {EVIDENCE_DIR / 'qa_sample.csv'}")

print(f"QA evaluation: {qa.correct.sum()}/{len(qa)} correct ({qa.correct.mean():.1%}), errors: {(~qa.correct).sum()}")
print("Key metrics:", metrics)
