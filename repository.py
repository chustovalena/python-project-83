import psycopg
from psycopg.rows import dict_row


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg.connect(self.db_url, row_factory=dict_row)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM urls ORDER BY id DESC")
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
            return existing
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

