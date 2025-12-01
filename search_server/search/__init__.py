"""Flask app for search server."""
# pylint: disable=import-outside-toplevel

import os
import pathlib
import flask
from index import api


def init_app():
    """Initialize app."""
    app = flask.Flask(__name__)
    app.config["SEARCH_INDEX_SEGMENT_API_URLS"] = os.getenv(
        "SEARCH_INDEX_SEGMENT_API_URLS",
        "http://localhost:9000,http://localhost:9001,http://localhost:9002"
    ).split(",")

    base_dir = pathlib.Path(__file__).parent
    INDEX_DIR = pathlib.Path(__file__).parent / "inverted_index"
    app.config["INDEX_PATH"] = os.getenv(
        "INDEX_PATH",
        INDEX_DIR/"inverted_index_1.txt",
    )

    app.config["STOPWORDS_PATH"] = os.getenv(
        "STOPWORDS_PATH",
        str((base_dir / "stopwords.txt").resolve())
    )

    app.config["PAGERANK_PATH"] = os.getenv(
        "PAGERANK_PATH",
        str((base_dir / "pagerank.out").resolve())
    )

    # Register blueprints - USE CONSISTENT IMPORTS
    from index.api.main import bp as api_bp  # Changed this line
    app.register_blueprint(api_bp)

    import search.views.index as index
    app.register_blueprint(index.bp)

    return app


app = init_app()
