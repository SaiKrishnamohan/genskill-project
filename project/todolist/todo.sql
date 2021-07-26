drop table if exists eventlist;
drop table if exists users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL
);

CREATE TABLE eventlist (
    user_id INTEGER,
    time TIME,
    date DATE,
    event TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);