-- tags definition

CREATE TABLE tags (
 id   INTEGER PRIMARY KEY,
 name TEXT NOT NULL COLLATE NOCASE,
 UNIQUE (name)
 );

CREATE INDEX tags_idx ON tags (name COLLATE NOCASE);