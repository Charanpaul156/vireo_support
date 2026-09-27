import io
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from classifier import classify_dataframe

st.set_page_config(page_title='Vireo Audio Support Categoriser', layout='wide')
st.title('Vireo Audio — AI-assisted Support Categoriser')
st.caption('Local, API-free classifier. Text rules take precedence; the exported intake tag is used only as a fallback. Confidence is heuristic, not a calibrated probability.')

uploaded = st.file_uploader('Upload tickets.csv', type='csv')
if uploaded is None:
    st.info('Upload the supplied tickets.csv to begin.')
    st.stop()

df = pd.read_csv(uploaded)
for c in ['created_at','first_response_at','resolved_at']:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors='coerce')

start = pd.Timestamp('2025-01-01')
end = pd.Timestamp('2026-07-01')
df = df[(df.created_at >= start) & (df.created_at < end)].copy()
classified = classify_dataframe(df)
classified['month'] = classified.created_at.dt.to_period('M').astype(str)

c1,c2,c3,c4 = st.columns(4)
c1.metric('Tickets in scope', f'{len(classified):,}')
c2.metric('Text-rule classified', f"{(classified.classification_method=='text_rule').mean():.0%}")
c3.metric('Fallback to source tag', f"{(classified.classification_method=='source_tag_fallback').mean():.0%}")
c4.metric('Low-confidence/unresolved', f"{(classified.decision_confidence<0.5).mean():.0%}")

st.subheader('Monthly volume by AI category')
cat = classified.pivot_table(index='month', columns='ai_category', values='ticket_id', aggfunc='count', fill_value=0)
st.line_chart(cat)

st.subheader('Monthly volume by first-assigned team')
team = classified.pivot_table(index='month', columns='assigned_team', values='ticket_id', aggfunc='count', fill_value=0)
st.line_chart(team)

st.subheader('Category totals')
st.dataframe(classified['ai_category'].value_counts().rename('tickets').to_frame())

st.subheader('Classification output')
st.dataframe(classified[['ticket_id','created_at','category','ai_category','classification_method','decision_confidence','assigned_team','customer_message']], use_container_width=True)

buf = io.BytesIO()
classified.to_csv(buf, index=False)
st.download_button('Download classified CSV', buf.getvalue(), 'vireo_classified_tickets.csv', 'text/csv')
