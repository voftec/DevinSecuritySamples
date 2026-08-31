import pytest


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}


def test_files_serves_static_file(client):
    response = client.get('/files?name=notes.txt')
    assert response.status_code == 200


def test_files_default_is_notes(client):
    assert client.get('/files').status_code == 200


@pytest.mark.parametrize('name', [
    '../app.py',
    '../../etc/passwd',
    '....//....//etc/passwd',
    '..\\app.py',
    '..%2fapp.py',
    '/etc/passwd',
    'C:\\Windows\\win.ini',
    '../sample.db',
    'static/../app.py',
])
def test_files_rejects_traversal(client, name):
    response = client.get('/files', query_string={'name': name})
    assert response.status_code in (400, 404)
    assert b'Flask' not in response.data
    assert b'root:' not in response.data
