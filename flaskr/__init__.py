import os
from typing import Any, Mapping, Optional

from flask import Flask

from . import auth, blog, db


def create_app(test_config: Optional[Mapping[str, Any]] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    app.jinja_options["autoescape"] = True

    os.makedirs(app.instance_path, exist_ok=True)

    @app.route("/ping")
    def ping():
        return "pong"

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    return app
