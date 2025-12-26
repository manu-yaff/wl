import sqlite3
from typing import Optional

from src.db.create_project_table import DATABASE_NAME


def create(name: Optional[str], context: Optional[str]):
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()

            create_project_query_string = """
                INSERT INTO Project (name, context)
                VALUES (?, ?)
            """

            project_data = (name, context)
            cursor.execute(create_project_query_string, project_data)
            connection.commit()

            print("Record inserted successfully")

    except sqlite3.IntegrityError as e:
        print(f"Error: Integrity constraint error {e}")
        print(f"Input: {name}, {context}")
        raise

    except Exception as e:
        print(f"Unknown error: {e}")
        raise
