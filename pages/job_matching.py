import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from database import insert_job, get_all_jobs, get_all_candidates, get_candidate_by_id, delete_job, insert_job_match, get_matches_for_job
from services.matching import rank_candidates_for_job

COMMON_SKILLS = [
    "Python","Java","C++","JavaScript","TypeScript","React","Next.js","Node.js","MongoDB",
    "MySQL","PostgreSQL","AWS","Docker","Git","Machine Learning","Deep Learning","NLP",
    "TensorFlow","PyTorch","Django","Flask","FastAPI","HTML","CSS","Tailwind","SQL",
    "Data Science","Kubernetes","Redis","GraphQL","Vue.js","Angular"
]

def render_create_job():
    st.markdown("### Create New Job")
    with st.form("create_job_form"):
        job_title = st.text_input("Job Title *", placeholder="e.g. Senior Python Developer")
        col1, col2 = st.columns(2)
        with col1:
            exp_req = st.text_input("Experience Required", placeholder="e.g. 3-5 years")
        with col2:
            edu_req = st.text_input("Education Required", placeholder="e.g. Bachelor's in CS")

        req_skills = st.multiselect("Required Skills", COMMON_SKILLS, placeholder="Select required skills")
        extra_skills = st.text_input("Add more skills (comma-separated)", placeholder="e.g. Redis, Kafka, Terraform")
        job_desc = st.text_area("Job Description *", height=180, placeholder="Describe the role, responsibilities, requirements...")

        submitted = st.form_submit_button("Save Job", type="primary", use_container_width=True)
        if submitted:
            if not job_title or not job_desc:
                st.error("Job title and description are required!")
            else:
                all_skills = list(req_skills)
                if extra_skills:
                    all_skills += [s.strip() for s in extra_skills.split(",") if s.strip()]
                jid = insert_job({
                    "title": job_title,
                    "required_skills": all_skills,
                    "experience_required": exp_req,
                    "education_required": edu_req,
                    "description": job_desc,
                })
                st.success(f"Job '{job_title}' created successfully! (ID: #{jid})")
                st.rerun()

def render_match_job(job):
    st.markdown(f"### Matching: **{job['title']}**")
    st.markdown(f"*Experience:* {job.get('experience_required','N/A')} &nbsp;|&nbsp; *Education:* {job.get('education_required','N/A')}")

    if job.get("required_skills"):
        skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in job["required_skills"]])
        st.markdown(f"**Required Skills:** {skills_html}", unsafe_allow_html=True)

    if st.button("Run Matching Engine", type="primary"):
        with st.spinner("Running semantic matching..."):
            candidates_raw = get_all_candidates()
            candidates = [get_candidate_by_id(c["id"]) for c in candidates_raw]

            if not candidates:
                st.warning("No candidates in database. Upload resumes first!")
                return

            results = rank_candidates_for_job(candidates, job)

            for r in results:
                insert_job_match({
                    "job_id": job["id"],
                    "candidate_id": r["candidate_id"],
                    "match_score": r["match_score"],
                    "matched_skills": r["matched_skills"],
                    "missing_skills": r["missing_skills"],
                })

            st.success(f"Matched {len(results)} candidates!")
            render_results(results, job)

    saved = get_matches_for_job(job["id"])
    if saved and not st.session_state.get(f"just_ran_{job['id']}", False):
        st.markdown("---")
        st.markdown("#### Previous Match Results")
        render_saved_matches(saved, job)

def render_results(results, job):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Candidate Rankings")

    if not results:
        st.info("No results found.")
        return

    names = [r["name"] for r in results[:10]]
    scores = [r["match_score"] for r in results[:10]]
    colors = ["#2563EB" if i == 0 else "#3B82F6" if i < 3 else "#93C5FD" for i in range(len(names))]

    fig = go.Figure(go.Bar(
        x=scores, y=names, orientation='h',
        marker_color=colors, marker_line_width=0,
        text=[f"{s:.1f}%" for s in scores], textposition='inside',
        textfont=dict(color='white', size=12, family='Inter')
    ))
    fig.update_layout(
        title=f"Top Candidates for: {job['title']}",
        height=max(300, len(names)*40+60),
        margin=dict(l=10, r=40, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12),
        xaxis=dict(range=[0,100], title="Match Score (%)", gridcolor='#F1F5F9'),
        yaxis=dict(categoryorder='total ascending'),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Detailed Results")
    for i, r in enumerate(results):
        rank_label = f"#{i+1}"
        matched_html = "".join([f'<span class="skill-tag skill-tag-matched">{s}</span>' for s in r.get("matched_skills",[])])
        missing_html = "".join([f'<span class="skill-tag skill-tag-missing">{s}</span>' for s in r.get("missing_skills",[])])

        with st.expander(f"{rank_label} {r['name']} — Match: {r['match_score']:.1f}%"):
            colA, colB, colC = st.columns(3)
            colA.metric("Match Score", f"{r['match_score']:.1f}%")
            colB.metric("ATS Score", f"{r['ats_score']}%")
            colC.metric("Resume Score", f"{r['resume_score']}%")
            if matched_html:
                st.markdown(f"**Matched Skills:** {matched_html}", unsafe_allow_html=True)
            if missing_html:
                st.markdown(f"**Missing Skills:** {missing_html}", unsafe_allow_html=True)

def render_saved_matches(saved, job):
    if not saved:
        return
    names = [r["name"] for r in saved[:8]]
    scores = [r["match_score"] for r in saved[:8]]
    fig = go.Figure(go.Bar(
        x=scores, y=names, orientation='h',
        marker_color="#93C5FD", marker_line_width=0,
        text=[f"{s:.1f}%" for s in scores], textposition='inside',
    ))
    fig.update_layout(height=max(250, len(names)*40+60), margin=dict(l=10, r=40, t=20, b=20),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(family='Inter', size=11),
                      xaxis=dict(range=[0,100], gridcolor='#F1F5F9'),
                      yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig, use_container_width=True)

def render():
    st.markdown('<p class="page-title">Job Matching</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Create job descriptions and use AI to match and rank candidates.</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Create Job", "All Jobs"])

    with tab1:
        render_create_job()

    with tab2:
        jobs = get_all_jobs()
        if not jobs:
            st.markdown('<div class="alert-info">No jobs yet. Create one in the "Create Job" tab!</div>', unsafe_allow_html=True)
            return

        st.markdown(f"**{len(jobs)} job(s) in database**")
        for job in jobs:
            skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in job.get("required_skills",[])[:6]])
            col1, col2, col3 = st.columns([5,1,1])
            with col1:
                st.markdown(f"""
                <div class="job-card">
                    <div class="job-title">{job['title']}</div>
                    <div class="job-meta">
                        {('Exp: ' + job['experience_required']) if job.get('experience_required') else ''}
                        {('&nbsp;&nbsp;Education: ' + job['education_required']) if job.get('education_required') else ''}
                        <span style="color:#94A3B8;">&nbsp;&nbsp;{job.get('created_at','')[:10]}</span>
                    </div>
                    <div style="margin-top:8px;">{skills_html}</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Match", key=f"match_{job['id']}", use_container_width=True):
                    st.session_state["match_job_id"] = job["id"]
                    st.rerun()
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Delete", key=f"deljob_{job['id']}", use_container_width=True):
                    delete_job(job["id"])
                    st.rerun()

        if "match_job_id" in st.session_state:
            from database import get_job_by_id
            selected_job = get_job_by_id(st.session_state["match_job_id"])
            if selected_job:
                st.markdown("---")
                render_match_job(selected_job)
