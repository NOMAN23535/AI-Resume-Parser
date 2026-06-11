import json
import io
import pandas as pd

def candidate_to_dict(c):
    return {
        "ID": c.get("id",""),
        "Name": c.get("name",""),
        "Email": c.get("email",""),
        "Phone": c.get("phone",""),
        "Location": c.get("location",""),
        "LinkedIn": c.get("linkedin",""),
        "GitHub": c.get("github",""),
        "Skills": ", ".join(c.get("skills",[])),
        "ATS Score": c.get("ats_score",0),
        "Resume Score": c.get("resume_score",0),
        "Education": "; ".join([f"{e.get('degree','')} - {e.get('institution','')}" for e in c.get("education",[])]),
        "Experience": "; ".join([f"{e.get('title','')} at {e.get('company','')}" for e in c.get("experience",[])]),
        "Certifications": "; ".join([e.get("cert_name","") for e in c.get("certifications",[])]),
        "File Name": c.get("file_name",""),
        "File Size": c.get("file_size",""),
        "Upload Date": c.get("upload_date", c.get("created_at","")),
        "Created At": c.get("created_at",""),
    }

def export_to_json(candidates):
    data = [candidate_to_dict(c) for c in candidates]
    return json.dumps(data, indent=2).encode("utf-8")

def export_to_csv(candidates):
    data = [candidate_to_dict(c) for c in candidates]
    df = pd.DataFrame(data)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

def export_to_excel(candidates):
    data = [candidate_to_dict(c) for c in candidates]
    df = pd.DataFrame(data)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Candidates")
    return buf.getvalue()

def export_single_pdf(candidate):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=22, textColor=colors.HexColor('#2563EB'), spaceAfter=4)
        h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#0F172A'), spaceBefore=12, spaceAfter=4)
        normal_style = styles['Normal']
        normal_style.fontSize = 10

        story.append(Paragraph(candidate.get("name","Candidate"), title_style))
        story.append(Paragraph(f"{candidate.get('email','')}  |  {candidate.get('phone','')}  |  {candidate.get('location','')}", normal_style))
        if candidate.get("linkedin"): story.append(Paragraph(f"LinkedIn: {candidate.get('linkedin')}", normal_style))
        if candidate.get("github"): story.append(Paragraph(f"GitHub: {candidate.get('github')}", normal_style))
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", color=colors.HexColor('#2563EB')))

        story.append(Paragraph("Scores", h2_style))
        score_data = [["ATS Score", f"{candidate.get('ats_score',0)}%", "Resume Score", f"{candidate.get('resume_score',0)}%"]]
        t = Table(score_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#2563EB')),
        ]))
        story.append(t)

        if candidate.get("skills"):
            story.append(Paragraph("Skills", h2_style))
            story.append(Paragraph(", ".join(candidate["skills"]), normal_style))

        if candidate.get("summary"):
            story.append(Paragraph("Summary", h2_style))
            story.append(Paragraph(candidate["summary"], normal_style))

        if candidate.get("education"):
            story.append(Paragraph("Education", h2_style))
            for edu in candidate["education"]:
                story.append(Paragraph(f"• {edu.get('degree','')} - {edu.get('institution','')} {edu.get('year','')}", normal_style))

        if candidate.get("experience"):
            story.append(Paragraph("Experience", h2_style))
            for exp in candidate["experience"]:
                story.append(Paragraph(f"• {exp.get('title','')} at {exp.get('company','')} {exp.get('duration','')}", normal_style))
                if exp.get("description"):
                    story.append(Paragraph(f"  {exp.get('description','')}", normal_style))

        if candidate.get("certifications"):
            story.append(Paragraph("Certifications", h2_style))
            for cert in candidate["certifications"]:
                story.append(Paragraph(f"• {cert.get('cert_name','')} {cert.get('year','')}", normal_style))

        if candidate.get("projects"):
            story.append(Paragraph("Projects", h2_style))
            for proj in candidate["projects"]:
                story.append(Paragraph(f"• {proj.get('project_name','')}", normal_style))
                if proj.get("description"):
                    story.append(Paragraph(f"  {proj.get('description','')}", normal_style))

        doc.build(story)
        return buf.getvalue()
    except Exception as e:
        return None
