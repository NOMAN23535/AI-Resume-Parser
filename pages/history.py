import streamlit as st
import pandas as pd
from database import get_all_uploads, delete_upload, get_candidate_by_id
from services.export import export_single_pdf, export_to_json, export_to_csv

def render():
    st.markdown('<p class="page-title">Upload History</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Track all resume uploads and their processing results.</p>', unsafe_allow_html=True)

    uploads = get_all_uploads()

    if not uploads:
        st.markdown('<div class="alert-info">No upload history yet. Upload some resumes to see history!</div>', unsafe_allow_html=True)
        return

    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Total Uploads", len(uploads))
    with col_stat2:
        avg_ats = sum(u.get("ats_score",0) for u in uploads) / len(uploads)
        st.metric("Avg ATS Score", f"{avg_ats:.1f}%")
    with col_stat3:
        avg_res = sum(u.get("resume_score",0) for u in uploads) / len(uploads)
        st.metric("Avg Resume Score", f"{avg_res:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    search = st.text_input("Search history...", placeholder="Search by file name or candidate name", label_visibility="collapsed")

    filtered = uploads
    if search:
        filtered = [u for u in uploads if search.lower() in u.get("file_name","").lower() or
                    search.lower() in u.get("candidate_name","").lower()]

    st.markdown(f"Showing **{len(filtered)}** records")
    st.markdown("<br>", unsafe_allow_html=True)

    for u in filtered:
        ats = u.get("ats_score", 0)
        res = u.get("resume_score", 0)
        ats_color = "#22C55E" if ats >= 70 else "#F59E0B" if ats >= 40 else "#EF4444"
        res_color = "#22C55E" if res >= 70 else "#F59E0B" if res >= 40 else "#EF4444"

        col1, col2, col3, col4 = st.columns([4,1,1,1])
        with col1:
            st.markdown(f"""
            <div class="candidate-card" style="cursor:default;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <div>
                        <div style="font-size:15px;font-weight:600;color:#0F172A;">{u.get('file_name','')}</div>
                        <div style="font-size:13px;color:#64748B;">
                            {u.get('candidate_name','Unknown')} &nbsp;·&nbsp;
                            {u.get('file_size','—')} &nbsp;·&nbsp;
                            {u.get('upload_date','')[:16]}
                        </div>
                    </div>
                    <div style="display:flex;gap:10px;">
                        <span style="background:#F0FDF4;color:{ats_color};border:1px solid {ats_color};border-radius:20px;padding:4px 12px;font-size:12px;font-weight:600;">
                            ATS: {ats}%
                        </span>
                        <span style="background:#F0FDF4;color:{res_color};border:1px solid {res_color};border-radius:20px;padding:4px 12px;font-size:12px;font-weight:600;">
                            Resume: {res}%
                        </span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            cid = u.get("candidate_id")
            if cid:
                cand = get_candidate_by_id(cid)
                if cand:
                    pdf_data = export_single_pdf(cand)
                    if pdf_data:
                        st.download_button("PDF", pdf_data, f"{u.get('candidate_name','report')}.pdf",
                                           "application/pdf", key=f"pdf_{u['id']}", use_container_width=True)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if cid:
                cand = get_candidate_by_id(cid)
                if cand:
                                                                                                            
                    merged = cand.copy()
                    merged["file_name"] = u.get("file_name", merged.get("file_name",""))
                    merged["file_size"] = u.get("file_size", merged.get("file_size",""))
                    merged["upload_date"] = u.get("upload_date", merged.get("created_at",""))
                    st.download_button("JSON", export_to_json([merged]), f"{u.get('candidate_name','candidate')}.json",
                                       "application/json", key=f"json_{u['id']}", use_container_width=True)
                    st.download_button("CSV", export_to_csv([merged]), f"{u.get('candidate_name','candidate')}.csv",
                                       "text/csv", key=f"csv_{u['id']}", use_container_width=True)

        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Delete", key=f"del_up_{u['id']}", use_container_width=True):
                delete_upload(u["id"])
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Clear All History", type="secondary"):
        for u in uploads:
            delete_upload(u["id"])
        st.rerun()
