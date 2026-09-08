import io,re
from fastapi import FastAPI,File,Form,UploadFile,HTTPException,Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel,Field
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.auth import hash_password,create_token,verify_token
from app.db import connect,init_db
app=FastAPI(title='AI Resume Analyzer API',version='4.0.0')
init_db(); security=HTTPBearer(auto_error=False)
SKILLS=['python','django','fastapi','flask','react','javascript','typescript','java','c#','sql','postgresql','mongodb','docker','git','aws','machine learning','deep learning','pytorch','tensorflow','pandas','scikit-learn','nlp','rest api','html','css','power bi','excel']
class Credentials(BaseModel): username:str=Field(min_length=3,max_length=80); password:str=Field(min_length=6,max_length=200)
def current_user(creds:HTTPAuthorizationCredentials=Depends(security)):
    if not creds: raise HTTPException(401,'Authentication required')
    user=verify_token(creds.credentials)
    if not user: raise HTTPException(401,'Invalid or expired token')
    return user
def extract(text:str):
    low=text.lower();return sorted({s for s in SKILLS if re.search(r'(?<![a-z])'+re.escape(s)+r'(?![a-z])',low)})
def pdf_text(data:bytes):
    try:return '\n'.join(p.extract_text() or '' for p in PdfReader(io.BytesIO(data)).pages)
    except Exception as e:raise HTTPException(400,f'Invalid PDF: {e}')
def similarity(a:str,b:str):
    if not a.strip() or not b.strip():return 0.0
    m=TfidfVectorizer(stop_words='english').fit_transform([a,b]);return round(float(cosine_similarity(m[0:1],m[1:2])[0][0])*100,1)
@app.get('/health')
def health():return {'status':'ok','service':'ai-resume-analyzer','version':'4.0.0','engine':'tfidf-plus-skill-matching'}
@app.post('/auth/register')
def register(body:Credentials):
    with connect() as c:
        if c.execute('SELECT 1 FROM users WHERE username=?',(body.username,)).fetchone(): raise HTTPException(409,'Username already exists')
        c.execute('INSERT INTO users(username,password_hash) VALUES(?,?)',(body.username,hash_password(body.password)));c.commit()
    return {'message':'registered','username':body.username}
@app.post('/auth/login')
def login(body:Credentials):
    with connect() as c: u=c.execute('SELECT * FROM users WHERE username=?',(body.username,)).fetchone()
    if not u or u['password_hash']!=hash_password(body.password): raise HTTPException(401,'Invalid username or password')
    return {'access_token':create_token(u['username']),'token_type':'bearer'}
@app.get('/auth/me')
def me(user=Depends(current_user)): return user
@app.get('/skills')
def skills():return {'skills':SKILLS}
@app.post('/analyze')
async def analyze(resume:UploadFile=File(...),job_description:str=Form(...),user=Depends(current_user)):
    if resume.content_type!='application/pdf':raise HTTPException(400,'Resume must be a PDF')
    text=pdf_text(await resume.read());r=set(extract(text));j=set(extract(job_description));matched=sorted(r&j);missing=sorted(j-r);skill_score=100*len(matched)/max(1,len(j));text_score=similarity(text,job_description);score=round(skill_score*0.7+text_score*0.3,1)
    return {'user':user['username'],'filename':resume.filename,'match_score':score,'skill_score':round(skill_score,1),'text_similarity':text_score,'matched_skills':matched,'missing_skills':missing,'resume_skills':sorted(r),'job_skills':sorted(j),'recommendation':'Tailor measurable achievements and add missing job keywords.' if missing else 'Strong coverage; quantify achievements and outcomes.'}
app.mount('/',StaticFiles(directory='web',html=True),name='web')
