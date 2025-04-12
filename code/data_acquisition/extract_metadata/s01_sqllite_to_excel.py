import sqlite3

import pandas as pd

table_names = [
    'authors',
    'books',
    'publishers',
    'data',
    'tags',
    'identifiers',
    'languages',
    'series',
    'comments',
    'books_authors_link',
    'books_languages_link',
    'books_publishers_link',
    'books_series_link',
    'books_tags_link',
]


def export_sqlite_to_excel(sqlite_file, excel_file):
    print("start export_sqlite_to_excel")
    print(f"sqlite_file={sqlite_file}")
    print(f"excel_file={excel_file}")
    with sqlite3.connect(sqlite_file) as conn:
        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            for table in table_names:
                print(f"write table={table}")
                df = pd.read_sql(f"SELECT * FROM {table}", conn)
                df.to_excel(excel_writer=writer, sheet_name=table, index=False, engine="openpyxl")
    print(f"done writing excel_file={excel_file}")


if __name__ == "__main__":
    export_sqlite_to_excel("data/input/metadata.db", "data/output_actual/metadata_exported.xlsx")
