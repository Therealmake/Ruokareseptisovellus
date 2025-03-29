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
    category TEXT,
    diet TEXT,
    image BLOB,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    user_id INTEGER REFERENCES users,
    comment TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE diets (
    id INTEGER PRIMARY KEY,
    name TEXT
);