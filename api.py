import io,re
from fastapi import FastAPI,File,Form,UploadFile,HTTPException
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app=FastAPI(title='AI Resume Analyzer API',version='3.0.0')
SKILLS=['python','django','fastapi','flask','react','javascript','typescript','java','c#','sql','postgresql','mongodb','docker','git','aws','machine learning','deep learning','pytorch','tensorflow','pandas','scikit-learn','nlp','rest api','html','css','power bi','excel']
def extract(text:str):
    low=text.lower();return sorted({s for s in SKILLS if re.search(r'(?<![a-z])'+re.escape(s)+r'(?![a-z])',low)})
def pdf_text(data:bytes):
    try:return '\n'.join(p.extract_text() or '' for p in PdfReader(io.BytesIO(data)).pages)
    except Exception as e:raise HTTPException(400,f'Invalid PDF: {e}')
def similarity(a:str,b:str):
    if not a.strip() or not b.strip():return 0.0
    m=TfidfVectorizer(stop_words='english').fit_transform([a,b]);return round(float(cosine_similarity(m[0:1],m[1:2])[0][0])*100,1)
@app.get('/health')
def health():return {'status':'ok','service':'ai-resume-analyzer','version':'3.0.0','engine':'tfidf-plus-skill-matching'}
@app.get('/skills')
def skills():return {'skills':SKILLS}
@app.post('/analyze')
async def analyze(resume:UploadFile=File(...),job_description:str=Form(...)):
    if resume.content_type!='application/pdf':raise HTTPException(400,'Resume must be a PDF')
    text=pdf_text(await resume.read());r=set(extract(text));j=set(extract(job_description));matched=sorted(r&j);missing=sorted(j-r);skill_score=100*len(matched)/max(1,len(j));text_score=similarity(text,job_description);score=round(skill_score*0.7+text_score*0.3,1)
    return {'filename':resume.filename,'match_score':score,'skill_score':round(skill_score,1),'text_similarity':text_score,'matched_skills':matched,'missing_skills':missing,'resume_skills':sorted(r),'job_skills':sorted(j),'recommendation':'Tailor measurable achievements and add missing job keywords.' if missing else 'Strong coverage; quantify achievements and outcomes.'}
app.mount('/',StaticFiles(directory='web',html=True),name='web')
