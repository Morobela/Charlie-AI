from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_project_and_chat_history():
    project = client.post('/api/project', json={'name':'P1','description':'d'}).json()
    assert project['id']
    chats = client.get(f"/api/project/{project['id']}/chats").json()
    assert isinstance(chats, list)


def test_artifact_versioning():
    project = client.post('/api/project', json={'name':'P2'}).json()
    art = client.post('/api/artifacts', json={'project_id': project['id'], 'name':'spec', 'content':'v1'}).json()
    updated = client.put(f"/api/artifacts/{art['id']}", json={'content':'v2'}).json()
    assert len(updated['versions']) == 2


def test_file_search_text_types():
    project = client.post('/api/project', json={'name':'P3'}).json()
    files = {'file': ('note.txt', b'alpha beta gamma alpha', 'text/plain')}
    r = client.post(f"/api/files/upload?project_id={project['id']}", files=files)
    assert r.status_code == 200
    s = client.get(f"/api/files/search?project_id={project['id']}&q=alpha").json()
    assert len(s) >= 1
