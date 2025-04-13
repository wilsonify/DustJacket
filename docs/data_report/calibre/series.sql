-- series definition

CREATE TABLE series (
 id   INTEGER PRIMARY KEY,
 name TEXT NOT NULL COLLATE NOCASE,
 sort TEXT COLLATE NOCASE,
 UNIQUE (name)
 );

 CREATE INDEX series_idx ON series (name COLLATE NOCASE);