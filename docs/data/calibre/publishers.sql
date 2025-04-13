-- publishers definition

CREATE TABLE publishers (
 id   INTEGER PRIMARY KEY,
 name TEXT NOT NULL COLLATE NOCASE,
 sort TEXT COLLATE NOCASE,
 UNIQUE(name)
 );

CREATE INDEX publishers_idx ON publishers (name COLLATE NOCASE);