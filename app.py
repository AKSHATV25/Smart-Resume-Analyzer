from flask import Flask, render_template, request
from gemini_suggestions import gemini_improve_resume

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    resume = ""
    job_desc = ""

    if request.method == "POST":
        resume = request.form.get("resume")
        job_desc = request.form.get("job_desc")

        if resume and job_desc:
            result = gemini_improve_resume(resume, job_desc)

    return render_template(
        "index.html",
        result=result,
        resume=resume,
        job_desc=job_desc
    )

if __name__ == "__main__":
    app.run(debug=True)