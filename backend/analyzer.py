from pathlib import Path


import pdfplumber
from docx import Document


# --------------------------------------------------
# Skills We Want to Detect
# --------------------------------------------------

SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "TypeScript",
    "React",
    "Node.js",
    "HTML",
    "CSS",
    "Flask",
    "FastAPI",
    "Django",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "AWS",
    "Azure",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Linux",
    "Machine Learning",
    "Deep Learning",
    "Blockchain",
    "Cryptography"
]


# --------------------------------------------------
# Extract Text from PDF
# --------------------------------------------------

def extract_text_from_pdf(file_path: Path) -> str:

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# --------------------------------------------------
# Extract Text from DOCX
# --------------------------------------------------

def extract_text_from_docx(file_path: Path) -> str:

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


# --------------------------------------------------
# Extract Text Based on File Type
# --------------------------------------------------

def extract_text(file_path: Path) -> str:

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        return extract_text_from_pdf(file_path)

    elif extension == ".docx":

        return extract_text_from_docx(file_path)

    else:

        raise ValueError(
            "Unsupported file type"
        )


# --------------------------------------------------
# Detect Skills
# --------------------------------------------------

def detect_skills(text: str):

    detected_skills = []

    text_lower = text.lower()

    for skill in SKILLS:

        if skill.lower() in text_lower:

            detected_skills.append(skill)

    return detected_skills


# --------------------------------------------------
# Count Words
# --------------------------------------------------

def count_words(text: str) -> int:

    words = text.split()

    return len(words)


# --------------------------------------------------
# Resume Analyzer
# --------------------------------------------------

def analyze_resume(
    file_path: Path,
    original_filename: str
):

    text = extract_text(file_path)

    skills = detect_skills(text)

    word_count = count_words(text)

    return {

        "filename": original_filename,

        "skills": skills,

        "skill_count": len(skills),

        "word_count": word_count,

        "text_preview": text[:1000]
    }