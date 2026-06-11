import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="AI Resume Parser - Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

from database import init_db
init_db()

                                                      
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

from assets.styles import get_css
st.markdown(get_css(st.session_state["dark_mode"]), unsafe_allow_html=True)

MENU_ITEMS = {
    "Dashboard":    "dashboard",
    "Upload Resume": "upload",
    "Candidates":   "candidates",
    "Job Matching":  "job_matching",
    "Analytics":    "analytics",
    "History":      "history",
    "Settings":     "settings",
}

with st.sidebar:
    # Display logo image centered with button width
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=250)
    else:
        st.warning("Logo file not found in assets folder")
    
    # Display main heading and subtitle centered
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">AI RESUME PARSER</div>
        <div class="sidebar-brand-subtitle">Developed By Noman Hameed</div>
    </div>
    """, unsafe_allow_html=True)

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "📊  Dashboard"

    for item in MENU_ITEMS.keys():
        is_active = st.session_state["current_page"] == item
        if st.button(item, key=f"nav_{item}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state["current_page"] = item
            st.session_state.pop("view_candidate_id", None)
            st.session_state.pop("match_job_id", None)
            st.rerun()

    st.markdown("<br>" * 2, unsafe_allow_html=True)

                                                       
    is_dark = st.session_state["dark_mode"]
    toggle_label = "☀️  Light Mode" if is_dark else "🌙  Dark Mode"
    st.markdown('<div class="theme-toggle-wrap">', unsafe_allow_html=True)
    if st.button(toggle_label, key="theme_toggle", use_container_width=True):
        st.session_state["dark_mode"] = not is_dark
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-footer">
        Resume Parser AI v1.0 &nbsp;·&nbsp; Streamlit + SpaCy & FastAPI &nbsp;·&nbsp; Developed by Noman Hameed
    </div>""", unsafe_allow_html=True)

current = st.session_state.get("current_page", "📊  Dashboard")
page_module = MENU_ITEMS.get(current, "dashboard")

if page_module == "dashboard":
    from pages.dashboard import render
elif page_module == "upload":
    from pages.upload import render
elif page_module == "candidates":
    from pages.candidates import render
elif page_module == "job_matching":
    from pages.job_matching import render
elif page_module == "analytics":
    from pages.analytics import render
elif page_module == "history":
    from pages.history import render
elif page_module == "settings":
    from pages.settings import render

render()
