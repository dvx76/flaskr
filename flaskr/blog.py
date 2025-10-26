from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from sqlalchemy import select
from werkzeug.exceptions import abort

from flaskr.auth import login_required

from .db import db_session
from .models import Post, User

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    posts = db_session.scalars(select(Post).order_by(Post.created.desc()))
    return render_template("blog/index.html.j2", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author=g.user)
            db_session.add(post)
            db_session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html.j2")


def get_post(id: int) -> Post:
    post = db_session.get(Post, id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if post.author_id != g.user.id:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db_session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html.j2", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db_session.delete(get_post(id))
    db_session.commit()
    return redirect(url_for("blog.index"))
