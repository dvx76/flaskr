import os
import sqlite3

import connexion
from werkzeug.security import check_password_hash

from flaskr.db import get_db


class ResourceNotFound(connexion.ProblemException):
    def __init__(self, resource_id: int | None = None):
        super().__init__(
            status=404,
            title="NotFound",
            detail=f"Resource {resource_id if resource_id else ''} does not exist",
        )


def auth(username: str, password: str):
    db = sqlite3.connect(
        app.app.config["DATABASE"],
        detect_types=sqlite3.PARSE_DECLTYPES,
        uri=True,
    )
    db.row_factory = sqlite3.Row

    user_row = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()
    db.close()

    if user_row and check_password_hash(user_row["password"], password):
        return {"sub": user_row["id"], "username": username}
    return


def get_all_posts():
    db = get_db()
    posts = db.execute(
        "SELECT id, author_id, created, title, body FROM post ORDER BY created DESC"
    ).fetchall()

    return [dict(post) for post in posts]


def get_post(id: int):
    db = get_db()
    post = db.execute(
        "SELECT id, author_id, created, title, body FROM post WHERE id = (?)", (id,)
    ).fetchone()

    if not post:
        raise ResourceNotFound(id)

    return dict(post)


def update_post(id: int, body: dict, token_info: dict):
    db = get_db()
    post = db.execute(
        "UPDATE post SET title = ?, body = ? WHERE id = ? and author_id = ? "
        "RETURNING id, author_id, created, title, body",
        (body["title"], body["body"], id, token_info["sub"]),
    ).fetchone()
    db.commit()

    if not post:
        return {"message": f"Post {id} not found"}, 404

    return dict(post)


def delete_post(id: int, token_info: dict):
    db = get_db()
    post = db.execute(
        "DELETE FROM post WHERE id = ? and author_id = ? "
        "RETURNING id, author_id, created, title, body",
        (id, token_info["sub"]),
    ).fetchone()
    db.commit()

    if not post:
        return {"message": f"Post {id} not found"}, 404

    return None, 204


def create_post(body: dict, token_info: dict):
    db = get_db()
    row = db.execute(
        "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?) "
        "RETURNING id, author_id, created, title, body",
        (body["title"], body["body"], token_info["sub"]),
    ).fetchone()
    db.commit()

    return dict(row), 201


app = connexion.FlaskApp(__name__)
app.add_api("openapi.yaml")
app.app.config.from_mapping(
    DATABASE=os.path.join(app.app.instance_path, "flaskr.sqlite")
)

if __name__ == "__main__":
    app.run("flaskr.app:app", port=5000)
