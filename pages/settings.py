import streamlit as st
import os
import platform
from database import get_db_stats
from parser.resume_parser import SKILLS_DB

def render():
    st.markdown('<p class="page-title">Settings</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">System configuration, database info, and model details.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Database Stats", "Model Info", "System Info"])

    with tab1:
        st.markdown("#### Database Statistics")
        stats = get_db_stats()
        items = [
            ("Candidates", stats["candidates"], "#2563EB"),
            ("Skills Records", stats["skills"], "#7C3AED"),
            ("Education Records", stats["education"], "#0891B2"),
            ("Experience Records", stats["experience"], "#059669"),
            ("Certifications", stats["certifications"], "#D97706"),
            ("Projects", stats["projects"], "#DC2626"),
            ("Jobs", stats["jobs"], "#2563EB"),
            ("Job Matches", stats["job_matches"], "#7C3AED"),
            ("Upload Logs", stats["uploads"], "#0891B2"),
        ]
        cols = st.columns(3)
        for i, (label, value, color) in enumerate(items):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="kpi-card" style="margin-bottom:12px;">
                    <div class="kpi-value" style="color:{color};font-size:24px;">{value}</div>
                    <div class="kpi-label">{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "recruitment.db")
        if os.path.exists(db_path):
            size = os.path.getsize(db_path) / 1024
            st.info(f"Database: `{db_path}` — Size: **{size:.1f} KB**")
        else:
            st.warning("Database file not found.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Danger Zone")
        with st.expander("Clear Database"):
            st.warning("This will permanently delete ALL data!")
            confirm = st.text_input("Type 'DELETE ALL' to confirm")
            if st.button("Clear All Data", type="primary"):
                if confirm == "DELETE ALL":
                    import sqlite3
                    conn = sqlite3.connect(db_path)
                    c = conn.cursor()
                    for table in ["candidates","skills","education","experience","certifications","projects","jobs","job_matches","uploads"]:
                        c.execute(f"DELETE FROM {table}")
                    conn.commit()
                    conn.close()
                    st.success("All data cleared!")
                    st.rerun()
                else:
                    st.error("Incorrect confirmation text.")

    with tab2:
        st.markdown("#### AI Models")
        st.markdown("""
        <div class="card">
            <div class="card-title">NLP Parser — SpaCy</div>
            <div style="font-size:14px;color:#374151;">
                <b>Model:</b> en_core_web_sm<br>
                <b>Purpose:</b> Named Entity Recognition (NER) for extracting names, locations<br>
                <b>Tasks:</b> PERSON detection, GPE/LOC detection<br>
                <b>Install:</b> <code>python -m spacy download en_core_web_sm</code>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">Semantic Matching — Sentence Transformers</div>
            <div style="font-size:14px;color:#374151;">
                <b>Model:</b> all-MiniLM-L6-v2<br>
                <b>Purpose:</b> Semantic similarity between resumes and job descriptions<br>
                <b>Output:</b> Cosine similarity score (0-100%)<br>
                <b>Provider:</b> HuggingFace / sentence-transformers library
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="card-title">Skills Database</div>
            <div style="font-size:14px;color:#374151;">
                <b>Total Skills:</b> {len(SKILLS_DB)}<br>
                <b>Detection:</b> Regex-based keyword matching<br>
                <b>Coverage:</b> Languages, Frameworks, Tools, Cloud, Data Science, DevOps
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("#### Skills Database Preview")
        cols = st.columns(5)
        for i, skill in enumerate(SKILLS_DB):
            with cols[i % 5]:
                st.markdown(f'<span class="skill-tag" style="display:block;margin:2px;text-align:center;">{skill}</span>', unsafe_allow_html=True)

    with tab3:
        st.markdown("#### System Information")
        import sys
        info = {
            "Python Version": sys.version.split()[0],
            "OS": platform.system() + " " + platform.release(),
            "Architecture": platform.machine(),
            "Working Directory": os.getcwd(),
            "Upload Directory": os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads"),
            "Export Directory": os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports"),
        }

        for k, v in info.items():
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown(f"**{k}**")
            with col2:
                st.markdown(f"`{v}`")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Required Packages")
        packages = [
            ("streamlit",">=1.32.0","Web Framework"),
            ("pdfplumber",">=0.10.0","PDF Parsing"),
            ("python-docx",">=1.1.0","DOCX Parsing"),
            ("spacy",">=3.7.0","NLP / NER"),
            ("sentence-transformers",">=2.6.0","AI Matching"),
            ("plotly",">=5.20.0","Charts"),
            ("pandas",">=2.2.0","Data Processing"),
            ("openpyxl",">=3.1.0","Excel Export"),
            ("reportlab",">=4.1.0","PDF Export"),
        ]
        import pandas as pd
        df = pd.DataFrame(packages, columns=["Package","Version","Purpose"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Quick Setup Commands")
        st.code("""# Install dependencies
pip install -r requirements.txt

# Download SpaCy model
python -m spacy download en_core_web_sm

# Run the application
streamlit run app.py""", language="bash")
