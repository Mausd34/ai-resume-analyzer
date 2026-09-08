import streamlit as st
import requests
st.set_page_config(page_title='AI Resume Analyzer',page_icon='📄',layout='wide')
st.title('📄 AI Resume Analyzer'); st.caption('Resume-to-job matching dashboard')
base=st.sidebar.text_input('API URL','http://127.0.0.1:8000')
resume=st.file_uploader('Resume PDF',type=['pdf']); job=st.text_area('Job description',height=220)
if st.button('Analyze',type='primary') and resume and job.strip():
    try:
        r=requests.post(base+'/analyze',files={'resume':(resume.name,resume.getvalue(),'application/pdf')},data={'job_description':job},timeout=60); r.raise_for_status(); d=r.json()
        a,b,c=st.columns(3); a.metric('Match',f"{d['match_score']}%"); b.metric('Matched',len(d['matched_skills'])); c.metric('Missing',len(d['missing_skills']))
        st.success('Matched: '+', '.join(d['matched_skills']) if d['matched_skills'] else 'None'); st.warning('Improve: '+', '.join(d['missing_skills']) if d['missing_skills'] else 'Great coverage')
    except Exception as e: st.error(str(e))
