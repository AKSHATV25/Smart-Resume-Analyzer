from google import genai
import os
import json
import re

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

def gemini_improve_resume(resume_text, job_desc):
    prompt = f"""
    Analyze resume vs job description.

    Resume:
    {resume_text}

    Job Description:
    {job_desc}

    Return ONLY valid JSON (no markdown):
    {{
      "ats_score": 75,
      "improved_resume": "...",
      "suggestions": ["...", "..."],
      "missing_keywords": ["...", "..."],
      "matched_keywords": ["...", "..."]
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()


    text = re.sub(r"```json|```", "", text).strip()

    text = re.sub(r"\(.*?\)", "", text)

    try:
        data = json.loads(text)
    except Exception as e:
        return {
            "ats_score": 0,
            "improved_resume": text,
            "suggestions": [f"Parsing error: {str(e)}"],
            "missing_keywords": [],
            "matched_keywords": []
        }

    return data