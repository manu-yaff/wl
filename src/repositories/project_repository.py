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


def get(id: int):
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            get_one_query = """
                SELECT * FROM Project
                WHERE id = ?
            """

            cursor.execute(get_one_query, (id,))

            project = cursor.fetchone()

            return project

    except Exception as e:
        print(f"Error: {e}")
        raise


def update(id: int, name: str, context: str):
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            update_query = """
                UPDATE Project
                SET name = ?, context = ?
                WHERE id = ?
            """

            cursor.execute(update_query, (name, context, id))

            connection.commit()

            print("Record updated successfully")

    except Exception as e:
        print(f"Error: {e}")
        raise
