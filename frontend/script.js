const API_URL = "http://127.0.0.1:8000";


async function analyzeResume() {

    const fileInput = document.getElementById("resumeFile");

    const statusMessage =
        document.getElementById("statusMessage");

    const analyzeButton =
        document.getElementById("analyzeButton");


    // Check if a file was selected

    if (fileInput.files.length === 0) {

        statusMessage.textContent =
            "Please select a resume first.";

        return;
    }


    const file = fileInput.files[0];


    // Validate file type

    const allowedTypes = [
        "application/pdf",

        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ];


    if (!allowedTypes.includes(file.type)) {

        statusMessage.textContent =
            "Only PDF and DOCX files are allowed.";

        return;
    }


    // Validate file size

    const maxSize = 5 * 1024 * 1024;


    if (file.size > maxSize) {

        statusMessage.textContent =
            "File size must be less than 5 MB.";

        return;
    }


    // Create form data

    const formData = new FormData();

    formData.append("file", file);


    // Update UI

    statusMessage.textContent =
        "Uploading and analyzing resume...";

    analyzeButton.disabled = true;


    try {

        const response = await fetch(
            `${API_URL}/upload`,
            {
                method: "POST",

                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Upload failed."
            );
        }


        // Display results

        displayResults(data);


        statusMessage.textContent =
            "Resume analyzed successfully.";


    } catch (error) {

        console.error(error);


        statusMessage.textContent =
            error.message;

    } finally {

        analyzeButton.disabled = false;
    }
}


function displayResults(data) {

    const analysis = data.analysis;


    document.getElementById("fileName")
        .textContent = analysis.filename;


    document.getElementById("wordCount")
        .textContent = analysis.word_count;


    document.getElementById("skillCount")
        .textContent = analysis.skill_count;


    document.getElementById("skills")
        .textContent =
        analysis.skills.length > 0
            ? analysis.skills.join(", ")
            : "No skills detected";


    document.getElementById("textPreview")
        .textContent =
        analysis.text_preview || "No text extracted";


    document.getElementById("resultsSection")
        .style.display = "block";
}