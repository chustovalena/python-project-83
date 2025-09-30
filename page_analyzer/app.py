import logging
import os
from flask import Flask
from dotenv import load_dotenv
from repository import UrlRepository
from page_analyzer.log_conf import RequestFormatter, RequestFilter
from page_analyzer.routes import register_routes


def create_app(db_url=None):
    app = Flask(__name__)

    formatter = RequestFormatter(
        (
            "%(asctime)s [%(levelname)s] %(remote_addr)s "
            "%(method)s %(path)s: %(message)s"
        )
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(RequestFilter())
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DATABASE_URL'] = db_url or os.getenv('DATABASE_URL')
    app.debug = True

    repo = UrlRepository(app.config['DATABASE_URL'])

    register_routes(app, repo)

    return app


app = create_app()
