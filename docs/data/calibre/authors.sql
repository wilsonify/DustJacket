
-- authors definition

CREATE TABLE authors (
 id   INTEGER PRIMARY KEY,
 name TEXT NOT NULL COLLATE NOCASE,
 sort TEXT COLLATE NOCASE,
 link TEXT NOT NULL DEFAULT "",
 UNIQUE(name)
 );
