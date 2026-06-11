import re
import os
import io

SKILLS_DB = [
    # Programming & Languages
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript", "PHP", "Ruby", "Go", "Rust",
    "Kotlin", "Swift", "Dart", "Scala", "R", "MATLAB", "Perl", "Lua", "Julia", "Objective-C", "VB.NET",
    "Assembly", "Fortran", "COBOL",

    # Web Development
    "HTML5", "CSS3", "Bootstrap", "Tailwind CSS", "React", "Next.js", "NextJS", "Angular", "Vue.js", "Svelte",
    "jQuery", "AJAX", "Node.js", "Express.js", "Django", "Flask", "FastAPI", "Laravel", "CodeIgniter", "ASP.NET",
    "Spring Boot", "REST API", "GraphQL", "WebSockets", "PWA", "Responsive Design", "SEO", "Webpack", "Vite", "Babel",

    # Frontend frameworks/tools
    "Redux", "TypeORM", "Prisma", "Mongoose",

    # Mobile
    "Android", "Kotlin Android", "Java Android", "Flutter", "React Native", "Swift iOS", "Objective-C iOS", "Xamarin",
    "Ionic", "Mobile UI", "Firebase",

    # Databases
    "MySQL", "PostgreSQL", "Oracle", "SQL Server", "SQLite", "MongoDB", "Cassandra", "Redis", "MariaDB",
    "DynamoDB", "Firebase Firestore", "Neo4j", "CouchDB", "NoSQL", "Elasticsearch", "Snowflake",

    # Data Science & Analytics
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "Power BI", "Tableau", "Data Analysis", "Data Cleaning",
    "Feature Engineering", "Data Visualization", "Statistical Analysis",

    # Machine Learning & AI
    "Machine Learning", "Deep Learning", "Neural Networks", "CNN", "RNN", "LSTM", "TensorFlow", "Keras", "PyTorch",
    "Scikit-Learn", "XGBoost", "LightGBM", "Computer Vision", "OpenCV", "NLP", "Hugging Face", "Transformers", "BERT",
    "GPT", "Sentence-Transformers", "LangChain", "LlamaIndex", "RAG", "Generative AI", "Prompt Engineering",

    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud Platform", "GCP", "EC2", "Lambda", "S3", "Cloud Functions", "Kubernetes", "Docker",
    "Terraform", "Ansible", "Puppet", "Chef", "Jenkins", "GitHub Actions", "GitLab CI/CD", "CI/CD", "Prometheus", "Grafana",

    # Infrastructure / Servers
    "NGINX", "Apache", "Nginx", "Load Balancing", "Serverless",

    # Messaging / Streaming
    "Kafka", "RabbitMQ", "Apache Kafka", "Airflow", "ETL",

    # Testing & QA
    "Selenium", "Pytest", "Jest", "Cypress", "QA Automation",

    # Tools & Version Control
    "Git", "GitHub", "GitLab", "Bitbucket", "Linux", "Ubuntu", "Docker", "Nginx",

    # UI/UX & Design
    "Figma", "Adobe XD", "Sketch", "Photoshop", "Illustrator", "Canva", "Wireframing", "Prototyping",

    # Graphic & Video
    "Adobe Premiere Pro", "After Effects", "DaVinci Resolve", "Final Cut Pro", "Motion Graphics",

    # Marketing & SEO
    "SEO", "Google Ads", "Facebook Ads", "Instagram Marketing", "LinkedIn Marketing", "Email Marketing", "PPC",

    # Content & Writing
    "Copywriting", "Technical Writing", "SEO Writing", "Blog Writing",

    # Project Management & Business
    "Agile", "Scrum", "Kanban", "Jira", "Trello", "Asana", "Requirement Gathering", "Process Mapping",

    # Security & Networking
    "Network Security", "Ethical Hacking", "Penetration Testing", "OWASP", "Firewall Management", "TCP/IP", "DNS", "VPN",

    # Other development frameworks/tools
    "ExpressJS", "Express", "Redux Toolkit", "TypeORM", "SQLAlchemy", "Prisma", "Mongoose", "NGINX",

    # Soft skills / general
    "Communication", "Leadership", "Teamwork", "Problem Solving", "Time Management", "Critical Thinking", "Presentation",

    # Additional data/platforms
    "Hadoop", "Spark", "Hive", "BigQuery", "Databricks", "Airflow", "Hadoop", "Spark",

    # Misc and common libraries
    "Openpyxl", "ReportLab", "pdfplumber", "PyPDF2", "python-docx", "BeautifulSoup", "Scrapy", "Selenium",
]

