import re

def cosine_similarity_simple(vec1, vec2):
    dot = sum(a*b for a,b in zip(vec1,vec2))
    mag1 = sum(a**2 for a in vec1)**0.5
    mag2 = sum(b**2 for b in vec2)**0.5
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

def get_sentence_transformer_score(text1, text2):
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        emb = model.encode([text1, text2])
        score = cosine_similarity_simple(emb[0].tolist(), emb[1].tolist())
        return round(score * 100, 2)
    except Exception:
        return keyword_match_score(text1, text2)

def keyword_match_score(text1, text2):
    words1 = set(re.findall(r'\b\w{3,}\b', text1.lower()))
    words2 = set(re.findall(r'\b\w{3,}\b', text2.lower()))
    if not words1 or not words2:
        return 0.0
    intersection = words1 & words2
    union = words1 | words2
    jaccard = len(intersection) / len(union)
    return round(jaccard * 100, 2)

def match_candidate_to_job(candidate, job):
    candidate_text = " ".join([
        candidate.get("raw_text",""),
        " ".join(candidate.get("skills",[])),
        " ".join([e.get("description","") for e in candidate.get("experience",[])]),
    ])
    job_text = " ".join([
        job.get("description",""),
        " ".join(job.get("required_skills",[])),
        job.get("experience_required",""),
        job.get("education_required",""),
    ])

    semantic_score = get_sentence_transformer_score(candidate_text, job_text)

    candidate_skills = [s.lower() for s in candidate.get("skills",[])]
    required_skills = [s.lower() for s in job.get("required_skills",[])]

    matched_skills = [s for s in required_skills if any(s in cs or cs in s for cs in candidate_skills)]
    missing_skills = [s for s in required_skills if s not in matched_skills]

    skill_match_pct = (len(matched_skills) / len(required_skills) * 100) if required_skills else semantic_score

    final_score = (semantic_score * 0.5 + skill_match_pct * 0.5)
    final_score = round(min(final_score, 100), 2)

    return {
        "match_score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_pct": round(skill_match_pct, 1),
        "semantic_score": semantic_score,
    }

def rank_candidates_for_job(candidates, job):
    results = []
    for candidate in candidates:
        match = match_candidate_to_job(candidate, job)
        results.append({
            "candidate_id": candidate["id"],
            "name": candidate.get("name",""),
            "email": candidate.get("email",""),
            "ats_score": candidate.get("ats_score",0),
            "resume_score": candidate.get("resume_score",0),
            "match_score": match["match_score"],
            "matched_skills": match["matched_skills"],
            "missing_skills": match["missing_skills"],
        })
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
