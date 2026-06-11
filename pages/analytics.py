import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from collections import Counter
from database import get_all_candidates, get_candidate_by_id, get_all_uploads, get_connection
import sqlite3

def render():
    st.markdown('<p class="page-title">Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Deep insights into your recruitment pipeline and talent pool.</p>', unsafe_allow_html=True)

    candidates = get_all_candidates()
    uploads = get_all_uploads()

    if not candidates:
        st.markdown('<div class="alert-info">No data available. Upload resumes to see analytics!</div>', unsafe_allow_html=True)
        return

    df = pd.DataFrame(candidates)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Candidates", len(candidates))
    with c2: st.metric("Avg ATS Score", f"{df['ats_score'].mean():.1f}%")
    with c3: st.metric("Avg Resume Score", f"{df['resume_score'].mean():.1f}%")
    with c4: st.metric("High Scorers (70+)", len(df[df['ats_score'] >= 70]))

    st.markdown("<br>", unsafe_allow_html=True)

    all_skills = []
    for c in candidates:
        full = get_candidate_by_id(c["id"])
        all_skills.extend(full.get("skills", []))

    col1, col2 = st.columns(2)
    with col1:
        if all_skills:
            skill_counts = Counter(all_skills).most_common(15)
            skills_df = pd.DataFrame(skill_counts, columns=["Skill","Count"])
            fig = px.bar(skills_df, x="Count", y="Skill", orientation="h",
                         title="Top Skills Distribution",
                         color="Count", color_continuous_scale=["#BFDBFE","#1D4ED8"])
            fig.update_layout(height=420, margin=dict(l=10,r=20,t=50,b=10),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font=dict(family='Inter',size=11), coloraxis_showscale=False,
                              yaxis=dict(categoryorder='total ascending'))
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(x=df["ats_score"], name="ATS Score", nbinsx=10,
                                    marker_color="#2563EB", marker_line_width=0, opacity=0.8))
        fig2.add_trace(go.Histogram(x=df["resume_score"], name="Resume Score", nbinsx=10,
                                    marker_color="#059669", marker_line_width=0, opacity=0.8))
        fig2.update_layout(title="Score Distribution", barmode="overlay", height=420,
                           margin=dict(l=10,r=10,t=50,b=10),
                           paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font=dict(family='Inter',size=11),
                           legend=dict(orientation="h",yanchor="bottom",y=1.02),
                           xaxis_title="Score (%)", yaxis_title="Count")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT degree, COUNT(*) as cnt FROM education GROUP BY degree ORDER BY cnt DESC LIMIT 10")
        edu_data = [(r["degree"], r["cnt"]) for r in cur.fetchall()]
        conn.close()
        if edu_data:
            edu_df = pd.DataFrame(edu_data, columns=["Degree","Count"])
            fig3 = px.pie(edu_df, names="Degree", values="Count", title="Education Distribution",
                          color_discrete_sequence=px.colors.qualitative.Set2)
            fig3.update_layout(height=350, margin=dict(l=10,r=10,t=50,b=10),
                               paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter',size=11))
            fig3.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig3, use_container_width=True)

    with col4:
        if all_skills and len(all_skills) > 3:
            top5 = Counter(all_skills).most_common(5)
            skill_names = [s[0] for s in top5]
            skill_vals = [s[1] for s in top5]
            skill_pct = [v/len(candidates)*100 for v in skill_vals]
            fig4 = go.Figure(go.Bar(
                x=skill_names, y=skill_pct,
                marker_color=["#2563EB","#7C3AED","#0891B2","#059669","#D97706"],
                marker_line_width=0, text=[f"{v:.0f}%" for v in skill_pct], textposition='outside'
            ))
            fig4.update_layout(title="Skill Penetration (%)", height=350,
                               margin=dict(l=10,r=10,t=50,b=10),
                               paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               font=dict(family='Inter',size=11), showlegend=False,
                               yaxis_title="% of Candidates with Skill")
            st.plotly_chart(fig4, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        if df["ats_score"].notna().sum() >= 2:
            def score_group(s):
                if s >= 70: return "High (70-100)"
                elif s >= 40: return "Medium (40-70)"
                else: return "Low (0-40)"
            df["Score Group"] = df["ats_score"].apply(score_group)
            group_counts = df["Score Group"].value_counts().reset_index()
            group_counts.columns = ["Group","Count"]
            fig5 = px.bar(group_counts, x="Group", y="Count", title="Candidate Score Categories",
                          color="Group", color_discrete_map={
                              "High (70-100)":"#22C55E", "Medium (40-70)":"#F59E0B", "Low (0-40)":"#EF4444"})
            fig5.update_layout(height=300, margin=dict(l=10,r=10,t=50,b=10),
                               paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               font=dict(family='Inter',size=11), showlegend=False)
            fig5.update_traces(marker_line_width=0)
            st.plotly_chart(fig5, use_container_width=True)

    with col6:
        conn2 = get_connection()
        conn2.row_factory = sqlite3.Row
        cur2 = conn2.cursor()
        cur2.execute("SELECT DATE(upload_date) as date, COUNT(*) as cnt FROM uploads GROUP BY DATE(upload_date) ORDER BY date DESC LIMIT 30")
        trend_data = [(r["date"], r["cnt"]) for r in cur2.fetchall()]
        conn2.close()
        if trend_data:
            trend_df = pd.DataFrame(trend_data, columns=["Date","Uploads"])
            trend_df = trend_df.sort_values("Date")
            fig6 = px.line(trend_df, x="Date", y="Uploads", title="Upload Trend",
                           markers=True, line_shape="spline")
            fig6.update_traces(line_color="#2563EB", marker_color="#2563EB", marker_size=8)
            fig6.update_layout(height=300, margin=dict(l=10,r=10,t=50,b=10),
                               paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               font=dict(family='Inter',size=11))
            st.plotly_chart(fig6, use_container_width=True)

    if all_skills and len(Counter(all_skills)) >= 8:
        st.markdown("#### Skills Radar Chart (Top 8)")
        top8 = Counter(all_skills).most_common(8)
        snames = [s[0] for s in top8]
        svals = [s[1] for s in top8]
        max_val = max(svals) if svals else 1
        norm = [v/max_val * 100 for v in svals]

        fig7 = go.Figure(go.Scatterpolar(
            r=norm + [norm[0]], theta=snames + [snames[0]],
            fill='toself', fillcolor='rgba(37,99,235,0.15)',
            line=dict(color='#2563EB', width=2),
            marker=dict(color='#2563EB', size=6)
        ))
        fig7.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])),
                           title="Top Skills Radar", height=400,
                           margin=dict(l=30,r=30,t=60,b=30),
                           paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter',size=11))
        st.plotly_chart(fig7, use_container_width=True)
