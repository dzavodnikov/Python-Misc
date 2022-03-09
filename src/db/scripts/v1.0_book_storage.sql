CREATE TABLE author (
    id      SERIAL PRIMARY KEY,

    name    VARCHAR(64) NOT NULL
);

CREATE TABLE book (
    id      SERIAL PRIMARY KEY,

    title   VARCHAR(128) NOT NULL
);

CREATE TABLE author_book (
    author_id      SERIAL REFERENCES 
    author(id) NOT NULL,

    book_id      SERIAL REFERENCES 
    book(id) NOT NULL,

    UNIQUE(author_id, book_id)
);
