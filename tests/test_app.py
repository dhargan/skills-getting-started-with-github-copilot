import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307

def test_activities_list():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_signup_and_duplicate():
    # Varsayılan bir etkinlik ve e-posta ile test
    response = client.get("/activities")
    activities = response.json()
    if not activities:
        pytest.skip("No activities defined in app.")
    activity_name = list(activities.keys())[0]
    email = "testuser@mergington.edu"
    # İlk kayıt
    signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup.status_code == 200
    # Tekrar kayıt (aynı e-posta)
    duplicate = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert duplicate.status_code == 400 or duplicate.status_code == 409
