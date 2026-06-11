import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "recruitment.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        location TEXT,
        linkedin TEXT,
        github TEXT,
        portfolio TEXT,
        summary TEXT,
        ats_score REAL DEFAULT 0,
        resume_score REAL DEFAULT 0,
        raw_text TEXT,
        file_name TEXT,
        file_path TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now'))
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        skill_name TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        degree TEXT,
        institution TEXT,
        year TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS experience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        title TEXT,
        company TEXT,
        duration TEXT,
        description TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        cert_name TEXT,
        issuer TEXT,
        year TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        project_name TEXT,
        description TEXT,
        technologies TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        required_skills TEXT,
        experience_required TEXT,
        education_required TEXT,
        description TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS job_matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        candidate_id INTEGER,
        match_score REAL,
        matched_skills TEXT,
        missing_skills TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        candidate_name TEXT,
        candidate_id INTEGER,
        file_size TEXT,
        ats_score REAL,
        resume_score REAL,
        upload_date TEXT DEFAULT (datetime('now'))
    )""")

    conn.commit()
    conn.close()

def insert_candidate(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO candidates (name, email, phone, location, linkedin, github, portfolio, summary, ats_score, resume_score, raw_text, file_name, file_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("name",""), data.get("email",""), data.get("phone",""),
        data.get("location",""), data.get("linkedin",""), data.get("github",""),
        data.get("portfolio",""), data.get("summary",""), data.get("ats_score",0),
        data.get("resume_score",0), data.get("raw_text",""),
        data.get("file_name",""), data.get("file_path","")
    ))
    candidate_id = c.lastrowid

    for skill in data.get("skills", []):
        c.execute("INSERT INTO skills (candidate_id, skill_name) VALUES (?, ?)", (candidate_id, skill))

    for edu in data.get("education", []):
        c.execute("INSERT INTO education (candidate_id, degree, institution, year) VALUES (?, ?, ?, ?)",
                  (candidate_id, edu.get("degree",""), edu.get("institution",""), edu.get("year","")))

    for exp in data.get("experience", []):
        c.execute("INSERT INTO experience (candidate_id, title, company, duration, description) VALUES (?, ?, ?, ?, ?)",
                  (candidate_id, exp.get("title",""), exp.get("company",""), exp.get("duration",""), exp.get("description","")))

    for cert in data.get("certifications", []):
        c.execute("INSERT INTO certifications (candidate_id, cert_name, issuer, year) VALUES (?, ?, ?, ?)",
                  (candidate_id, cert.get("name",""), cert.get("issuer",""), cert.get("year","")))

    for proj in data.get("projects", []):
        c.execute("INSERT INTO projects (candidate_id, project_name, description, technologies) VALUES (?, ?, ?, ?)",
                  (candidate_id, proj.get("name",""), proj.get("description",""), proj.get("technologies","")))

    conn.commit()
    conn.close()
    return candidate_id

def get_all_candidates():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM candidates ORDER BY created_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_candidate_by_id(cid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM candidates WHERE id=?", (cid,))
    cand = dict(c.fetchone() or {})
    if cand:
        c.execute("SELECT skill_name FROM skills WHERE candidate_id=?", (cid,))
        cand["skills"] = [r["skill_name"] for r in c.fetchall()]
        c.execute("SELECT * FROM education WHERE candidate_id=?", (cid,))
        cand["education"] = [dict(r) for r in c.fetchall()]
        c.execute("SELECT * FROM experience WHERE candidate_id=?", (cid,))
        cand["experience"] = [dict(r) for r in c.fetchall()]
        c.execute("SELECT * FROM certifications WHERE candidate_id=?", (cid,))
        cand["certifications"] = [dict(r) for r in c.fetchall()]
        c.execute("SELECT * FROM projects WHERE candidate_id=?", (cid,))
        cand["projects"] = [dict(r) for r in c.fetchall()]
    conn.close()
    return cand

def delete_candidate(cid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM candidates WHERE id=?", (cid,))
    conn.commit()
    conn.close()

def update_candidate(cid, data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""UPDATE candidates SET name=?, email=?, phone=?, location=?, linkedin=?, github=?,
                 portfolio=?, summary=?, updated_at=? WHERE id=?""",
              (data.get("name",""), data.get("email",""), data.get("phone",""),
               data.get("location",""), data.get("linkedin",""), data.get("github",""),
               data.get("portfolio",""), data.get("summary",""),
               datetime.now().isoformat(), cid))
    if "skills" in data:
        c.execute("DELETE FROM skills WHERE candidate_id=?", (cid,))
        for skill in data["skills"]:
            c.execute("INSERT INTO skills (candidate_id, skill_name) VALUES (?, ?)", (cid, skill))
    conn.commit()
    conn.close()

