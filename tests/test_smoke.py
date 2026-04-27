from fastapi.testclient import TestClient

from src.app.factory import create_app


def _client():
    return TestClient(create_app())


def test_health_endpoint():
    client = _client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_dashboard_redirects_when_unauthenticated():
    client = _client()
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"].startswith("/login")


def test_login_page_renders():
    client = _client()
    resp = client.get("/login")
    assert resp.status_code == 200


def test_login_flow_grants_access_to_protected_page():
    client = _client()
    resp = client.post(
        "/login",
        data={"username": "admin", "password": "admin", "next": "/"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"] == "/"

    resp = client.get("/")
    assert resp.status_code == 200
    assert "Dashboard" in resp.text


def test_login_with_bad_credentials():
    client = _client()
    resp = client.post(
        "/login",
        data={"username": "admin", "password": "wrong", "next": "/"},
    )
    assert resp.status_code == 401
