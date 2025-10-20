import pytest
from flask import g, session
from flask.testing import FlaskClient

from flaskr import db


def test_register_get(client: FlaskClient):
    response = client.get("/auth/register")

    assert response.status_code == 200


def test_register_post(client: FlaskClient):
    response = client.post("/auth/register", data={"username": "a", "password": "a"})

    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"

    assert (
        db.get_db().execute("SELECT * FROM user WHERE username = 'a'").fetchone()
        is not None
    )


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("test", "", b"Password is required."),
        ("test", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data


def test_login(client):
    assert client.get("/auth/login").status_code == 200
    response = client.post("/auth/login", data={"username": "test", "password": "test"})
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", "Incorrect username."),
        ("test", "a", "Incorrect password."),
    ),
)
def test_login_validate_input(client, username, password, message):
    response = client.post(
        "/auth/login", data={"username": username, "password": password}
    )
    assert message in response.text


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_create_update_validate(client: FlaskClient, path: str):
    client.post("/auth/login", data={"username": "test", "password": "test"})

    response = client.post(path, data={"title": "", "body": "invalid post"})
    assert b"Title is required." in response.data

    conn = db.get_db()
    post = conn.execute("SELECT * FROM post WHERE body = 'invalid post'").fetchone()
    assert post is None


def test_delete(client: FlaskClient):
    client.post("/auth/login", data={"username": "test", "password": "test"})

    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    conn = db.get_db()
    post = conn.execute("SELECT * FROM post WHERE id = 1").fetchone()
    assert post is None
