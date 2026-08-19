from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from uuid import uuid4

from backend.analyzer import analyze_resume


# --------------------------------------------------
# Application Configuration
# --------------------------------------------------

app = FastAPI(
    title="Resume Analyzer API",
    description="Backend API for the Cloud-Based Resume Analyzer",
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Upload Folder
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Allowed File Types
# --------------------------------------------------

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx"
}


# --------------------------------------------------
# Maximum File Size
# --------------------------------------------------

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Resume Analyzer API is running",
        "version": "1.0.0"
    }


# --------------------------------------------------
# Health Check Endpoint
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Resume Upload Endpoint
# --------------------------------------------------

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Check if filename exists
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided"
        )

    # Get file extension
    extension = Path(file.filename).suffix.lower()

    # Check allowed file type
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed"
        )

    # Read file content
    file_content = await file.read()

    # Check file size
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    # Generate unique filename
    unique_filename = f"{uuid4().hex}{extension}"

    # Create complete file path
    file_path = UPLOAD_FOLDER / unique_filename

    # Save file
    with open(file_path, "wb") as output_file:
        output_file.write(file_content)

    # Analyze resume
    analysis_result = analyze_resume(
        file_path=file_path,
        original_filename=file.filename
    )

    return {
        "message": "Resume uploaded and analyzed successfully",
        "filename": file.filename,
        "stored_filename": unique_filename,
        "analysis": analysis_result
    }