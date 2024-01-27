import pytest
from app.__init__ import create_app, db
from flask import json

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_user_registration(client):
    valid_payload = {
        "username": "testuser",
        "email_address": "testuser@example.com",
        "password": "password123"
    }
    response = client.post('/auth/register', data=json.dumps(valid_payload), content_type='application/json')

    assert response.status_code == 201
    assert 'User created successfully' in json.loads(response.data)['message']
