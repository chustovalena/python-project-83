import os
import pytest
import psycopg
from page_analyzer.app import create_app
from repository import UrlRepository


@pytest.fixture(scope='session')
def db_url():
    return os.environ.get(
        'TEST_DATABASE_URL',
        "postgresql://test_user:test_pass@localhost:5432/test_db"
    )


@pytest.fixture(scope='session', autouse=True)
def setup_test_db(db_url):
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            with open('database.sql', 'r') as f:
                schema_sql = f.read()
                cur.execute(schema_sql)
            conn.commit()


@pytest.fixture(autouse=True)
def clean_tables(db_url):
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE url_checks, urls RESTART IDENTITY CASCADE;")
        conn.commit()
    yield


@pytest.fixture
def repo(db_url):
    return UrlRepository(db_url)


@pytest.fixture
def app(db_url):
    app = create_app(db_url=db_url)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()
