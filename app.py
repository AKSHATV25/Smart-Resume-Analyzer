from flask import Flask, render_template, request, jsonify
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# 🔥 Stopwords (fix garbage words issue)
STOPWORDS = set([
    "the","and","is","in","to","of","for","with","a","an","we","are",
    "looking","required","should","have","be","on","as","by","or"
])

# 📄 Extract text from PDF
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

# 🧠 Clean text
def clean_text(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return [w for w in words if w not in STOPWORDS]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["resume"]
    jobdesc = request.form["jobdesc"]

    resume_text = extract_text(file)
    resume_words = clean_text(resume_text)
    job_words = clean_text(jobdesc)

    resume_set = set(resume_words)
    job_set = set(job_words)

    matched = list(resume_set & job_set)
    missing = list(job_set - resume_set)

    # 🎯 ATS Score
    score = int((len(matched) / len(job_set)) * 100) if job_set else 0

    # 🧠 NLP Similarity
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_text, jobdesc])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    similarity = round(similarity * 100, 2)

    # 🤖 Suggestions
    suggestions = []
    if score < 50:
        suggestions.append("Add more relevant technical skills.")
    if missing:
        suggestions.append("Include missing skills: " + ", ".join(missing[:5]))
    if similarity < 40:
        suggestions.append("Improve content similarity with job description.")
    suggestions.append("Add projects and experience related to job role.")

    return jsonify({
        "score": score,
        "similarity": similarity,
        "matched": matched[:10],
        "missing": missing[:10],
        "suggestions": suggestions
    })

if __name__ == "__main__":
    app.run(debug=True)