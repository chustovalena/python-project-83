CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    name varchar(255) UNIQUE NOT NULL,
    created_at date DEFAULT CURRENT_DATE
);


CREATE TABLE IF NOT EXISTS url_checks (
    id SERIAL PRIMARY KEY,
    url_id int NOT NULL REFERENCES urls(id),
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at date DEFAULT CURRENT_DATE
);
