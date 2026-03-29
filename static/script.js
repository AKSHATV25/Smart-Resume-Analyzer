function upload() {
    let fileInput = document.getElementById("resume");
    let jobdesc = document.getElementById("jobdesc").value.trim();

    if (!fileInput.files.length) {
        alert("Please upload a resume!");
        return;
    }

    let file = fileInput.files[0];

    let formData = new FormData();
    formData.append("resume", file);
    formData.append("jobdesc", jobdesc);

    fetch("/analyze", {
        method: "POST",
        body: formData
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Server error");
        }
        return res.json();
    })
    .then(data => {
        console.log("Response:", data);

        // Show result section
        document.getElementById("result").classList.remove("hidden");

        // ✅ Safe updates (avoid undefined errors)
        document.getElementById("score").innerText = data.score ? data.score + "%" : "0%";
        document.getElementById("sim").innerText = data.similarity ? data.similarity + "%" : "0%";

        document.getElementById("progress").style.width = (data.score || 0) + "%";

        // ✅ Matched Skills
        let matched = document.getElementById("matched");
        matched.innerHTML = "";
        (data.matched || []).forEach(s => {
            matched.innerHTML += `<span class="badge matched">${s}</span>`;
        });

        // ✅ Missing Skills
        let missing = document.getElementById("missing");
        missing.innerHTML = "";
        (data.missing || []).forEach(s => {
            missing.innerHTML += `<span class="badge missing">${s}</span>`;
        });

        // ✅ Suggestions
        let suggestions = document.getElementById("suggestions");
        suggestions.innerHTML = "";
        (data.suggestions || []).forEach(s => {
            suggestions.innerHTML += `<div class="suggestion">${s}</div>`;
        });
    })
    .catch(err => {
        console.error(err);
        alert("Error analyzing resume. Check backend.");
    });
}