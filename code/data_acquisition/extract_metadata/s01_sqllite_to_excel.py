import os.path
import sqlite3

from openpyxl import Workbook

path_to_here = os.path.abspath(os.path.dirname(__file__))
path_to_data = os.path.abspath(f"{path_to_here}/../../../data")

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

    # Create a new Excel workbook
    wb = Workbook()
    # Remove the default sheet created with a new workbook
    default_sheet = wb.active
    wb.remove(default_sheet)

    with sqlite3.connect(sqlite_file) as conn:
        cursor = conn.cursor()

        for table in table_names:
            print(f"write table={table}")
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            # Create a new sheet
            ws = wb.create_sheet(title=table)

            # Write header
            ws.append(column_names)

            # Write data
            for row in rows:
                ws.append(row)

    wb.save(excel_file)
    print(f"done writing excel_file={excel_file}")


if __name__ == "__main__":
    export_sqlite_to_excel(f"{path_to_data}/input/metadata.db", f"{path_to_data}/output_actual/metadata_exported.xlsx")
