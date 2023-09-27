import pytest
from ras import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_login_valid_credentials(client):
    response = client.post('/', data=dict(uname='test@example.com', psd='password'), follow_redirects=True)
    assert response.status_code == 200 

def test_login_invalid_credentials(client):
    response = client.post('/', data=dict(uname='invalid@example.com', psd='invalid_password'), follow_redirects=True)
    assert b'Invalid email/password. Try Again..' in response.data

def test_login_invalid_password(client):
    response = client.post('/', data=dict(uname='imailshubhamjoshi@gmail.com', psd='wrong_password'), follow_redirects=True)
    assert b'Invalid password. Try Again..' in response.data
