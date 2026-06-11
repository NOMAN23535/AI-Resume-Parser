LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary:       #2B5CE6;
    --primary-dark:  #1E44C4;
    --primary-light: #EEF2FD;
    --bg:            #F5F7FA;
    --bg-white:      #FFFFFF;
    --sidebar-bg:    #1C2B4A;
    --sidebar-hover: #253660;
    --sidebar-active:#2B5CE6;
    --text-dark:     #0F1C35;
    --text-mid:      #4A5568;
    --text-light:    #8A96A8;
    --border:        #E2E8F2;
    --red:           #E53E3E;
    --orange:        #DD6B20;
    --green:         #38A169;
    --shadow:        0 1px 4px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.05);
    --shadow-md:     0 4px 20px rgba(43,92,230,0.12);
    --radius-sm: 8px; --radius-md: 12px; --radius-lg: 18px;
}
</style>
"""

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary:       #4D7FFF;
    --primary-dark:  #3366EE;
    --primary-light: #1A2A4A;
    --bg:            #111827;
    --bg-white:      #1F2937;
    --sidebar-bg:    #0D1117;
    --sidebar-hover: #1A2333;
    --sidebar-active:#2B5CE6;
    --text-dark:     #F1F5F9;
    --text-mid:      #94A3B8;
    --text-light:    #64748B;
    --border:        #2D3748;
    --red:           #FC8181;
    --orange:        #F6AD55;
    --green:         #68D391;
    --shadow:        0 1px 4px rgba(0,0,0,0.3), 0 4px 16px rgba(0,0,0,0.2);
    --shadow-md:     0 4px 20px rgba(0,0,0,0.4);
    --radius-sm: 8px; --radius-md: 12px; --radius-lg: 18px;
}
</style>
"""