def extract_text_from_pdf(file_bytes):
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception:
        pass
    if not text.strip():
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        except Exception:
            pass
    return text

def extract_text_from_docx(file_bytes):
    text = ""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + " "
                text += "\n"
    except Exception:
        pass
    return text

def extract_email(text):
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    matches = re.findall(pattern, text)
    return matches[0] if matches else ""

def extract_phone(text):
    patterns = [
        r'(\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4})',
        r'(\+\d{10,13})',
        r'(\d{10,11})',
    ]
    for p in patterns:
        matches = re.findall(p, text)
        for m in matches:
            clean = re.sub(r'[^\d+]', '', m)
            if len(clean) >= 10:
                return m.strip()
    return ""

def extract_linkedin(text):
    pattern = r'(linkedin\.com/in/[A-Za-z0-9\-_%]+)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return "https://" + matches[0] if matches else ""

def extract_github(text):
    pattern = r'(github\.com/[A-Za-z0-9\-_%]+)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return "https://" + matches[0] if matches else ""

def extract_portfolio(text):
    pattern = r'(https?://(?:www\.)?[A-Za-z0-9\-]+\.[A-Za-z]{2,}(?:/[^\s]*)?)'
    matches = re.findall(pattern, text)
    for m in matches:
        if "linkedin" not in m and "github" not in m and "mailto" not in m:
            return m
    return ""

def extract_name_spacy(text):
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text.strip()
                if 2 <= len(name.split()) <= 4:
                    return name
    except Exception:
        pass
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:5]:
        words = line.split()
        if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
            skip = ['resume','curriculum','vitae','cv','profile','contact','summary']
            if not any(s in line.lower() for s in skip):
                return line
    return "Unknown Candidate"

def extract_location_spacy(text):
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text[:1000])
        for ent in doc.ents:
            if ent.label_ in ("GPE", "LOC"):
                return ent.text.strip()
    except Exception:
        pass
    patterns = [
        r'(?:Location|Address|City|Based in)[:\s]+([A-Za-z\s,]+)',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()[:50]
    return ""

def extract_skills(text):
    found = []
    text_lower = text.lower()
    for skill in SKILLS_DB:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            if skill not in found:
                found.append(skill)
    return found

def extract_education(text):
    edu_list = []
    degrees = ["B.Sc", "BSc", "B.S", "BS", "B.Tech", "BTech", "B.E", "BE", "BCA", "BBA",
               "M.Sc", "MSc", "M.S", "MS", "M.Tech", "MTech", "MBA", "MCA", "Ph.D", "PhD",
               "Bachelor", "Master", "Doctorate", "Associate", "Diploma", "Certificate",
               "B.Com", "M.Com", "BA", "MA", "LLB", "LLM", "MBBS", "MD"]
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for deg in degrees:
            if re.search(r'\b' + re.escape(deg) + r'\b', line, re.IGNORECASE):
                year_match = re.search(r'(19|20)\d{2}', line)
                year = year_match.group() if year_match else ""
                inst = ""
                context = " ".join(lines[max(0,i-1):i+3])
                univ_keywords = ["University","College","Institute","School","Academy","Polytechnic"]
                for kw in univ_keywords:
                    if kw.lower() in context.lower():
                        idx = context.lower().find(kw.lower())
                        start = max(0, idx-30)
                        end = min(len(context), idx+60)
                        inst = context[start:end].strip()
                        break
                edu_list.append({"degree": deg, "institution": inst[:100], "year": year})
                break
    seen = set()
    unique = []
    for e in edu_list:
        key = e["degree"] + e["institution"]
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique[:5]

def extract_experience(text):
    exp_list = []
    titles = ["Engineer","Developer","Manager","Analyst","Designer","Consultant","Architect",
              "Lead","Senior","Junior","Intern","Specialist","Director","Officer","Coordinator",
              "Administrator","Scientist","Researcher","Programmer","Tester","QA","DevOps",
              "Full Stack","Frontend","Backend","Data","Software","Web","Mobile","Cloud","AI","ML"]
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for title in titles:
            if title.lower() in line.lower() and len(line) < 120:
                dur_match = re.search(r'(\d{4}\s*[-–]\s*(?:\d{4}|Present|Current|Now))', line + " " + (lines[i+1] if i+1 < len(lines) else ""), re.IGNORECASE)
                duration = dur_match.group() if dur_match else ""
                company = ""
                at_match = re.search(r'(?:at|@|,)\s*([A-Z][A-Za-z\s&.]+)', line)
                if at_match:
                    company = at_match.group(1).strip()[:60]
                desc = lines[i+1].strip() if i+1 < len(lines) else ""
                exp_list.append({"title": line.strip()[:80], "company": company, "duration": duration, "description": desc[:150]})
                break
    seen = set()
    unique = []
    for e in exp_list:
        if e["title"] not in seen:
            seen.add(e["title"])
            unique.append(e)
    return unique[:6]

def extract_certifications(text):
    certs = []
    cert_keywords = ["certified","certification","certificate","aws certified","google certified",
                     "microsoft certified","pmp","cissp","ccna","ceh","comptia","oracle certified",
                     "salesforce","coursera","udemy","edx","linkedin learning","hackerrank","kaggle"]
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if any(kw in line_lower for kw in cert_keywords) and len(line.strip()) > 5:
            year_match = re.search(r'(19|20)\d{2}', line)
            year = year_match.group() if year_match else ""
            issuer_match = re.search(r'(?:by|from|issued by)\s+([A-Z][A-Za-z\s]+)', line, re.IGNORECASE)
            issuer = issuer_match.group(1).strip() if issuer_match else ""
            certs.append({"name": line.strip()[:100], "issuer": issuer[:60], "year": year})
    return certs[:8]

def extract_projects(text):
    projects = []
    sections = re.split(r'\n(?=Project[s]?\s*[:\-]|\bProject\b)', text, flags=re.IGNORECASE)
    for section in sections[1:]:
        lines = [l.strip() for l in section.split('\n') if l.strip()]
        if lines:
            name = lines[0][:80]
            desc = " ".join(lines[1:4])[:200]
            techs = []
            for skill in SKILLS_DB:
                if skill.lower() in desc.lower():
                    techs.append(skill)
            projects.append({"name": name, "description": desc, "technologies": ", ".join(techs[:6])})
    if not projects:
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'project\s*\d*\s*[:\-]', line, re.IGNORECASE) and len(line) < 100:
                desc = " ".join(lines[i+1:i+3])[:200] if i+1 < len(lines) else ""
                techs = [s for s in SKILLS_DB if s.lower() in desc.lower()][:5]
                projects.append({"name": line.strip()[:80], "description": desc, "technologies": ", ".join(techs)})
    return projects[:5]

