CREATE TABLE publisher (
    id      SERIAL PRIMARY KEY,

    title   VARCHAR(64) NOT NULL,

    UNIQUE(title)
);

ALTER TABLE book
ADD COLUMN publisher_id SERIAL 
REFERENCES publisher(id);
