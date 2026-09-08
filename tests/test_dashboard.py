from fastapi.testclient import TestClient
from api import app
client=TestClient(app)
def test_health(): assert client.get('/health').json()['status']=='ok'
def test_skills():
    r=client.get('/skills'); assert r.status_code==200; assert 'python' in r.json()['skills']
