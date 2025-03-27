CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    recipe_name TEXT,
    ingredients TEXT,
    instructions TEXT,
    user_id INTEGER REFERENCES users
);