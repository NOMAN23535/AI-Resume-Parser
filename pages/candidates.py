import streamlit as st
import pandas as pd
from database import get_all_candidates, get_candidate_by_id, delete_candidate, update_candidate
from services.export import export_single_pdf, export_to_json, export_to_csv, export_to_excel
import json

def get_score_class(score):
    if score >= 70: return "score-high"
    elif score >= 40: return "score-medium"
    else: return "score-low"

def render_profile(cid):
    c = get_candidate_by_id(cid)
    if not c:
        st.error("Candidate not found")
        return

    if st.button("Back to Candidates", key="back_btn"):
        st.session_state.pop("view_candidate_id", None)
        st.rerun()

    st.markdown(f"""
    <div class="profile-header">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
            <div>
                <div class="profile-name">{c.get('name','Unknown')}</div>
                <div class="profile-meta">
                    {c['email'] if c.get('email') else ''}
                    {'&nbsp;&nbsp;' + c['phone'] if c.get('phone') else ''}
                    {'&nbsp;&nbsp;' + c['location'] if c.get('location') else ''}
                </div>
                <div style="margin-top:8px;">
                    {f'<a href="{c["linkedin"]}" style="color:#93C5FD;font-size:13px;">LinkedIn</a>&nbsp;&nbsp;' if c.get('linkedin') else ''}
                    {f'<a href="{c["github"]}" style="color:#93C5FD;font-size:13px;">GitHub</a>' if c.get('github') else ''}
                </div>
            </div>
            <div style="display:flex;gap:16px;">
                <div class="profile-score-card">
                    <div class="profile-score-value">{c.get('ats_score',0)}%</div>
                    <div class="profile-score-label">ATS Score</div>
                </div>
                <div class="profile-score-card">
                    <div class="profile-score-value">{c.get('resume_score',0)}%</div>
                    <div class="profile-score-label">Resume Score</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
    with col_dl1:
        pdf_data = export_single_pdf(c)
        if pdf_data:
            st.download_button("PDF Report", pdf_data, f"{c.get('name','candidate')}_report.pdf", "application/pdf", use_container_width=True)
    with col_dl2:
        st.download_button("JSON", export_to_json([c]), f"{c.get('name','candidate')}.json", "application/json", use_container_width=True)
    with col_dl3:
        st.download_button("CSV", export_to_csv([c]), f"{c.get('name','candidate')}.csv", "text/csv", use_container_width=True)
    with col_dl4:
        st.download_button("Excel", export_to_excel([c]), f"{c.get('name','candidate')}.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Experience", "Education", "Edit Profile"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Skills")
            if c.get("skills"):
                html = "".join([f'<span class="skill-tag">{s}</span>' for s in c["skills"]])
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.markdown("*No skills recorded*")

            if c.get("summary"):
                st.markdown("#### Summary")
                st.markdown(c["summary"])

        with col2:
            if c.get("certifications"):
                st.markdown("#### Certifications")
                for cert in c["certifications"]:
                    name = cert.get("cert_name", cert.get("name",""))
                    yr = cert.get("year","")
                    st.markdown(f"• **{name}** {yr}")

            if c.get("projects"):
                st.markdown("#### Projects")
                for proj in c["projects"]:
                    pname = proj.get("project_name", proj.get("name",""))
                    st.markdown(f"• **{pname}**")
                    if proj.get("description"):
                        st.markdown(f"  {proj['description'][:120]}...")
                    if proj.get("technologies"):
                        tech_html = "".join([f'<span class="skill-tag">{t.strip()}</span>' for t in proj["technologies"].split(",") if t.strip()])
                        st.markdown(tech_html, unsafe_allow_html=True)

    with tab2:
        if c.get("experience"):
            for exp in c["experience"]:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size:16px;font-weight:600;color:#0F172A;">{exp.get('title','')}</div>
                    <div style="font-size:13px;color:#2563EB;font-weight:500;margin:4px 0;">
                        {exp.get('company','')} {('• ' + exp['duration']) if exp.get('duration') else ''}
                    </div>
                    {f'<div style="font-size:13px;color:#64748B;margin-top:8px;">{exp.get("description","")}</div>' if exp.get('description') else ''}
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("*No experience records found*")

    with tab3:
        if c.get("education"):
            for edu in c["education"]:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size:16px;font-weight:600;color:#0F172A;">{edu.get('degree','')}</div>
                    <div style="font-size:13px;color:#2563EB;font-weight:500;margin:4px 0;">{edu.get('institution','')}</div>
                    {f'<div style="font-size:13px;color:#64748B;">Graduation Year: {edu["year"]}</div>' if edu.get('year') else ''}
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("*No education records found*")

    with tab4:
        st.markdown("#### Edit Candidate Information")
        with st.form("edit_form"):
            e_name = st.text_input("Full Name", value=c.get("name",""))
            e_email = st.text_input("Email", value=c.get("email",""))
            e_phone = st.text_input("Phone", value=c.get("phone",""))
            e_location = st.text_input("Location", value=c.get("location",""))
            e_linkedin = st.text_input("LinkedIn URL", value=c.get("linkedin",""))
            e_github = st.text_input("GitHub URL", value=c.get("github",""))
            e_summary = st.text_area("Summary", value=c.get("summary",""), height=100)
            e_skills = st.text_input("Skills (comma-separated)", value=", ".join(c.get("skills",[])))
            submitted = st.form_submit_button("Save Changes", type="primary")
            if submitted:
                skills_list = [s.strip() for s in e_skills.split(",") if s.strip()]
                update_candidate(cid, {
                    "name": e_name, "email": e_email, "phone": e_phone,
                    "location": e_location, "linkedin": e_linkedin, "github": e_github,
                    "summary": e_summary, "skills": skills_list
                })
                st.success("Profile updated successfully!")
                st.rerun()

def render():
    st.markdown('<p class="page-title">Candidates</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Manage and search all candidates in your talent pool.</p>', unsafe_allow_html=True)

    if "view_candidate_id" in st.session_state:
        render_profile(st.session_state["view_candidate_id"])
        return

    candidates = get_all_candidates()

    col_search, col_sort, col_filter = st.columns([3,1.5,1.5])
    with col_search:
        search = st.text_input("Search candidates...", placeholder="Name, email, or skills", label_visibility="collapsed")
    with col_sort:
        sort_by = st.selectbox("Sort by", ["ATS Score ↓", "Resume Score ↓", "Name A-Z", "Newest First"], label_visibility="collapsed")
    with col_filter:
        score_filter = st.selectbox("Filter Score", ["All", "High (70+)", "Medium (40-70)", "Low (<40)"], label_visibility="collapsed")

    if search:
        from database import get_candidate_by_id as gcbi
        filtered = []
        for c in candidates:
            full = gcbi(c["id"])
            skill_match = any(search.lower() in s.lower() for s in full.get("skills",[]))
            if (search.lower() in c.get("name","").lower() or
                search.lower() in c.get("email","").lower() or
                search.lower() in c.get("location","").lower() or
                skill_match):
                filtered.append(c)
        candidates = filtered

    if score_filter == "High (70+)":
        candidates = [c for c in candidates if c.get("ats_score",0) >= 70]
    elif score_filter == "Medium (40-70)":
        candidates = [c for c in candidates if 40 <= c.get("ats_score",0) < 70]
    elif score_filter == "Low (<40)":
        candidates = [c for c in candidates if c.get("ats_score",0) < 40]

    if sort_by == "ATS Score ↓":
        candidates.sort(key=lambda x: x.get("ats_score",0), reverse=True)
    elif sort_by == "Resume Score ↓":
        candidates.sort(key=lambda x: x.get("resume_score",0), reverse=True)
    elif sort_by == "Name A-Z":
        candidates.sort(key=lambda x: x.get("name",""))
    elif sort_by == "Newest First":
        candidates.sort(key=lambda x: x.get("created_at",""), reverse=True)

    st.markdown(f"<p style='color:#64748B;font-size:13px;margin:8px 0 16px;'>Showing **{len(candidates)}** candidates</p>", unsafe_allow_html=True)

    if not candidates:
        st.markdown('<div class="alert-info">No candidates found. Upload resumes to get started!</div>', unsafe_allow_html=True)
        return

    # Selection UI: allow selecting specific candidates for export
    labels = [f"{c['id']} - {c.get('name','Unknown')} ({c.get('email','')})" for c in candidates]
    if "candidate_multi" not in st.session_state:
        st.session_state["candidate_multi"] = []

    st.markdown("**Select candidates to export**")
    sel_col1, sel_col2 = st.columns([3,1])
    # Render buttons first so their actions can set flags in session_state
    with sel_col2:
        if st.button("Select All", key="select_all_btn"):
            st.session_state["select_all_request"] = True
            st.experimental_rerun()
        if st.button("Clear Selection", key="clear_sel_btn"):
            st.session_state["clear_select_request"] = True
            st.experimental_rerun()

    # Before creating the multiselect widget, handle any pending requests
    if st.session_state.get("select_all_request"):
        st.session_state["candidate_multi"] = labels
        st.session_state.pop("select_all_request", None)
    if st.session_state.get("clear_select_request"):
        st.session_state["candidate_multi"] = []
        st.session_state.pop("clear_select_request", None)

    with sel_col1:
        selected = st.multiselect("Pick candidates (use Select All/Clear for convenience)", labels, key="candidate_multi")

    # Map selected labels back to ids
    selected_ids = [int(s.split(" - ")[0]) for s in st.session_state.get("candidate_multi", [])]

    # Export controls: for selected candidates and also bulk export
    col_exp_btn = st.columns([1,1,1,3])
    with col_exp_btn[0]:
        # Export selected JSON or all if none selected
        if selected_ids:
            selected_full = [get_candidate_by_id(i) for i in selected_ids]
            st.download_button("Export Selected JSON", export_to_json(selected_full), "selected_candidates.json", "application/json", use_container_width=True, key="dl_sel_json")
        else:
            st.download_button("Export JSON", export_to_json(candidates), "candidates.json", "application/json", use_container_width=True, key="dl_all_json")
    with col_exp_btn[1]:
        if selected_ids:
            selected_full = [get_candidate_by_id(i) for i in selected_ids]
            st.download_button("Export Selected CSV", export_to_csv(selected_full), "selected_candidates.csv", "text/csv", use_container_width=True, key="dl_sel_csv")
        else:
            st.download_button("Export CSV", export_to_csv(candidates), "candidates.csv", "text/csv", use_container_width=True, key="dl_all_csv")
    with col_exp_btn[2]:
        if selected_ids:
            selected_full = [get_candidate_by_id(i) for i in selected_ids]
            st.download_button("Export Selected Excel", export_to_excel(selected_full), "selected_candidates.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, key="dl_sel_xlsx")
        else:
            st.download_button("Export Excel", export_to_excel(candidates), "candidates.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, key="dl_all_xlsx")

    st.markdown("<br>", unsafe_allow_html=True)

    for c in candidates:
        from database import get_candidate_by_id as gcbi
        full = gcbi(c["id"])
        skills_preview = full.get("skills", [])[:5]
        skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills_preview])
        if len(full.get("skills",[])) > 5:
            skills_html += f'<span class="skill-tag" style="background:#F1F5F9;color:#64748B;">+{len(full["skills"])-5} more</span>'

        ats_class = get_score_class(c.get("ats_score",0))
        res_class = get_score_class(c.get("resume_score",0))

        col1, col2 = st.columns([5,1])
        with col1:
            st.markdown(f"""
            <div class="candidate-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;">
                    <div>
                        <div class="candidate-name">{c.get('name','Unknown')}</div>
                        <div class="candidate-email">
                            {c['email'] if c.get('email') else ''}
                            {'&nbsp;&nbsp;' + c['location'] if c.get('location') else ''}
                        </div>
                        <div>{skills_html}</div>
                    </div>
                    <div style="text-align:right;">
                        <span class="score-badge {ats_class}">ATS: {c.get('ats_score',0)}%</span>&nbsp;
                        <span class="score-badge {res_class}">Resume: {c.get('resume_score',0)}%</span>
                        <div style="font-size:12px;color:#94A3B8;margin-top:6px;">{c.get('created_at','')[:10]}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("View", key=f"view_{c['id']}", use_container_width=True):
                st.session_state["view_candidate_id"] = c["id"]
                st.rerun()
            if st.button("Delete", key=f"del_{c['id']}", use_container_width=True):
                delete_candidate(c["id"])
                st.rerun()
