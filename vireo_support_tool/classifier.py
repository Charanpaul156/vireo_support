import re
import pandas as pd

LABELS = [
    'Billing & Payments','Delivery & Shipping','Returns & Refunds',
    'Connectivity','Charging & Battery','App & Firmware','Product Enquiry',
    'Audio Quality','Warranty & Repair','Account & Login','Other'
]

RULES = [
    ('Product Enquiry', r'\b(will this|will it|does .* work|can i|can .* work|compatib|compatible|before i buy|spec(?:s|ification)?|survive a shower|connect two)\b'),
    ('Billing & Payments', r'\b(duplicate|double) (payment|charge)|\bcharged twice\b|\b(payment|transaction|gateway|upi|card).*(?:failed|declined|reversed|success)\b|\b(invoice|gst invoice|coupon|discount|price adjustment|promo code)\b|\bpaid once, statement disagrees\b|\b(?:money|amount) (?:was )?(?:debited|deducted).*no (?:order|confirmation)\b|\bpayment (?:was )?deducted\b.*\bno order\b|\bpage failed after i paid\b'),
    ('Account & Login', r'\b(login|log in|otp|one[- ]time|password|sign in|account|verification code|sent me a code|locked out)\b'),
    ('Warranty & Repair', r'\b(warranty|repair|rma|service centre|service center|claim number|warranty claim|repair status)\b'),
    ('Connectivity', r'\b(pair|pairing|connect|connection|disconnect|discoverable|bluetooth)\b'),
    ('Charging & Battery', r'\b(battery|charging|charge(?:ing)?|drain|dies by|battery backup|no charge|0%)\b'),
    ('App & Firmware', r'\b(app|firmware|fw\b|update|upgrade|crash|bug|software|version|progress bar|loading screen)\b'),
    ('Delivery & Shipping', r'\b(not (?:been )?received|not delivered|haven\'t received|hasn\'t been delivered|didn[’\']t (?:receive|get)|never came|nothing at (?:my|the) door|item not with me|shipment|shipping|courier|tracking|awb|rto|reship|parcel|package|order status.*(stuck|not|haven)|delivery|delayed|dispatch|wrong (?:item|colour|color)|change (?:the )?delivery address|shipping address|wrong pincode|different colour|different color|damaged\b|crushed|cracked|still waiting for something to show up|paid.*still waiting|moved houses|old flat)\b'),
    ('Audio Quality', r'\b(audio|sound|mic|microphone|distort(?:ed|ion)?|buzz(?:ing)?|volume|one ear|left side|right side|silent|crackl(?:e|ing)?|hiss(?:ing)?|static|muffl(?:ed)?|rattl(?:e|ing)?)\b|(?:\b(?:left|right|faulty|blown|crackling|buzzing|muffled|quiet)?\s*speaker\s+(?:quality|sound|volume|crackl\w*|distort\w*|buzz\w*|static|hiss\w*|rattl\w*|muffl\w*|blown|noise|problem|issue|silent|not working|cut(?:ting)?\s*out|echo)\b|\b(?:crackl\w*|distort\w*|buzz\w*|hiss\w*|rattl\w*|muffl\w*|static|noise|sound)\s+(?:from|in|of)\s+(?:the\s+)?speaker\b)'),
    ('Returns & Refunds', r'\b(return|returned|refund (?:not|still|pending|received|credited)|still waiting for my refund|refund not received|pickup|pick up|reverse pickup|cancel|cancellation|money back|not credited|stop the shipment|change of mind|picked up the item|return was accepted|packed the box)\b'),
]

COMPILED = [(label, re.compile(pattern, re.I)) for label, pattern in RULES]

def classify_row(row):
    text = str(row.get('customer_message', '') or '')
    # Delivery takes precedence over return language when an actual fulfilment failure is stated.
    for label, rx in COMPILED:
        if label == 'Returns & Refunds':
            if rx.search(text) and not re.search(r'\b(not delivered|not received|haven\'t received|never came|nothing at (?:my|the) door|shipment|courier|tracking|awb|rto|reship|parcel|package|order status.*stuck|delivery|delayed|dispatch|paid.*still waiting|still waiting for something to show up)\b', text, re.I):
                return label, 'text_rule', 0.90
            continue
        if rx.search(text):
            return label, 'text_rule', 0.90
    tag = row.get('category')
    if tag in LABELS:
        return tag, 'source_tag_fallback', 0.55
    return 'Other', 'unresolved', 0.30

def classify_dataframe(df):
    out = df.copy()
    result = out.apply(classify_row, axis=1, result_type='expand')
    result.columns = ['ai_category','classification_method','decision_confidence']
    return pd.concat([out.reset_index(drop=True), result.reset_index(drop=True)], axis=1)
