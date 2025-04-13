import json
import os
import sqlite3

path_to_here = os.path.abspath(os.path.dirname(__file__))
path_to_data = os.path.abspath(f"{path_to_here}/../../../data")


def safe_filename(book_id, title):
    sanitized_title = (
        title[:50]
        .replace('/', '-')
        .replace('\\', '-')
        .replace(' ', '-')
    )
    return f"{book_id:04d}-{sanitized_title}.json"


def fetch_one(cursor, query):
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else None


def fetch_all(cursor, query):
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


def export_books_to_json(sqlite_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with sqlite3.connect(sqlite_file) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get all books
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        for row in books:
            book_id = row['id']
            title = row['title']
            filename = safe_filename(book_id, title)
            file_path = os.path.join(output_dir, filename)

            # Author
            author_id = fetch_one(cursor, f"SELECT author FROM books_authors_link WHERE book = {book_id}")
            author_name = fetch_one(cursor, f"SELECT name FROM authors WHERE id = {author_id}") or "unknown"

            # Publisher
            publisher_id = fetch_one(cursor, f"SELECT publisher FROM books_publishers_link WHERE book = {book_id}")
            publisher_name = fetch_one(cursor, f"SELECT name FROM publishers WHERE id = {publisher_id}") or "unknown"

            # Series
            series_id = fetch_one(cursor, f"SELECT series FROM books_series_link WHERE book = {book_id}")
            series_name = fetch_one(cursor, f"SELECT name FROM series WHERE id = {series_id}") or ""

            # Tags
            tag_ids = fetch_all(cursor, f"SELECT tag FROM books_tags_link WHERE book = {book_id}")
            tags_list = []
            for tag_id in tag_ids:
                tag_text = fetch_one(cursor, f"SELECT name FROM tags WHERE id = {tag_id}")
                if tag_text:
                    tags_list.append(tag_text)

            # Comments
            comments_text = fetch_one(cursor, f"SELECT text FROM comments WHERE book = {book_id}") or ""

            # Final dictionary
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

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(book_dict, f, default=str, indent=2)


if __name__ == "__main__":
    export_books_to_json(f"{path_to_data}/input/metadata.db", f"{path_to_data}/output_actual/books_metadata")
