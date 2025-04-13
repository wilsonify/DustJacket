-- comments definition

CREATE TABLE comments (
 id INTEGER PRIMARY KEY,
 book INTEGER NOT NULL,
 text TEXT NOT NULL COLLATE NOCASE,
 UNIQUE(book)
 );

CREATE INDEX comments_idx ON comments (book);