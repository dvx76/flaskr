from flaskr.app import app


def test_homepage():
    with app.test_client() as client:
        response = client.get("/posts/1")
        assert response.status_code == 200
        assert response.json() == {
            "author_id": 1,
            "body": "world",
            "created": "2025-09-23T06:12:15Z",
            "id": 1,
            "title": "hello",
        }
