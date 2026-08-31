import pytest


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}


def test_login_valid_credentials(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'password123'})
    assert response.status_code == 200
    assert response.json == {'status': 'ok', 'role': 'admin'}


def test_login_wrong_password(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'nope'})
    assert response.status_code == 401
    assert response.json == {'status': 'fail'}


@pytest.mark.parametrize('username,password', [
    ("' OR '1'='1' --", 'anything'),
    ('admin', "' OR '1'='1"),
    ("admin'--", 'anything'),
    ("' UNION SELECT 1, 'x', 'y', 'admin' --", 'anything'),
])
def test_login_rejects_sql_injection(client, username, password):
    response = client.post('/login', data={'username': username, 'password': password})
    assert response.status_code == 401
    assert response.json == {'status': 'fail'}


def test_login_injection_does_not_drop_table(client):
    response = client.post(
        '/login',
        data={'username': "x'; DROP TABLE users; --", 'password': 'x'},
    )
    assert response.status_code == 401
    assert client.post(
        '/login', data={'username': 'alice', 'password': 'alice'}
    ).status_code == 200
