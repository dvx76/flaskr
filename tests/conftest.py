import pytest
from flask import Flask

from flaskr import create_app
from flaskr.db import get_db, init_db


@pytest.fixture
def app():
    app = create_app({"DATABASE": "file:mem1?mode=memory&cache=shared"})

    with app.app_context():
        init_db()
        db = get_db()
        db.execute(
            "INSERT INTO user (username, password) VALUES "
            "('test', 'scrypt:32768:8:1$B6EWUB7sblZHpKwE$74951791e0ebcdcf91999e0e4c3e7768fcb87f994c35de0d80e99d83ec36e9f542b76c4d486c57ced5cea72fd76c3f5a64b0a2c31a89a02e3a86a52a6f52fb1c')"
        )
        db.execute(
            "INSERT INTO user (username, password) VALUES "
            "('other', 'scrypt:32768:8:1$6DDdh5peSL3fmCBy$c997bb4e0ecdeb5ad2e94cd4cde3a58efa290889a7c40497b154cd23df46ffc25f731370f849ab262fd310d9ee48ce5a9950a6910e08b9a8f52ec791acb85c61')"
        )
        db.execute(
            "INSERT INTO post (title, body, author_id, created) VALUES"
            "('test title', 'test' || x'0a' || 'body', 1, '2025-01-01 00:00:00')"
        )
        db.commit()
        yield app


@pytest.fixture
def client(app: Flask):
    return app.test_client()
