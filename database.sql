CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    name varchar(255) UNIQUE NOT NULL,
    created_at date DEFAULT CURRENT_DATE
);
