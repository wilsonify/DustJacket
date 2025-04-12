import json
import os
import sqlite3

import pandas as pd


def safe_filename(book_id, title):
    sanitized_title = (
        title[:50]
        .replace('/', '-')
        .replace('\\', '-')
        .replace(' ', '-')
    )
    return f"{book_id:04d}-{sanitized_title}.json"


def export_books_to_json(sqlite_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with sqlite3.connect(sqlite_file) as conn:
        books_df = pd.read_sql("SELECT * FROM books", conn)
        for _, row in books_df.iterrows():
            book_id = row['id']
            book_uuid = row['uuid']
            title = row['title']
            filename = safe_filename(book_id, title)
            file_path = os.path.join(output_dir, filename)
            author_id = pd.read_sql(f"""SELECT author FROM books_authors_link WHERE book = {book_id}""", conn).loc[
                0, "author"]
            author_name = pd.read_sql(f"""SELECT name FROM authors WHERE id = {author_id}""", conn).loc[0, "name"]
            try:
                publisher_id = (pd
                .read_sql(f"""SELECT publisher FROM books_publishers_link WHERE book={book_id}""", conn)
                .loc[0, "publisher"]
                )
                publisher_name = (
                    pd.read_sql(f"""SELECT name FROM publishers WHERE id = {publisher_id}""", conn)
                    .loc[0, "name"]
                )
            except:
                publisher_name = "unknown"

            try:
                series_id = (
                    pd.read_sql(f"""SELECT series FROM books_series_link WHERE book = {book_id}""", conn)
                    .loc[0, "series"]
                )
                series_name = pd.read_sql(f"""SELECT name FROM series WHERE id = {series_id}""", conn).loc[0, "name"]
            except:
                series_name = ""

            tags_ids = pd.read_sql(f"""SELECT tag FROM books_tags_link WHERE book={book_id}""", conn)
            tag_ids_list = tags_ids["tag"].to_list()
            tags_list = []
            for tag_id in tag_ids_list:
                tag_text = pd.read_sql(f"""SELECT name FROM tags WHERE id={tag_id}""", conn).loc[0, "name"]
                tags_list.append(tag_text)

            try:
                comments_text = pd.read_sql(f"""SELECT text FROM comments WHERE book={book_id}""", conn).loc[0, "text"]
            except:
                comments_text = ""

            book_dict = dict(
                book_id=row['id'],
                book_uuid=row["uuid"],
                title=row["title"],
                pubdate=row["pubdate"],
                isbn=row["isbn"],
                author_name=author_name,
                publisher_name=publisher_name,
                series_name=series_name,
                series_index=row["series_index"],
                tags=tags_list,
                description=comments_text,
            )
            json.dump(book_dict, open(file_path, 'w'), default=str, indent=2)


if __name__ == "__main__":
    export_books_to_json("data/input/metadata.db", "data/output_actual/books_metadata")
