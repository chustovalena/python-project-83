import os
import pytest
from page_analyzer.app import create_app


@pytest.fixture
def app():
    os.environ['DATABASE_URL'] = "postgresql://test_user:test_pass@localhost:5432/test_db"
    os.environ['SECRET_KEY'] = 'test-secret'
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()
