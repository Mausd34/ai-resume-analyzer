from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pypdf import PdfReader
import io, re

app = FastAPI(title="AI Resume Analyzer API", version="1.0.0")
SKILLS = ["python","django","fastapi","flask","react","javascript","typescript","java","c#","sql","postgresql","mongodb","docker","git","aws","machine learning","deep learning","pytorch","tensorflow","pandas","scikit-learn","nlp","rest api","html","css","power bi","excel"]

def extract(text: str):
    low=text.lower(); return sorted({s for s in SKILLS if re.search(r"(?<![a-z])"+re.escape(s)+r"(?![a-z])", low)})

def pdf_text(data: bytes):
    try: return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
    except Exception as e: raise HTTPException(400, f"Invalid PDF: {e}")

@app.get("/health")
def health(): return {"status":"ok","service":"ai-resume-analyzer"}

@app.post("/analyze")
async def analyze(resume: UploadFile=File(...), job_description: str=Form(...)):
    if resume.content_type != "application/pdf": raise HTTPException(400,"Resume must be a PDF")
    text=pdf_text(await resume.read()); r=set(extract(text)); j=set(extract(job_description))
    matched=sorted(r&j); missing=sorted(j-r); score=round(100*len(matched)/max(1,len(j)),1)
    return {"filename":resume.filename,"match_score":score,"matched_skills":matched,"missing_skills":missing,"resume_skills":sorted(r),"job_skills":sorted(j),"recommendation":"Tailor measurable achievements and add missing job keywords." if missing else "Strong keyword coverage; quantify achievements."}
