import spacy

nlp = spacy.load("en_core_web_sm")

# Strong action verbs
strong_verbs = [
    "developed", "designed", "implemented", "optimized",
    "engineered", "built", "created", "analyzed",
    "automated", "led", "improved"
]

weak_verbs = ["worked", "did", "made", "helped"]

# Skill database (can expand)
skill_db = [
    "python", "java", "machine learning", "sql",
    "flask", "django", "data analysis", "nlp",
    "javascript", "react"
]


def improve_resume(text, job_desc=""):
    doc = nlp(text.lower())

    suggestions = []
    improved_lines = []

    # 🔹 Sentence Improvement
    for sent in doc.sents:
        sentence = sent.text.strip()

        # Replace weak verbs
        for weak in weak_verbs:
            if weak in sentence:
                better = sentence.replace(weak, "developed")
                improved_lines.append(better)
                suggestions.append(f"Replace '{weak}' with stronger action verbs")
                break
        else:
            improved_lines.append(sentence)

    # 🔹 Skill Detection
    resume_skills = set()
    for token in doc:
        if token.text in skill_db:
            resume_skills.add(token.text)

    # 🔹 Missing Skills from Job Description
    missing_skills = []
    if job_desc:
        jd_doc = nlp(job_desc.lower())
        jd_skills = set([token.text for token in jd_doc if token.text in skill_db])
        missing_skills = list(jd_skills - resume_skills)

    return {
        "improved_text": "\n".join(improved_lines),
        "suggestions": list(set(suggestions)),
        "missing_skills": missing_skills
    }