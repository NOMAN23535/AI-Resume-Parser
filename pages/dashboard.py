import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from database import get_dashboard_stats, get_all_candidates, get_all_uploads, get_all_jobs

def make_gauge(value, title, color="#2563EB"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 14, 'color': '#64748B', 'family': 'Inter'}},
        number={'suffix': '%', 'font': {'size': 28, 'color': '#0F172A', 'family': 'Inter'}, 'valueformat': '.0f'},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#CBD5E1", 'tickfont': {'size': 10}},
            'bar': {'color': color, 'thickness': 0.25},
            'bgcolor': "white",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': '#FEE2E2'},
                {'range': [40, 70], 'color': '#FEF9C3'},
                {'range': [70, 100], 'color': '#DCFCE7'}
            ],
            'threshold': {'line': {'color': color, 'width': 3}, 'thickness': 0.75, 'value': value}
        }
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=10),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(family='Inter'))
    return fig

def render():
    stats = get_dashboard_stats()
    candidates = get_all_candidates()
    uploads = get_all_uploads()

    st.markdown('<p class="page-title">Resume Parser AI Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Welcome back! Here\'s what\'s happening with your recruitment pipeline.</p>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpis = [
        (c1, stats["total_candidates"], "Total Candidates", "#2563EB"),
        (c2, stats["total_jobs"], "Total Jobs", "#7C3AED"),
        (c3, f"{stats['avg_ats']}%", "Avg ATS Score", "#0891B2"),
        (c4, f"{stats['avg_resume']}%", "Avg Resume Score", "#059669"),
        (c5, stats["total_matches"], "Total Matches", "#D97706"),
        (c6, stats["new_this_month"], "New This Month", "#DC2626"),
    ]
    for col, value, label, color in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value" style="color:{color}">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><div class="card-title">Average ATS Score</div>', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(stats["avg_ats"], "ATS Score", "#2563EB"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><div class="card-title">Average Resume Score</div>', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(stats["avg_resume"], "Resume Score", "#059669"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if candidates:
        from collections import Counter
        all_skills = []
        for c in candidates:
            from database import get_candidate_by_id
            full = get_candidate_by_id(c["id"])
            all_skills.extend(full.get("skills", []))

        col3, col4 = st.columns(2)
        with col3:
            if all_skills:
                skill_counts = Counter(all_skills).most_common(12)
                skills_df = pd.DataFrame(skill_counts, columns=["Skill", "Count"])
                fig = px.bar(skills_df, x="Count", y="Skill", orientation="h",
                             title="Top Skills Distribution",
                             color="Count", color_continuous_scale=["#BFDBFE", "#2563EB"])
                fig.update_layout(height=340, margin=dict(l=10, r=10, t=40, b=10),
                                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                  font=dict(family='Inter', size=11),
                                  showlegend=False, coloraxis_showscale=False,
                                  yaxis=dict(categoryorder='total ascending'))
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)

        with col4:
            if len(candidates) >= 1:
                df = pd.DataFrame(candidates)
                top10 = df.nlargest(10, "ats_score")[["name","ats_score","resume_score"]]
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(x=top10["name"], y=top10["ats_score"], name="ATS Score",
                                      marker_color="#2563EB", marker_line_width=0))
                fig2.add_trace(go.Bar(x=top10["name"], y=top10["resume_score"], name="Resume Score",
                                      marker_color="#059669", marker_line_width=0))
                fig2.update_layout(title="Top Candidate Rankings", height=340, barmode="group",
                                   margin=dict(l=10, r=10, t=40, b=60),
                                   paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family='Inter', size=11),
                                   xaxis=dict(tickangle=-30), legend=dict(orientation="h", yanchor="bottom", y=1.02))
                st.plotly_chart(fig2, use_container_width=True)

        col5, col6 = st.columns(2)
        with col5:
            from database import get_connection
            conn = get_connection()
            import sqlite3
            conn.row_factory = sqlite3.Row
            c_cur = conn.cursor()
            c_cur.execute("SELECT degree, COUNT(*) as cnt FROM education GROUP BY degree ORDER BY cnt DESC LIMIT 8")
            edu_data = c_cur.fetchall()
            conn.close()
            if edu_data:
                edu_df = pd.DataFrame([(r["degree"], r["cnt"]) for r in edu_data], columns=["Degree","Count"])
                fig3 = px.pie(edu_df, names="Degree", values="Count", title="Education Distribution",
                              color_discrete_sequence=px.colors.sequential.Blues_r)
                fig3.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10),
                                   paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter', size=11))
                fig3.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig3, use_container_width=True)

        with col6:
            if len(candidates) >= 2:
                df2 = pd.DataFrame(candidates)
                fig4 = px.histogram(df2, x="ats_score", nbins=10, title="ATS Score Distribution",
                                    color_discrete_sequence=["#2563EB"])
                fig4.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10),
                                   paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family='Inter', size=11), showlegend=False)
                fig4.update_traces(marker_line_width=0)
                st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">Recent Uploads</p>', unsafe_allow_html=True)

    if uploads:
        recent = uploads[:10]
        df_up = pd.DataFrame(recent)[["file_name","candidate_name","ats_score","resume_score","upload_date"]]
        df_up.columns = ["File Name","Candidate","ATS Score","Resume Score","Upload Date"]
        df_up["Upload Date"] = pd.to_datetime(df_up["Upload Date"]).dt.strftime("%Y-%m-%d %H:%M")
        st.dataframe(df_up, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="alert-info">No uploads yet. Go to <b>Upload Resume</b> to get started!</div>', unsafe_allow_html=True)
