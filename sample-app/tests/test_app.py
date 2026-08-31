def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}


def test_sql_injection_blocked(client):
    """A classic auth-bypass payload must not log in."""
    response = client.post('/login', data={
        'username': "' OR '1'='1' --",
        'password': 'anything'
    })
    assert response.status_code == 401
    assert response.json == {'status': 'fail'}


def test_valid_login(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.json == {'status': 'ok', 'role': 'admin'}


def test_admin_user_requires_auth(client):
    response = client.get('/admin/users/1')
    assert response.status_code == 401
    assert response.json == {'status': 'fail', 'error': 'authentication required'}


def test_admin_user_requires_admin_role(client):
    client.post('/login', data={'username': 'alice', 'password': 'alice'})
    response = client.get('/admin/users/1')
    assert response.status_code == 403
    assert response.json == {'status': 'fail', 'error': 'admin required'}


def test_admin_user_returns_safe_fields(client):
    client.post('/login', data={'username': 'admin', 'password': 'password123'})
    response = client.get('/admin/users/1')
    assert response.status_code == 200
    assert response.json == {'id': 1, 'username': 'admin', 'role': 'admin'}
    assert 'password' not in response.json


def test_admin_user_not_found(client):
    client.post('/login', data={'username': 'admin', 'password': 'password123'})
    response = client.get('/admin/users/999')
    assert response.status_code == 404
    assert response.json == {'error': 'not found'}


def test_path_traversal_blocked(client):
    response = client.get('/files?name=../app.py')
    assert response.status_code == 400
    assert response.json == {'error': 'invalid path'}


def test_static_file_allowed(client):
    response = client.get('/files?name=notes.txt')
    assert response.status_code == 200