COMMON_CSS = """
<style>
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text-dark) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.main { background: var(--bg) !important; }
.main .block-container {
    padding-top: 2rem; padding-left: 2.4rem;
    padding-right: 2.4rem; max-width: 1440px;
    background: var(--bg) !important;
}

/* ── Sidebar ─────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #CBD5E0 !important; }
[data-testid="stSidebar"] a[href^="http://localhost:8501"],
[data-testid="stSidebar"] a[href^="/analytics"],
[data-testid="stSidebar"] a[href^="/candidates"],
[data-testid="stSidebar"] a[href^="/dashboard"],
[data-testid="stSidebar"] a[href^="/history"],
[data-testid="stSidebar"] a[href^="/job_matching"],
[data-testid="stSidebar"] a[href^="/settings"],
[data-testid="stSidebar"] a[href^="/upload"] { display: none !important; }

[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    color: #A0AEC0 !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    text-align: left !important;
    transition: all 0.15s !important;
    padding: 10px 14px !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: var(--sidebar-hover) !important;
    color: #FFFFFF !important;
    transform: none !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: var(--sidebar-active) !important;
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stButton button * { color: inherit !important; }

/* ── Sidebar Brand ───────────────────── */
.sidebar-brand {
    padding: 12px 20px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin: 0 !important;
    text-align: center;
    margin-bottom: 18px !important;
}
.sidebar-brand-logo { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.sidebar-brand-icon {
    width: 36px; height: 36px;
    background: var(--primary);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.sidebar-brand-title {
    font-size: 17px !important; font-weight: 700 !important;
    color: #FFFFFF !important; letter-spacing: -0.01em; margin: 0 !important;
    text-align: center !important;
}
.sidebar-brand-subtitle { font-size: 14px !important; color: #718096 !important; margin: 6px 0 0 0 !important; text-align: center !important; }

/* ── Sidebar Logo Image ──────────────── */
[data-testid="stSidebar"] .stImage {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin: 0 20px 12px 20px !important;
}
[data-testid="stSidebar"] img {
    width: 100% !important;
    height: auto !important;
    display: block !important;
    border-radius: 20px !important;
    object-fit: cover !important;
    background: rgba(255,255,255,0.05) !important;
    padding: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    aspect-ratio: 16/9;
}
.sidebar-footer {
    padding: 16px 20px;
    border-top: 1px solid rgba(255,255,255,0.07);
    font-size: 11px; color: #4A5568 !important;
    text-align: center; letter-spacing: 0.02em;
}

/* ── Theme Toggle ────────────────────── */
.theme-toggle-wrap {
    padding: 0 20px 16px;
}
.theme-toggle-wrap .stButton button {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #94A3B8 !important;
    font-size: 12px !important;
    padding: 7px 12px !important;
    border-radius: 20px !important;
    width: auto !important;
}
.theme-toggle-wrap .stButton button:hover {
    background: rgba(255,255,255,0.12) !important;
    color: #FFFFFF !important;
}

/* ── Page Title ──────────────────────── */
.page-title {
    font-size: 26px; font-weight: 800;
    color: var(--text-dark); letter-spacing: -0.02em; margin-bottom: 2px;
}
.page-subtitle { font-size: 14px; color: var(--text-mid); margin-bottom: 28px; }

/* ── KPI Cards ───────────────────────── */
.kpi-card {
    background: var(--bg-white);
    border-radius: var(--radius-md);
    padding: 22px 18px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    text-align: center;
    transition: all 0.18s ease;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.kpi-icon { font-size: 26px; margin-bottom: 8px; display: block; }
.kpi-value {
    font-size: 28px; font-weight: 800;
    color: var(--text-dark); line-height: 1;
    margin-bottom: 5px; letter-spacing: -0.02em;
}
.kpi-label {
    font-size: 11px; color: var(--text-light);
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em;
}

/* ── Cards ───────────────────────────── */
.card {
    background: var(--bg-white);
    border-radius: var(--radius-md);
    padding: 24px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    margin-bottom: 16px;
}
.card-title {
    font-size: 15px; font-weight: 700;
    color: var(--text-dark); margin-bottom: 16px;
    padding-bottom: 12px; border-bottom: 1px solid var(--border);
}

/* ── Section Headers ─────────────────── */
.section-header {
    font-size: 20px; font-weight: 700;
    color: var(--text-dark); margin-bottom: 4px;
}
.section-subheader { font-size: 13px; color: var(--text-mid); margin-bottom: 18px; }
.section-divider { border: none; border-top: 1px solid var(--border); margin: 28px 0; }

/* ── Candidate Cards ─────────────────── */
.candidate-card {
    background: var(--bg-white);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    margin-bottom: 10px;
    transition: all 0.18s ease; cursor: pointer;
}
.candidate-card:hover { border-color: var(--primary); box-shadow: var(--shadow-md); transform: translateY(-1px); }
.candidate-name { font-size: 15.5px; font-weight: 700; color: var(--text-dark); margin-bottom: 3px; }
.candidate-email { font-size: 12.5px; color: var(--text-light); margin-bottom: 10px; }

/* ── Score Badges ────────────────────── */
.score-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.score-high   { background: rgba(56,161,105,0.12); color: var(--green); }
.score-medium { background: rgba(221,107,32,0.12); color: var(--orange); }
.score-low    { background: rgba(229,62,62,0.12);  color: var(--red); }

/* ── Skill Tags ──────────────────────── */
.skill-tag {
    display: inline-block; background: var(--primary-light);
    color: var(--primary); border-radius: 5px;
    padding: 3px 9px; font-size: 11.5px; font-weight: 600; margin: 2px;
}
.skill-tag-matched { background: rgba(56,161,105,0.12); color: var(--green); }
.skill-tag-missing { background: rgba(229,62,62,0.1);   color: var(--red); }

/* ── Badges ──────────────────────────── */
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
.badge-blue   { background: var(--primary-light); color: var(--primary); }
.badge-green  { background: rgba(56,161,105,0.12); color: var(--green); }
.badge-yellow { background: rgba(221,107,32,0.12); color: var(--orange); }
.badge-red    { background: rgba(229,62,62,0.12);  color: var(--red); }

/* ── Upload Area ─────────────────────── */
.upload-area {
    border: 2px dashed var(--border);
    border-radius: var(--radius-lg); padding: 52px 32px;
    text-align: center; background: var(--primary-light);
    margin: 16px 0; transition: all 0.18s;
}
.upload-area:hover { border-color: var(--primary); }
.upload-icon { font-size: 44px; margin-bottom: 14px; display: block; }
.upload-title { font-size: 18px; font-weight: 700; color: var(--primary); margin-bottom: 6px; }
.upload-subtitle { font-size: 13px; color: var(--text-mid); }

/* ── Table ───────────────────────────── */
.data-table { width: 100%; border-collapse: collapse; font-size: 13.5px; }
.data-table th {
    background: var(--bg); padding: 11px 14px; text-align: left;
    font-weight: 700; color: var(--text-mid); font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.07em; border-bottom: 2px solid var(--border);
}
.data-table td { padding: 11px 14px; border-bottom: 1px solid var(--border); color: var(--text-mid); }
.data-table tr:hover td { background: var(--primary-light); color: var(--text-dark); }

/* ── Profile Header ──────────────────── */
.profile-header {
    background: var(--primary);
    border-radius: var(--radius-lg); padding: 32px 36px;
    color: white; margin-bottom: 24px;
    box-shadow: 0 4px 24px rgba(43,92,230,0.25);
}
.profile-name { font-size: 26px; font-weight: 800; margin-bottom: 6px; letter-spacing: -0.02em; }
.profile-meta { font-size: 13.5px; opacity: 0.8; margin-bottom: 12px; }
.profile-score-card {
    background: rgba(255,255,255,0.18); border-radius: var(--radius-md);
    padding: 14px 22px; text-align: center;
}
.profile-score-value { font-size: 26px; font-weight: 800; }
.profile-score-label { font-size: 10px; opacity: 0.75; text-transform: uppercase; letter-spacing: 0.1em; }

/* ── Alerts ──────────────────────────── */
.alert-success { background: rgba(56,161,105,0.12); border: 1px solid rgba(56,161,105,0.3); border-radius: var(--radius-sm); padding: 12px 16px; color: var(--green); font-weight: 600; font-size: 14px; }
.alert-error   { background: rgba(229,62,62,0.1);   border: 1px solid rgba(229,62,62,0.3);  border-radius: var(--radius-sm); padding: 12px 16px; color: var(--red);   font-weight: 600; font-size: 14px; }
.alert-info    { background: var(--primary-light);   border: 1px solid rgba(75,125,230,0.25); border-radius: var(--radius-sm); padding: 12px 16px; color: var(--primary); font-weight: 600; font-size: 14px; }

/* ── Buttons ─────────────────────────── */
.stButton button {
    border-radius: var(--radius-sm) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 13.5px !important;
    transition: all 0.15s !important;
}
.stButton button[kind="primary"] {
    background: var(--primary) !important; border: none !important;
    color: #FFFFFF !important; box-shadow: 0 2px 10px rgba(43,92,230,0.25) !important;
}
.stButton button[kind="primary"]:hover {
    background: var(--primary-dark) !important;
    box-shadow: 0 4px 18px rgba(43,92,230,0.35) !important; transform: translateY(-1px) !important;
}
.stButton button[kind="secondary"] {
    background: var(--bg-white) !important; border: 1.5px solid var(--border) !important;
    color: var(--text-mid) !important;
}
.stButton button[kind="secondary"]:hover {
    border-color: var(--primary) !important; color: var(--primary) !important;
    background: var(--primary-light) !important;
}

/* ── Inputs ──────────────────────────── */
.stTextInput input, .stTextArea textarea,
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
    background: var(--bg-white) !important; border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important; color: var(--text-dark) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(43,92,230,0.1) !important;
}

/* ── Tabs ────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px; background: var(--border);
    border-radius: var(--radius-sm); padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px; padding: 7px 18px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 500; font-size: 13px; color: var(--text-mid);
}
.stTabs [aria-selected="true"] {
    background: var(--bg-white) !important; color: var(--primary) !important;
    font-weight: 700 !important; box-shadow: 0 1px 6px rgba(0,0,0,0.1) !important;
}

/* ── Metrics ─────────────────────────── */
[data-testid="metric-container"] {
    background: var(--bg-white) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important; padding: 16px !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="metric-container"] label {
    color: var(--text-light) !important; font-size: 11px !important;
    font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.06em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--text-dark) !important; }

/* ── Expander ────────────────────────── */
.streamlit-expanderHeader {
    background: var(--bg-white) !important; border-radius: var(--radius-sm) !important;
    font-weight: 700 !important; color: var(--text-dark) !important;
    border: 1px solid var(--border) !important;
}

/* ── Progress ────────────────────────── */
.stProgress .st-bo { background-color: var(--primary) !important; }

/* ── Rank List ───────────────────────── */
.rank-item {
    display: flex; align-items: center; padding: 12px 16px;
    background: var(--bg-white); border-radius: var(--radius-sm);
    border: 1px solid var(--border); margin-bottom: 7px; transition: all 0.15s;
}
.rank-item:hover { border-color: var(--primary); background: var(--primary-light); }
.rank-number {
    width: 30px; height: 30px; background: var(--bg); color: var(--text-mid);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 13px; margin-right: 12px; flex-shrink: 0;
}
.rank-number-1 { background: rgba(221,107,32,0.15); color: var(--orange); }
.rank-number-2 { background: rgba(148,163,184,0.15); color: var(--text-mid); }
.rank-number-3 { background: rgba(77,127,255,0.12); color: var(--primary); }

/* ── Job Cards ───────────────────────── */
.job-card {
    background: var(--bg-white); border-radius: var(--radius-md);
    padding: 20px; border: 1px solid var(--border);
    box-shadow: var(--shadow); margin-bottom: 10px; transition: all 0.18s ease;
}
.job-card:hover { border-color: var(--primary); transform: translateY(-1px); box-shadow: var(--shadow-md); }
.job-title { font-size: 15px; font-weight: 700; color: var(--text-dark); margin-bottom: 5px; }
.job-meta { font-size: 12.5px; color: var(--text-mid); }

/* ── Dataframe ───────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden; box-shadow: var(--shadow);
}

/* ── Select ──────────────────────────── */
[data-baseweb="select"] > div {
    background: var(--bg-white) !important; border-color: var(--border) !important;
    color: var(--text-dark) !important;
}

/* ── Scrollbar ───────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-light); }
</style>
"""

def get_css(dark_mode=False):
    theme = DARK_CSS if dark_mode else LIGHT_CSS
    return theme + COMMON_CSS