def insert_job(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO jobs (title, required_skills, experience_required, education_required, description)
                 VALUES (?, ?, ?, ?, ?)""",
              (data.get("title",""), json.dumps(data.get("required_skills",[])),
               data.get("experience_required",""), data.get("education_required",""),
               data.get("description","")))
    jid = c.lastrowid
    conn.commit()
    conn.close()
    return jid

def get_all_jobs():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM jobs ORDER BY created_at DESC")
    rows = []
    for r in c.fetchall():
        d = dict(r)
        try:
            d["required_skills"] = json.loads(d["required_skills"])
        except:
            d["required_skills"] = []
        rows.append(d)
    conn.close()
    return rows

def get_job_by_id(jid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE id=?", (jid,))
    row = c.fetchone()
    if row:
        d = dict(row)
        try:
            d["required_skills"] = json.loads(d["required_skills"])
        except:
            d["required_skills"] = []
        conn.close()
        return d
    conn.close()
    return None

def delete_job(jid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE id=?", (jid,))
    conn.commit()
    conn.close()

def insert_job_match(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM job_matches WHERE job_id=? AND candidate_id=?",
              (data["job_id"], data["candidate_id"]))
    c.execute("""INSERT INTO job_matches (job_id, candidate_id, match_score, matched_skills, missing_skills)
                 VALUES (?, ?, ?, ?, ?)""",
              (data["job_id"], data["candidate_id"], data["match_score"],
               json.dumps(data.get("matched_skills",[])), json.dumps(data.get("missing_skills",[]))))
    conn.commit()
    conn.close()

def get_matches_for_job(jid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT jm.*, c.name, c.email, c.ats_score, c.resume_score
                 FROM job_matches jm JOIN candidates c ON jm.candidate_id=c.id
                 WHERE jm.job_id=? ORDER BY jm.match_score DESC""", (jid,))
    rows = []
    for r in c.fetchall():
        d = dict(r)
        try: d["matched_skills"] = json.loads(d["matched_skills"])
        except: d["matched_skills"] = []
        try: d["missing_skills"] = json.loads(d["missing_skills"])
        except: d["missing_skills"] = []
        rows.append(d)
    conn.close()
    return rows

def insert_upload_log(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO uploads (file_name, candidate_name, candidate_id, file_size, ats_score, resume_score)
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (data.get("file_name",""), data.get("candidate_name",""), data.get("candidate_id",0),
               data.get("file_size",""), data.get("ats_score",0), data.get("resume_score",0)))
    conn.commit()
    conn.close()

def get_all_uploads():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM uploads ORDER BY upload_date DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_upload(uid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM uploads WHERE id=?", (uid,))
    conn.commit()
    conn.close()

def get_db_stats():
    conn = get_connection()
    c = conn.cursor()
    stats = {}
    for table in ["candidates","skills","education","experience","certifications","projects","jobs","job_matches","uploads"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        stats[table] = c.fetchone()[0]
    conn.close()
    return stats

def get_dashboard_stats():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM candidates")
    total_candidates = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = c.fetchone()[0]
    c.execute("SELECT AVG(ats_score) FROM candidates")
    avg_ats = c.fetchone()[0] or 0
    c.execute("SELECT AVG(resume_score) FROM candidates")
    avg_resume = c.fetchone()[0] or 0
    c.execute("SELECT COUNT(*) FROM job_matches")
    total_matches = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM candidates WHERE created_at >= date('now','start of month')")
    new_this_month = c.fetchone()[0]
    conn.close()
    return {
        "total_candidates": total_candidates,
        "total_jobs": total_jobs,
        "avg_ats": round(avg_ats, 1),
        "avg_resume": round(avg_resume, 1),
        "total_matches": total_matches,
        "new_this_month": new_this_month
    }
