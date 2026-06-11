import streamlit as st
import os
import time
from datetime import datetime
from parser.resume_parser import parse_resume
from database import insert_candidate, insert_upload_log

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def format_size(size_bytes):
    if size_bytes < 1024: return f"{size_bytes} B"
    elif size_bytes < 1024*1024: return f"{size_bytes/1024:.1f} KB"
    else: return f"{size_bytes/(1024*1024):.1f} MB"

def process_file(uploaded_file):
    file_bytes = uploaded_file.read()
    file_size = format_size(len(file_bytes))
    save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(file_bytes)
    parsed = parse_resume(file_bytes, uploaded_file.name)
    parsed["file_path"] = save_path
    candidate_id = insert_candidate(parsed)
    insert_upload_log({
        "file_name": uploaded_file.name,
        "candidate_name": parsed.get("name",""),
        "candidate_id": candidate_id,
        "file_size": file_size,
        "ats_score": parsed.get("ats_score",0),
        "resume_score": parsed.get("resume_score",0),
    })
    return parsed, candidate_id, file_size

def render():
    st.markdown('<p class="page-title">Upload Resume</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Upload one or multiple resumes for AI-powered parsing and scoring.</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Single Resume", "Multiple Resumes"])

    with tab1:
        st.markdown("""
        <div class="upload-area">
            <div class="upload-title">Upload a Single Resume</div>
            <div class="upload-subtitle">Supported formats: PDF, DOCX • Max size: 10MB</div>
        </div>""", unsafe_allow_html=True)

        uploaded = st.file_uploader("Choose a resume file", type=["pdf","docx"], key="single_upload",
                                     label_visibility="collapsed")
        if uploaded:
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                st.markdown(f"**{uploaded.name}**")
            with col2:
                st.markdown(f"{format_size(uploaded.size)}")
            with col3:
                st.markdown(f"{datetime.now().strftime('%H:%M:%S')}")

            if st.button("Parse & Analyze Resume", type="primary", use_container_width=True):
                with st.spinner("Analyzing resume with AI..."):
                    try:
                        progress = st.progress(0)
                        progress.progress(20, "Extracting text...")
                        time.sleep(0.3)
                        progress.progress(50, "Running NLP analysis...")
                        parsed, cid, fsize = process_file(uploaded)
                        progress.progress(80, "Calculating scores...")
                        time.sleep(0.2)
                        progress.progress(100, "Complete!")
                        time.sleep(0.3)
                        progress.empty()

                        st.markdown(f'<div class="alert-success">Resume parsed successfully! Candidate ID: #{cid}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)

                        col_a, col_b, col_c, col_d = st.columns(4)
                        with col_a:
                            st.metric("ATS Score", f"{parsed['ats_score']}%")
                        with col_b:
                            st.metric("Resume Score", f"{parsed['resume_score']}%")
                        with col_c:
                            st.metric("Skills Found", len(parsed.get("skills",[])))
                        with col_d:
                            st.metric("Experience Entries", len(parsed.get("experience",[])))

                        st.markdown("<br>", unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### Extracted Information")
                            info = {
                                "Name": parsed.get("name","—"),
                                "Email": parsed.get("email","—"),
                                "Phone": parsed.get("phone","—"),
                                "Location": parsed.get("location","—"),
                                "LinkedIn": parsed.get("linkedin","—"),
                                "GitHub": parsed.get("github","—"),
                            }
                            for k, v in info.items():
                                st.markdown(f"**{k}:** {v}")

                        with col2:
                            st.markdown("#### Skills Detected")
                            if parsed.get("skills"):
                                skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in parsed["skills"]])
                                st.markdown(skills_html, unsafe_allow_html=True)
                            else:
                                st.markdown("No skills detected")

                        if parsed.get("education"):
                            st.markdown("#### Education")
                            for edu in parsed["education"]:
                                st.markdown(f"• **{edu.get('degree','')}** — {edu.get('institution','')} {edu.get('year','')}")

                        if parsed.get("experience"):
                            st.markdown("#### Experience")
                            for exp in parsed["experience"]:
                                company_text = f"at {exp['company']}" if exp.get('company') else ""
                                st.markdown(f"• **{exp.get('title','')}** {company_text} {exp.get('duration','')}")

                        if parsed.get("certifications"):
                            st.markdown("#### Certifications")
                            for cert in parsed["certifications"]:
                                st.markdown(f"• {cert.get('cert_name', cert.get('name',''))}")

                    except Exception as e:
                        st.error(f"Error processing resume: {str(e)}")

    with tab2:
        st.markdown("""
        <div class="upload-area">
            <div class="upload-title">Bulk Resume Upload</div>
            <div class="upload-subtitle">Upload multiple resumes at once • PDF and DOCX supported</div>
        </div>""", unsafe_allow_html=True)

        uploaded_files = st.file_uploader("Choose multiple resume files", type=["pdf","docx"],
                                           accept_multiple_files=True, key="multi_upload",
                                           label_visibility="collapsed")
        if uploaded_files:
            st.markdown(f"**{len(uploaded_files)} file(s) selected:**")
            for f in uploaded_files:
                st.markdown(f"• {f.name} ({format_size(f.size)})")

            if st.button(f"Parse All {len(uploaded_files)} Resumes", type="primary", use_container_width=True):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()

                for i, uploaded in enumerate(uploaded_files):
                    status_text.markdown(f"Processing **{uploaded.name}** ({i+1}/{len(uploaded_files)})...")
                    try:
                        parsed, cid, fsize = process_file(uploaded)
                        results.append({
                            "File": uploaded.name,
                            "Candidate": parsed.get("name","Unknown"),
                            "Email": parsed.get("email","—"),
                            "Skills": len(parsed.get("skills",[])),
                            "ATS Score": f"{parsed['ats_score']}%",
                            "Resume Score": f"{parsed['resume_score']}%",
                            "Status": "Success",
                            "ID": f"#{cid}"
                        })
                    except Exception as e:
                        results.append({
                            "File": uploaded.name,
                            "Candidate": "—",
                            "Email": "—",
                            "Skills": 0,
                            "ATS Score": "—",
                            "Resume Score": "—",
                            "Status": "Error",
                            "ID": "—"
                        })
                    progress_bar.progress((i+1)/len(uploaded_files))

                status_text.empty()
                progress_bar.empty()

                success_count = sum(1 for r in results if r["Status"] == "Success")
                st.markdown(f'<div class="alert-success">Processed {success_count}/{len(uploaded_files)} resumes successfully!</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                import pandas as pd
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, hide_index=True)
