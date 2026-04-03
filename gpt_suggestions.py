from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_improve_resume(resume_text, job_desc=""):
    prompt = f"""
You are an expert ATS resume optimizer.

Rewrite the resume professionally.
Improve bullet points using strong action verbs.
Suggest improvements.
Find missing skills based on job description.

Return ONLY valid JSON in this format:
{{
  "improved_resume": "text",
  "suggestions": ["point1", "point2"],
  "missing_skills": ["skill1", "skill2"]
}}

Job Description:
{job_desc}

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {"error": content}