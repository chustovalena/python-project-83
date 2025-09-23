import psycopg
from psycopg.rows import dict_row


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg.connect(self.db_url, row_factory=dict_row)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""SELECT DISTINCT ON (urls.id)
                    urls.id,
                    urls.name,
                    url_checks.created_at AS last_check,
                    url_checks.status_code
                    FROM urls
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id
                    ORDER BY urls.id, url_checks.created_at DESC;""")
                return cur.fetchall()

    def find(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT * FROM urls WHERE id=%s", (url_id,))
                url = cur.fetchone()
                return dict(url) if url else None

    def save(self, url):
        name = url['url']
        existing = self.find_name(name)

        if existing:
            return None
        return self._create(url)

    def find_name(self, name):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT * FROM urls WHERE name = %s;", (name,))
                return cur.fetchone()

    def _create(self, url):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""
                INSERT INTO urls (name) VALUES (%s) RETURNING id, name, created_at;
                """, (url['url'],))
                new_url = cur.fetchone()
            conn.commit()
            return new_url

    def new_check(self, url_id, status_code, h1, title, description):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("INSERT INTO url_checks (url_id, status_code, h1, title, description) VALUES (%s, %s, %s, %s, %s) RETURNING id;", (url_id, status_code, h1, title, description,))
                check_id = cur.fetchone()['id']
            conn.commit()
            return check_id

    def get_checks_with_id(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC;", (url_id,))
                return cur.fetchall()