def extract_summary(text):
    patterns = [
        r'(?:Summary|Profile|Objective|About Me|Professional Summary)[:\s\n]+(.{100,500})',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE | re.DOTALL)
        if m:
            summary = m.group(1).strip()[:400]
            return re.sub(r'\s+', ' ', summary)
    return ""

def calculate_ats_score(parsed):
    score = 0
    if parsed.get("name","") and parsed["name"] != "Unknown Candidate": score += 10
    if parsed.get("email",""): score += 10
    if parsed.get("phone",""): score += 5
    if parsed.get("location",""): score += 5
    skills = parsed.get("skills",[])
    score += min(len(skills) * 2, 20)
    edu = parsed.get("education",[])
    score += min(len(edu) * 5, 15)
    exp = parsed.get("experience",[])
    score += min(len(exp) * 3, 15)
    certs = parsed.get("certifications",[])
    score += min(len(certs) * 2, 10)
    projects = parsed.get("projects",[])
    score += min(len(projects) * 2, 10)
    return min(round(score, 1), 100)

def calculate_resume_score(parsed):
    score = 0
    skills = parsed.get("skills",[])
    score += min(len(skills) * 2, 40)
    exp = parsed.get("experience",[])
    score += min(len(exp) * 5, 30)
    edu = parsed.get("education",[])
    score += min(len(edu) * 7, 20)
    certs = parsed.get("certifications",[])
    score += min(len(certs) * 2, 10)
    return min(round(score, 1), 100)

def parse_resume(file_bytes, file_name):
    ext = os.path.splitext(file_name)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_bytes)
    elif ext in [".docx", ".doc"]:
        text = extract_text_from_docx(file_bytes)
    else:
        text = file_bytes.decode("utf-8", errors="ignore")

    parsed = {
        "name": extract_name_spacy(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": extract_location_spacy(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "portfolio": extract_portfolio(text),
        "summary": extract_summary(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "certifications": extract_certifications(text),
        "projects": extract_projects(text),
        "raw_text": text[:5000],
        "file_name": file_name,
    }
    parsed["ats_score"] = calculate_ats_score(parsed)
    parsed["resume_score"] = calculate_resume_score(parsed)
    return parsed
