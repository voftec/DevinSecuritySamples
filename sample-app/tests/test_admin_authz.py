def login(client, username, password):
    return client.post('/login', data={'username': username, 'password': password})


def test_admin_user_requires_authentication(client):
    response = client.get('/admin/users/1')
    assert response.status_code == 401
    assert 'password' not in response.get_data(as_text=True)


def test_admin_user_forbidden_for_non_admin(client):
    assert login(client, 'alice', 'alice').status_code == 200
    response = client.get('/admin/users/1')
    assert response.status_code == 403
    assert 'password' not in response.get_data(as_text=True)


def test_admin_user_allowed_for_admin_without_password(client):
    assert login(client, 'admin', 'password123').status_code == 200
    response = client.get('/admin/users/2')
    assert response.status_code == 200
    assert response.json == {'id': 2, 'username': 'alice', 'role': 'user'}


def test_admin_user_not_found(client):
    assert login(client, 'admin', 'password123').status_code == 200
    response = client.get('/admin/users/999')
    assert response.status_code == 404


def test_logout_revokes_admin_access(client):
    assert login(client, 'admin', 'password123').status_code == 200
    assert client.post('/logout').status_code == 200
    assert client.get('/admin/users/1').status_code == 401
